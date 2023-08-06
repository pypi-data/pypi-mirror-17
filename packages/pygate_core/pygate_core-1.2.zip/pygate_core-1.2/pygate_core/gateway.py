﻿#allows a gateway plugin to manage it's cloud presence.

from pygate_core import cloud


class Gateway(object):
    '''allows a gateway to manage it's cloud presence'''

    def __init__(self, moduleName):
        result = super(Gateway, self).__init__()
        self._moduleName = moduleName
        return result

    def addAsset(self, id, deviceId, name, description, isActuator, assetType, style = "Undefined"):
        """add asset"""
        return cloud.addAsset(self._moduleName, deviceId, id, name, description, isActuator, assetType, style)

    def deleteAsset(self, deviceId, asset):
        cloud.deleteAsset(self._moduleName, deviceId, asset)

    def addGatewayAsset(self, id, name, description, isActuator, assetType, style = "Undefined"):
        cloud.addGatewayAsset(self._moduleName, id, name, description, isActuator, assetType, style)

    def addDevice(self, deviceId, name, description, storeHistory = True):
        """add device"""
        cloud.addDevice(self._moduleName, deviceId, name, description, storeHistory)

    def addDeviceFromTemplate(self, deviceId, templateId):
        """add a device from template"""
        return cloud.addDeviceFromTemplate(self._moduleName, deviceId, templateId)

    def deleteDevice(self, deviceId):
        """delete device"""
        cloud.deleteDevice(self._moduleName, deviceId)

    def send(self, value, deviceId, actuator):
        cloud.send(self._moduleName, deviceId, actuator, value)

    def deviceExists(self, deviceId):
        return cloud.deviceExists(self._moduleName, deviceId)

