#!/usr/bin/python3

#    EPICS SCPI Control Plane Integration -- Access SCPI devices.
#    Copyright (C) 2022 Florin Boariu and Matthias Roessle.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import pyvisa
import logging

from os import environ as env

class PropertyBranch(object):
    '''
    The SCPI protocol is in many details a hierachical
    one -- commands are being built by extending on a base string
    with sub-branches. For instance:

      - `FUNC <name>` enables a specific function, but
        `FUNC:<name> <param>` sets a specific parameter
         of that function.

      - `BURST:STATE` sets the burst state `BURST:NCYCLES` sets
        the number of burst cycles, etc.

    This object takes any parameter that doesn't begin with an underscore
    and interprets it as a command to send to the device on top of the base
    command that it was initiated with. For instance:
    ```
       p = PropertyBranch(kdev, 'burst')
       p.state = "off"
    ```

    This would return the result of the `"BURST:STATE OFF" command.
    Any strings sent are converted to upper case. Any boolean parameters
    (True/False) are converted to "ON" / "OFF".

    In returning values, the class tries first to convert "ON"/"OFF" to
    boolean, than any integer values in might encounter, then floating
    points. If all fail, a regular Python string is returned.

    The specific functions `get()` and `set()` act directly on the root
    command, e.g. this would result in setting the function "FUNC SIN",
    then requesting the function name again (`FUNC?`):
    ```
       p = PropertyBranch(kdev, 'func`)
       p.set("sin")
       p.get() ## --> 'SIN'
    ```

    The functions `enable()` and `disable()` are shortcuts for `set("ON")`
    and `set("OFF")`, respectively.

    '''

    def __init__(self, kdev, cmdroot, nxerror=None):
        '''
        Parameters:
          - `kdev`: The SCPI device to use. We defer all
            communication to that device.
          - `cmdroot`: The base string for the command, without
            the trailing colon (e.g. `BURST` or `FUNC`).
        '''

        # check if the attribute exists, raise an nxerror otherwise
        if nxerror:
            try:
                kdev.query(cmdroot+"?")
            except pyvisa.VisaIOError:
                raise nxerror
        
        self.cmdroot = cmdroot
        self.kdev    = kdev
        self.__propcache = {}


    def query(self, subcmd):
        val = self.kdev.query(self.cmdroot+subcmd)

        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val
    

    def __call__(self, *args, sep=', '):
        if len(args) == 0:
            return self.query("?")

        if len(args) == 1:
            val = args[0]
        else:
            val = sep.join(args)
            
        if type(val) == bool:
            val = "ON" if val else "OFF"
            
        cmd = self.cmdroot+" %s" % str(val)
        
        ret = self.kdev.write(cmd)
        if ret != len(cmd)+1:
            raise IOError("Error writing: {cmd} (sent %d bytes, "
                          "should be %d)" % (ret, len(cmd)))
        

    def __getattr__(self, name):
        nxerror = None
        prop = self.__propcache.setdefault(name,
                                           PropertyBranch(self.kdev, "%s:%s" % \
                                                          (self.cmdroot, name), nxerror))
        return prop


class MagicScpi(object):
                     

    def __init__(self, dev=None, setup={}, timeout=3.0):
        '''
        Connects via TCP/IP to the waveform generator behind IP address `IP`.
        Default is `None`, which means the address will be read from the
        `MAGICSCPI_ADDRESS` environment variable.

        Parameters:
          - `ip`: The IP address to connect to. If none is specified, it is
            taken from the `MAGICSCPI_ADDRESS` environment variable.

          - `setup`: A dictionary containing additional setup. Keys are the
            parameter name (e.g. 'VOLT:UNIT'), values are the value ('Vpp').

          - `timeout`: Timeout in seconds
        '''

        try:
            self.port = dev or env['MAGICSCPI_ADDRESS']
        except KeyError:
            logging.error("No SCPI port specified and no MAGICSCPI_ADDRESS available")
            raise
        
        self.dev = pyvisa.ResourceManager('@py').open_resource(self.port)
        self.dev.read_termination = '\n'
        self.dev.write_termination = '\n'
        self.dev.timeout = int(timeout*1000)

        self.__propcache = {}

        logging.debug("Device open: %s" % self.port)
        logging.debug("Device ID: %s" % self.id())

    def write(self, s):
        '''
        Wrapper for the `write()` command that does some
        error hanlding.
        '''
        ret = self.dev.write(s)
        if ret != len(s)+1:
            raise IOError("Wrote %d bytes, whould have been %d (%s)" %\
                          (ret, len(s), str(s)))

    
    def query(self, q):
        '''
        Wrapper for the `query()` command that does some
        error hanlding.
        '''
        return self.dev.query(q)


    def id(self):
        '''
        Return stuff.
        '''
        return self.query('*IDN?')

    
    def __getattr__(self, name):
        nxerror = None
        prop = self.__propcache.setdefault(name,
                                           PropertyBranch(self.dev, "%s" % name,
                                                          nxerror))
        return prop



class MockPropertyBranch(object):
    '''
    Accepts any property.
    '''
    def __init__(self, *args, **kwargs):
        self._val = 3.14
        self.__pcache = {}

    def __call__(self, *args):
        if len(args) == 0:
            return self._val
        else:
            self._val = val

    def enable(self):
        self.set(1.0)

    def disable(self):
        self.set(0.0)

    def __getattr__(self, name):
        return self.__pcache.setdefault(name, MockPropertyBranch())


class MockScpi(object):
    '''
    Mocking class for Keith3390. Has some defauls for
    the explicit attributes (output, waveform, ...)
    '''

    def __init__(self, *args, **kwargs):
        self.__pcache = {}

    def id():
        return "Mock SCPI Device"

    def __getattr__(self, name):
        return self.__pcache.setdefault(name, MockPropertyBranch())
    
