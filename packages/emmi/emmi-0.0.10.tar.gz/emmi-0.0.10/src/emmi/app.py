#!/usr/bin/python3

import asyncio, time, logging
import logging

'''
Base modules for easier development of EPICS
'''

def cfgFromEnv(envPrefix, envVars, splitChar='_'):
    '''
    Returns a configuration dictionary (possibly nested) from
    all environment variables that math a specific prefix.
    Splits variable names at `splitChar` and adds a new dictionary
    level for each split.
    '''

    if not envPrefix:
        return {}

    env = {}

    for k,v in envVars.items():
        if not k.startswith(envPrefix):
            continue
        
        parts = k.split(splitChar)

        current_dict = env
        for p in parts[:-1]:
            current_dict = current_dict.setdefault(p, {})
        current_dict[parts[-1]] = v

    return env.get(envPrefix, {})

    

def test_cfgFromEnv():
    env = {
        'foo_var': 'foo_var',
        'foo_car': 'foo_car',
        'foo_bar_car': 'foo_bar_car',
        'bar_car': 'bar_car'
    }

    conf = cfgFromEnv("foo", env)
    
    assert len(conf) == 3
    assert len(conf['bar']) == 1
    assert conf['car'] == 'foo_car'
    assert conf['var'] == 'foo_var'
               

class IocApplication(object):
    '''
    Main application model for EPICS-SCPI gateway.
    '''
    
    def __init__(self, prefix=None, argsDict=None, envDict=None, confDict=None, envPrefix='EMMIIOC'):
        '''
        Initialize application with EPICS prefix `prefix`.
        If the prefix is not specified, an attempt is made to retrieve
        a prefix from the environment variable in `envname`.
        If `epicsDict` is not `None`, it is used as a configuration
        dictionary (usually initialized from a Yaml file)
        '''
        
        from os import environ

        self.conf = {}
        
        for d in [confDict, argsDict, envDict or cfgFromEnv(envPrefix, environ)]:
            if d is not None:
                self.conf.update(d)
                
        if prefix is not None:
            self.conf.setdefault('epics', {}).setdefault('prefix', prefix)
        
        self.initIoc(self.conf['epics'])
        
        logging.info("Using EPICS device prefix: %s" % self.epicsPrefix)


    def testMode(self):
        return self.conf['epics']['prefix'].endswith('TEST')        
        

    def initIoc(self, epicsConf):
        # the epics part
        from softioc import softioc, builder, asyncio_dispatcher

        self.epicsPrefix = epicsConf['prefix']
        self.softioc = softioc
        self.iocBuilder = builder
        self.iocDispatch = asyncio_dispatcher.AsyncioDispatcher()
        self.iocBuilder.SetDeviceName(self.epicsPrefix)

        # the device property part
        self.pv = {
            'heartbeat': self.iocBuilder.aIn('heartbeat', initial_value=1)
        }


    def run(self):
        '''
        Starts IOC thread and runs main application loop (which essentially does nothing).
        Does not return.
        '''

        self.iocBuilder.LoadDatabase()
        self.softioc.iocInit(self.iocDispatch)

        counter = 0
        while True:
            self.pv['heartbeat'].set(counter)
            counter += 1
            time.sleep(1.0)
            
        self.softioc.exit()
