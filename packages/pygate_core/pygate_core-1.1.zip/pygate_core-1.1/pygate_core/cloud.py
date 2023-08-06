﻿import logging
import threading
import time
from uuid import getnode as get_mac

import att_iot_gateway.att_iot_gateway as IOT                              #provide cloud support

from pygate_core import assetStateCache as valueCache, config

existingGatewayAssets = {}                                                      # used during sync of asset gateways: contains all the existing assets, when a new asset is created, the ref is remvoed from this list.
_sensorCallback = None                                                          #callback for pyGate module, called when sensor data is sent out.
_actuatorCallback = None                                                          #callback for pyGate module, called when actuator data came in and needs to be redistributed to the correct module.
_httpLock = threading.Lock()                                                    # makes http request thread save (only 1 plugin can call http at a time, otherwise we get confused.
_mqttLock = threading.Lock()                                                    # makes mqtt send requests thread save

def onActuate(device, actuator, value):
    '''called by att_iot_gateway when actuator command is received'''
    if _actuatorCallback:                                     # need a callback, otherwise there is no handler for the command (yet).
        if device:                                          # its an actuator for a specific device
            devid = device.split('_')                       # device id contains module name
            _actuatorCallback(devid[0], devid[1], actuator, value)
        else:                                               # it's an actuator at the level of the gateway.
            splitPos = actuator.find('_')
            module = actuator[:splitPos]          #get the module name from the actuator
            _actuatorCallback(module, None, actuator[splitPos + 1:], value)



def connect(actuatorcallback, sensorCallback):
    """set up the connection with the cloud from the specified configuration
       actuatorcallback: the callback function for actuator commands
                    format: onActuate(module, device, actuator, value)
       sensorCallback: the callback function that will be called when sensor data is sent to the cloud"""
    global _sensorCallback, _actuatorCallback
    _actuatorCallback = actuatorcallback
    _sensorCallback = sensorCallback
    IOT.on_message = onActuate
    success = False
    while not success:
        try:
            IOT.connect(config.apiServer, config.secure)
            if _authenticate():
                IOT.subscribe(config.broker, 8883 if config.secure else 1883, config.secure, 'cacert.pem')              							#starts the bi-directional communication   "att-2.cloudapp.net"
                success = True
            else:
                logging.error("Failed to authenticate with IOT platform")
                time.sleep(2)                                           # wait a little until we try again.
        except KeyboardInterrupt:                                       # when trying to stop the gateway, make certain this loop doesn't get stuck because of the exception handling.
            return
        except:
            logging.exception("failed to connect")
            time.sleep(2)

def _authenticate():
    '''if authentication had previously succeeded, loads credentials and validates them with the platform
       if not previously authenticated: register as gateway and wait until user has claimed it
       params:
    '''
    if not config.gatewayId:
        uid = _getUid()
        gatewayName = config.getConfig("general", "name", "pyGate")
        IOT.createGateway(gatewayName, uid)
        while True:                                     # we try to finish the claim process until success or app quits, cause the app can't continue without a valid and claimed gateway
            if IOT.finishclaim(gatewayName, uid):
                _storeConfig()
                time.sleep(2)                                # give the platform a litle time to set up all the configs so that we can subscribe correctly to the topic. If we don't do this, the subscribe could fail
                return True
            else:
                time.sleep(1)
        return False                                # if we get here, didn't succeed in time to finish the claiming process.
    else:
        IOT.GatewayId = config.gatewayId
        IOT.ClientId = config.clientId
        IOT.ClientKey = config.clientKey
        if IOT.authenticate():
            logging.info('Authenticated')
            return True
        else:
            logging.error('failed to authenticate')
            return False

def _getUid():
    'extract the mac address in order to identify the gateway in the cloud'
    mac = 0
    while True:                                                                     # for as long as we are getting a fake mac address back, try again (this can happen if the hw isn't ready yet, for instance usb wifi dongle)
        mac = get_mac()
        if mac & 0x10000000000 == 0:
            break
        time.sleep(1)                                                                    # wait a bit before retrying.

    result = hex(mac)[2:-1]                                                         # remove the 0x at the front and the L at the back.
    while len(result) < 12:                                                         # it could be that there were missing '0' in the front, add them manually.
        result = "0" + result
    result = result.upper()                                                         # make certain that it is upper case, easier to read, more standardized
    logging.info('mac address: ' + result)
    return result

def _storeConfig():
    '''stores the cloud config data in the config object'''
    config.gatewayId = IOT.GatewayId
    config.clientId = IOT.ClientId
    config.clientKey = IOT.ClientKey
    config.save()

def addAsset(module, deviceId, id, name, description, type, profile, style = "Undefined"):
    """add asset"""
    devId = getDeviceId(module, deviceId)
    if len(name) > 140:
        newName = name[:140]
        logging.warning('length of asset name too long, max 140 chars allowed: ' + name + ", truncated to: :" + newName)
        name = newName
    if isinstance(type, bool):
        if type == True:                        # do a small conversion of old plugins that were still using true for actuators and False for sensors.
            type = 'actuator'
        else:
            type = 'sensor'
    _httpLock.acquire()
    try:
        return IOT.addAsset(id, devId, name, description, type, profile, style)
    finally:
        _httpLock.release()

def deleteAsset(module, deviceId, asset):
    """delete the asset"""
    devId = getDeviceId(module, deviceId)
    _httpLock.acquire()
    try:
        return IOT.deleteAsset(devId, asset)
    finally:
        _httpLock.release()

def deleteGatewayAsset(asset):
    """delete the asset
    :type asset: full asset name (including module)
    """
    _httpLock.acquire()
    try:
        return IOT.deleteGatewayAsset(id)
    finally:
        _httpLock.release()

def addGatewayAsset(module, id, name, description, isActuator, assetType, style = "Undefined"):
    """add asset to gateway
    :param module: module name
    :param id: id of asset
    :param name: name/label of asset
    :param description:  description
    :param isActuator: true = actuator
    :param assetType: datatype
    :param style: Undefined, Primary, Secondary, Battery, Config
    """
    id = module + '_' + id
    _httpLock.acquire()
    try:
        IOT.addGatewayAsset(id, name, description, isActuator, assetType, style)
        # not so clean:
        if id in existingGatewayAssets:  # this is for syncing assets: when the asset already exists, remove from the current sync list, so we don't delete it after the sync
            existingGatewayAssets.pop(id)
    finally:
        _httpLock.release()

def addDevice(module, deviceId, name, description, storeHistory = True):
    """add device"""
    devId = getDeviceId(module, deviceId)
    _httpLock.acquire()
    try:
        IOT.addDevice(devId, name, description, storeHistory)
    finally:
        _httpLock.release()

def addDeviceFromTemplate(module, deviceId, templateId):
    """add a device from template"""
    devId = getDeviceId(module, deviceId)
    _httpLock.acquire()
    try:
        return IOT.addDeviceFromTemplate(devId, templateId, None)
    finally:
        _httpLock.release()

def getDevices():
    """get all the devices listed for this gateway as a json structure."""
    _httpLock.acquire()
    try:
        gateway = IOT.getGateway(True)
        if gateway:
            return gateway['devices']
        return []
    finally:
        _httpLock.release()


def getGateway():
    """get the gateway details and all the devices listed for this gateway as a json structure."""
    _httpLock.acquire()
    try:
        return IOT.getGateway(True)
    finally:
        _httpLock.release()

def deviceExists(module, deviceId):
    """check if device exists"""
    devId = getDeviceId(module, deviceId)
    _httpLock.acquire()
    try:
        return IOT.deviceExists(devId)
    finally:
        _httpLock.release()

def deleteDevice(module, deviceId):
    """delete device"""
    devId = getDeviceId(module, deviceId)
    _httpLock.acquire()
    try:
        return IOT.deleteDevice(devId)
    finally:
        _httpLock.release()

def deleteDeviceFullName(name):
    """delete device. Only use this if you know the full name (module + deviceId) of the device
    and it's internal structure. In other words, if you have an id (name) that came directly from the cloud
    """
    _httpLock.acquire()
    try:
        return IOT.deleteDevice(name)
    finally:
        _httpLock.release()

def getAssetState(module, deviceId, assetId):
    """get value of asset (note: does not include the timestamp when the value was recorded)"""
    devId = getDeviceId(module, deviceId)
    _httpLock.acquire()
    try:
        return valueCache.getValue(assetId, devId)
    finally:
        _httpLock.release()

def _sendData(url, asset, method):
    """secure manner for calling low level 'sendData to IOT connection"""
    _httpLock.acquire()
    try:
        IOT._sendData(url, str(asset), IOT._buildHeaders(), 'PUT')
    finally:
        _httpLock.release()


def send(module, device, asset, value):
    '''send value to the cloud
    thread save: only 1 thread can send at a time'''
    if device:                                                      # could be that there is no device: for gateway assets.
        device = getDeviceId(module, device)
    else:
        asset = getDeviceId(module, asset)
    _mqttLock.acquire()
    try:
        IOT.send(value, device, asset)
    finally:
        _mqttLock.release()
    if _sensorCallback:
        _sensorCallback(module, device, asset, value)

def sendCommand(gatewayId, module, device, asset, value):
    '''send value to the cloud
        thread save: only 1 thread can send at a time'''
    if device:  # could be that there is no device: for gateway assets.
        device = getDeviceId(module, device)
    else:
        asset = getDeviceId(module, asset)
    _mqttLock.acquire()
    try:
        IOT.sendCommand(value, gatewayId, device, asset)
    finally:
        _mqttLock.release()

def getModuleName(value):
    """extract the module name out of the string param."""
    return value[:value.find('_')]

def stripDeviceId(value):
    """extract the module name out of the string param."""
    return value[value.find('_') + 1:]

def getDeviceId(module, device):
    return module + '_' + str(device)

def getUniqueName(module, device, asset):
    """renders a unique name for the specified asset by using '_' to combine all the fractions."""
    return module + "_" + str(device) + "_" + str(asset)
