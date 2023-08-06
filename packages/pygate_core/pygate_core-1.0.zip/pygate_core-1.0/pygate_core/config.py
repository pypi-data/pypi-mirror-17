﻿import logging
from ConfigParser import *
import yaml
import os.path

configs = None                                      #provides access to the configParser object for plug in modules

modules = []                                        #all the names of the plugins that handle devices/asset
processors =[]                                      #all the names of the plugins that handle asset value changes
gatewayId = None                                    # the id of the gateway 
clientId = None                                     #authentication value
clientKey = None                                    #authentication value
apiServer = 'api.smartliving.io'                    #the address of the api server to use
broker = 'broker.smartliving.io'                    #the address of the broker
secure = False

configPath = '../config/'                           # the path to the folder that contains all the configs. Warning: path to logging.config is set in pygate.py
rootConfigFileName = configPath + 'pyGate.config'   # the path and filename of the main config file


def load():
    """Load config data"""
    global configs, modules, processors, gatewayId, clientId,clientKey, apiServer,broker, secure
    configs = ConfigParser()
    if configs.read(rootConfigFileName):
        logging.info("loading " + rootConfigFileName)
        
        if configs.has_option('general', 'modules'):
            modulesStr = configs.get('general', 'modules')
            logging.info("modules: " + str(modulesStr))
            modules = [ x.strip() for x in modulesStr.split(';')]
        if configs.has_option('general', 'processors'):
            processorsStr = configs.get('general', 'processors')
            logging.info("processors: " + str(processorsStr))
            if processorsStr:
                processors = [ x.strip() for x in processorsStr.split(';')]
        if configs.has_option('general', 'gatewayId'):
            gatewayId = configs.get('general', 'gatewayId')
            logging.info("gatewayId: " + gatewayId)
        if configs.has_option('general', 'clientId'):
            clientId = configs.get('general', 'clientId')
            logging.info("clientId: " + clientId)
        if configs.has_option('general', 'clientKey'):
            clientKey = configs.get('general', 'clientKey')
            logging.info("clientKey: " + clientKey)

        if configs.has_option('general', 'api server'):
            apiServer = configs.get('general', 'api server')
            logging.info("api server: " + apiServer)
        if configs.has_option('general', 'broker'):
            broker = configs.get('general', 'broker')
            logging.info("broker: " + broker)
        if configs.has_option('general', 'secure'):
            secure = configs.get('general', 'secure')
            logging.info("secure: " + secure)
    else:
        logging.error('failed to load ' + rootConfigFileName)

def loadConfig(fileName, asJson = False):
    """loads the config file from the correct directory and returns a ConfigParser object that can be used to load
       config data"""
    fileName = os.path.join(configPath, fileName)
    if not os.path.isfile(fileName):
        logging.error('file not found ' + fileName)
        return None
    else:
        if not asJson:
            c = ConfigParser()
            if c.read(fileName):
                logging.info("loading " + fileName)
                return c
            else:
                logging.error('failed to load ' + fileName)
                return None
        else:
            with open(fileName) as json_file:
                logging.info("loading " + fileName)
                json_data = yaml.safe_load(json_file)
                return json_data

def getConfig(section, name, default):
    """return the parameter found in the main configuraion file (pyGate.config) in the specified section, specified
    name. If the section or name is not present, the default value is returned"""
    if configs.has_option(section, name):
        return configs.get(section, name)
    else:
        return default

def save():
    '''
    saves the global config data to the global config file. Called when config params have
    been changed, like the gatewayId
    Will save the entire config object, but will first make certain that 'gatewayId, clientId and clientKey'
    are up to date in the configs object.
    '''
    configs.set('general', 'gatewayId', gatewayId)
    configs.set('general', 'clientId', clientId)
    configs.set('general', 'clientKey', clientKey)
    with open(rootConfigFileName, 'w') as f:
        configs.write(f)
