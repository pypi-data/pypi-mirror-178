#!/usr/bin/python3

import time
import asyncio

import logging

'''
Validators are a concept that allow us to filter, translate and validate
data (values) from one ecosystem (e.g. EPICS) into another (e.g. SCIP).
Each validator needs to have at least:

  - one setup() function which receives named arguments with the necessary
    data for validating; arguments names will be directly accepted/visible
    in the YAML files, so choose wisely.

  - one __getitem__() function which returns the translated value, or
    raises ValueError if the value is out of the permissible conditions.
'''
        
class MappingValidator(object):
    '''
    Translates a value from one set to another
    '''
    def __init__(self, values={}):
        self.setup(values)

    def setup(self, values={}):
        self.trmap = values

    def __getitem__(self, val):
        try:
            #print ("Mapping: %r -> %r (%r)" % (val, self.trmap.get(val), self.trmap))
            return self.trmap.get(val)
        except KeyError:
            raise ValueError("%r: invalid value" % val)


class SetValidator(object):
    '''
    Accepts only objects form a specific set.
    '''
    def __init__(self, **kwargs):
        self.setup(**kwargs)

    def setup(self, values=[]):
        self.vset = values

    def __getitem__(self, val):
        if val in self.vset:
            return val
        else:
            raise ValueError("%r: value not in set %r" % (val, self.vset))


class BoundaryValidator(object):
    '''
    Accepts only values within specified boundaries
    '''
    def __init__(self, **kwargs):
        self.setup(kwargs)

    def setup(self, limits=[None, None], inclusive=[True, True], invert=False):
        self.lim = limits
        self.incl = inclusive
        self.inv = invert

    def __getitem__(self, val):
        err = ValueError("%r: outside of range" % val)
        if ((self.lim[0] is not None) and (self.inc[0] and val < self.lim[0])) == (not invert):
            raise err
        if ((self.lim[1] is not None) and (self.inc[1] and val > self.lim[1])) == (not invert):
            raise err
        if ((self.lim[0] is not None) and (not self.inc[0] and val <= self.lim[0])) == (not invert):
            raise err
        if ((self.lim[1] is not None) and (not self.inc[1] and val >= self.lim[1])) == (not invert):
            raise err
        return val

    
class SliceValidator(object):
    '''
    Returns only specified slice of an (iterable/indexable) value.
    '''
    def __init__(self, **kwargs):
        self.setup(**kwargs)
        
    def setup(self, start=None, stop=None, step=None):
        self.sobj = slice(start, stop, step)

    def __getitem__(self, val):
        return val[self.sobj]

    
class IdentityValidator(object):
    ''' Lets everything through '''

    def setup(self):
        pass
    
    def __getitem__(self, val):
        return val
    

class MockMotor(object):
    '''
    The simplest of the simplest motors: can only move, report position and stop.
    '''

    def __init__(self, *args, **kwargs):
        self.mock_timeslice = kwargs.get('mock_timeslice', 5.0)
        self.start = 0.0
        self.target = 0.0
        self.tstamp = time.time()
        self.goto(0.0)
    
    def where(self):
        '''
        Returns current position -- that is the position that we'd be currently
        having if we'd wanted to go from "current" towards "target" within
        the timeslice "mock_timeslice"
        '''
        tdelta = (time.time()-self.tstamp)
        if tdelta > self.mock_timeslice:
            tdelta = self.mock_timeslice
        dist = self.target-self.start
        return self.start + dist * (tdelta/self.mock_timeslice)

    def goto(self, val):
        '''
        Sends command to move to position (doesn't wait)
        '''
        self.start = self.where()
        self.target = val
        self.tstamp = time.time()

    def stop(self):
        '''
        Sends command to stop (doesn't wait). Technically, we'll be still
        in state "moving" for a while after this, but we'd be moving towards the position
        we're already onto.
        '''
        if self.moves():
            self.goto(self.where())

    def moves(self):
        '''
        Returns True if the motor moves. We fake this by testing whether
        we're still within the "timeslice". This has the added benefit
        that sometimes moves() returns False right away (i.e. if we weren't
        moving in the first place), and sometimes still returns False
        for a considerate amount of time (i.e. until the end of the current
        slice) if we were moving and just received a stop() command.
        '''
        return (time.time()-self.tstamp) < self.mock_timeslice

    def clear(self):
        '''
        Clears all outstanding error flags (they may pop up again).
        '''
        pass
    

class MotorEngine(object):
    '''
    Generic motor engine class. Essentially cycles through the states
    as it should, and serves the most basic properties `position` and
    `position_relative` correctly. It's based on generic True/False
    conditional procedures to decide when to switch.

    In its default incarnation, the conditionals are just generic waiting
    functions (1 second for anything), so it can be used as a mock-up for
    unit testing. But if you replace the conditionals by things that do
    "real stuff", it's actually usable for production.
    '''
    
    def __init__(self, motor=None):
        
        self.__motor = motor or MockMotor()

        # current state
        self.__state = "INIT"

        # Scheduled absolute or relative position change.
        # We move by storing the new positional values here first,
        # then sending them on their way when we're IDLE.
        self.__scheduled_goto = None
        self.__scheduled_moveby = None

        # Current errors list
        self.errors = []        

        # mock-up position setter 
        self.hardware_where  = self.__motor.where       
        self.hardware_ready  = lambda: True
        self.hardware_goto   = self.__motor.goto
        self.hardware_moveby = None
        self.hardware_brake  = self.__motor.stop
        self.hardware_moves  = self.__motor.moves
        self.hardware_clear  = self.__motor.clear


    def __clear_goto(self):
        self.__scheduled_goto = None
        self.__scheduled_moveby = None


    def state_enter(self, state):
        '''
        This is called exactly once, at the beginning, for every
        state that is newly entered. Returns the state string,
        for convenience.
        '''
        logging.info ("State: %s -> %s" % (self.__state, state))
        if state == "STOP":
            self.__clear_goto()
            if self.hardware_moves():
                self.hardware_brake()
        elif state == "BUSY":
            if self.__scheduled_moveby is not None:
                logging.info("BUSY state: relative move scheduled by %r" % self.__scheduled_moveby)
                if self.hardware_moveby:
                    self.hardware_moveby(self.__scheduled_moveby)
                else:
                    self.hardware_goto(self.hardware_where()+self.__scheduled_moveby)
            elif self.__scheduled_goto is not None:
                logging.info("BUSY state: absolute move scheduled to %r" % self.__scheduled_goto)
                self.hardware_goto(self.__scheduled_goto)
            self.__clear_goto()
        elif state == "IDLE":
            self.hardware_clear()
            self.errors = []
        else:
            pass
        return state
             

    ## State procedures -- return the new state they need to switch to.
    ## We're essentially delegating everything to __generic_state_proc().
    def state_proc(self, state):

        # These are the states we can advance to from here
        advances = {
            'INIT': { 'IDLE':  lambda: self.hardware_ready() },
            'IDLE': { 'STOP':  lambda: len(self.errors) > 0,
                      'BUSY':  lambda: self.__scheduled_goto is not None or \
                                       self.__scheduled_moveby is not None},
            'BUSY': { 'STOP':  lambda: len(self.errors) > 0 or not self.hardware_moves() },
            'STOP': { 'ERROR': lambda: len(self.errors) > 0 and not self.hardware_moves(),
                      'IDLE':  lambda: len(self.errors) == 0 and not self.hardware_moves() },
            'ERROR': { 'IDLE': lambda: len(self.errors) == 0 },
            'FAIL': {}
        }

        try:
            adv = advances[state]
        except KeyError as e:
            # BUSY needs to get some extra treatment because it can be extended
            if state.startswith('BUSY'):
                adv = advances['BUSY']

        # execute current state proc
        try:
            for k,v in adv.items():
                #print ("%s/Testing for %s: %r" % (state, k, v))
                if v():
                    return self.state_enter(k)
        except Exception as e:
            logging.error ("Unexpected exception in state %s:" % state, str(e))
            return "FAIL"

        return state
    
    
    # Current position -- getter reads out the hardware, setter
    # is a bit more complicated because we have to acknowledge
    # the current state (i.e. can't just override current states).
    @property
    def position(self):
        return self.hardware_where()

    @position.setter
    def position(self, val):
        if self.state == "IDLE":
            self.__scheduled_goto = val
        trig = self.state

             
    # Increment/decrement position by relative values -- the getter returns
    # 0 as soon as the scheduled move has been triggered, the setter just
    # sends the command / schedules the move.
    @property
    def position_relative(self):
        return self.__scheduled_moveby or 0
    
    @position_relative.setter
    def position_relative(self, val):
        if self.state == "IDLE":
            self.__scheduled_moveby = val
        trig = self.state
        

    def leave_ERROR(self, new_state):
        '''
        The only way we can leave ERROR is by clearing/going to IDLE
        '''
        if new_state == "IDLE":
             self.errors = []
             return self.state_enter("IDLE")
        return "ERROR"
             

    def leave_BUSY(self, new_state):
        '''
        The only way we can leave BUSY is by issuing a STOP.
        We accept that for `new_state` either as being STOP
        or ERROR.
        '''
        logging.info ("Leaving BUSY:", new_state)
        if new_state in [ "STOP", "ERROR" ]:
             return self.state_enter("STOP")
        return "BUSY"


    @property
    def state(self):
        self.__state = self.state_proc(self.__state)
        return self.__state
             
    @state.setter
    def state(self, new_state):
        '''
        This is only an API point -- i.e. for external use, not
        internal. There are only specific combinations of
        "current state" / "end state" that the user is allowed
        to perform. Everything else we ignore.
        '''
        if self.__state == 'ERROR':
            self.__state = self.leave_ERROR(new_state)
        elif self.__state.startswith("BUSY"):
            self.__state = self.leave_BUSY(new_state)


class PropertySetter(object):
    '''
    Wrapper that sets a property -- we need this because
    we want to build most of our API based on properties
    (insted of callable setter functions), but at several
    points in the involved APIs (softioc.Builder, for instance)
    callables are required.
    '''

    def __init__(self, name, obj=None, prop=None, proc=None, validator=IdentityValidator()):
        self.name = name
        self.setter_proc = proc
        self.target_obj = obj
        self.prop_name = prop
        self.validator = validator
        self.validation_failed = False

    async def __call__(self, value):
        try:
            valid = self.validator[value]
            self.validation_failed = False
            if self.setter_proc:
                try:
                    await self.setter_proc(valid)
                except TypeError as t:
                    self.setter_proc(valid)
            else:
                setattr(self.target_obj, self.prop_name, valid)
        except ValueError as e:
            if not self.validation_failed:
                logging.error("Failed to set %s: %r" % (self.name, e))
                self.validation_failed = True


class PropertyUpdater(object):
    '''
    A callable object which loops indefinitely reading out a property via `getter`
    and publishing it on EPICS process-variable `pv`. The waiting
    time on every loop run is such that a full run is as close
    as possible to `period`.
    '''
    
    def __init__(self, name, pv, period, getter=None, obj=None, prop=None, validator=IdentityValidator()):
        self.name   = name
        self.pv     = pv
        self.period = period
        self.getter = getter or self.get_from_property
        self.validator = validator
        self.obj = obj
        self.prop = prop

    def get_from_property(self):
        return getattr(self.obj, self.prop)

    def set_period(self, val):
        self.period = val

    async def __call__(self):
        logging.debug("%s: Updater running for PV %r" % (self.name, self.pv))
        available = True
        while True:
            try:
                tstart = time.time()
                val = self.getter()
                self.pv.set(self.validator[val])

                if not available:
                    logging.info("%s: has become available again" % self.name)
                    available = True
                
            except Exception as e:
                # We're not going to exit on PV setting problems (may be
                # intermittent), but at least we'll get loud about it.
                if available:
                    logging.error("%s: property became unavailable, reason: %r" % (self.name, e))
                    logging.error("%s: further errors will be silenced" % self.name)
                available = False
            except e:
                logging.error("%s: unknown exception %r" % e)
                raise

            tdiff = time.time()-tstart
            await asyncio.sleep(self.period - tdiff)


class MotorConnector(object):
    '''
    Implements a simple EPICS motor record, with a small subset of the
    [EPICS motor record](https://epics.anl.gov/bcda/synApps/motor/R7-1/motorRecord.html)
    variables. Relies on a motor inteface as described by `MotorEngine`, i.e.
    a class with the following properties:

      - `position`: returns the current motor values, respectively moves
        to the specified relative value

      - `position_relative`: facilitates a movement relative to the current
        position

      - `state`: a string that begins with one of the following:
    
          - "INIT" (preparing to take commands)
    
          - "IDLE" (not moving, ready to take commands)
    
          - "BUSY" (not able to accept commands, most likely already moving)
    
          - "ERROR" (stopped, reached a situation which requires external action)

          - "STOP" (stopping)
    
          - "FAIL" (unefined state, best effort to be stopped, unrecoverable error)
    
        The state string is intentionally checked only for its beginning part.
        States may be explicitly extended by appending information to strings,
        e.g. "BUSY.TRACKING" or "BUSY.HOMING" to distinguish different flavors
        of states. `SimpleMotor` will not react to anything beyond the five
        1st-level state information, but other software layers may.

    This class needs to be used with a
    [pythonSoftIOC](https://dls-controls.github.io/pythonSoftIOC)
    compatible EPICS IOC Python API. It uses `asyncio` for all asynchronous
    work.

    It implements the EPICS motor record variables VAL, RBV, RVL, HOMF/HOMB,
    STOP.

    FIXME: need to add support for supplementary actions / properties / signals
    (e.g. extend by additional "BUSY" states, or read/write specific properties
    like limits, force probe thresholds etc).
    '''    

    def __init__(self, motor_prefix, motor_engine, ioc_dispatcher,
                 poll_period=0.1, separator="_", style="simple"):
        '''
        Initializes the IOC variables. Parameters:
        
          - `motor_prefix`: a string to prepend to the motor variables.
        
          - `motor_engine`: the `MotorEngine` object we'll be talking to.
        
          - `ioc_dispatcher`: a pythonSoftIOC asyncio dispatcher compatible
            instance (typically a `softioc.asyncio_dispatcher.AsyncioDispatcher()`)
        '''

        self.pollPeriod = poll_period

        #from softioc import builder as ioc_builder

        # SPEC needs the following:
        #
        # Can be ignored / business of the controller?
        #  o ACCL: acceleration time in seconds (0.0)
        #  o BDST: backlash distance egu (0)
        #  o BVAL: backlash velocity egu/s (0)
        #  o VBAS: base velocity (minimum velocity?) egu/s (0)
        #  o ERES: encoder step size egu (0)
        #  o MRES: motor step size egu (0)
        #
        # Calibration fields and coordinate system transformations:
        #  - SET: set/use switch for calibration fields (0: use, 1: set)
        #  - FOFF: offset freeze switch -- is the user prevented from
        #          writing the offset?
        #  - OFF: user offset egu
        #  + DIR: user direction        
        #  - RRBV: raw readback value
        #  - RVAL: raw desired value        
        #
        # Unclear:
        #  o UEIP: use encoder if present (always 1?)
        #  o VELO: velocity egu/s (set to 0?)
        #
        # Need to have / already have:
        #  o STOP: stop
        #  o VAL: user desired value
        #  - SPMG: stop/pause/move/go -- complicated beast
        #    - Stop: same as STOP?        
        #
        # Nice to have, but not part of the EDA Motor Model:
        #  + DHLM: dial high-limit
        #  + DLLM: dial low-limit
        #  + HLS: at high-limit switch
        #  + LLS: at low-limit switch        
        #  o DMOV: done moving to value
        #
        # Unknown:
        #  + DISP: disable (turn off motor/unusable)        
        #
        # Nice to have, not needed by SPEC:
        #  o EGU: engineering unit names
        #  - RLV: relative-move value: when changed, changes VAL,
        #    then resets itself to 0
        #  
        
        self.engine = motor_engine

        # VAL/RBV
        self.con_pos = PropertyConnector(ioc_dispatcher,
                                         prefix=motor_prefix+separator,
                                         access=(motor_engine, "position"),
                                         signal={ 'poll_period': poll_period },
                                         kind="analog")

        # STATEVAL/RBV
        self.con_state = PropertyConnector(ioc_dispatcher,
                                           prefix=motor_prefix+separator+"STATE",
                                           access=(motor_engine, "state"),
                                           signal={ 'poll_period': poll_period },
                                           kind="strings",
                                           validator={ 'values': [
                                               'INIT', 'IDLE', 'BUSY', 'STOP', 'ERROR', 'FATAL'
                                           ]})

        # STOP
        self.con_stop = ActorConnector(var=motor_prefix+separator+"STOP",
                                       access=self.conExecStop,
                                       kind="values",
                                       validator={'values': [0, 1]})

        if style == "spec":

            # lots of variables expected by spec but which we don't really serve
            self.con_constants = [
                SignalConnector(ioc_dispatcher,
                                var=motor_prefix+separator+suffix,
                                access=lambda: value,
                                kind=kind,
                                poll_period=10.0)
                for suffix,kind,value in [ ("ACCL", "analog", 0),
                                           ("BDST", "analog", 0),
                                           ("BVAL", "analog", 0),
                                           ("VBAS", "analog", 0),
                                           ("ERES", "analog", 0),
                                           ("MRES", "analog", 0),
                                           ("UEIP", "analog", 1),
                                           ("VELO", "analog", 0)]]
            #("EGU",  "text", "mm")] ]

            # DMOV - set to 0 when motor begins moving
            self.con_dmov = SignalConnector(ioc_dispatcher,
                                            var=motor_prefix+separator+"DMOV",
                                            access=lambda: int(self.engine.state == "IDLE"),
                                            kind="integer",
                                            poll_period=self.pollPeriod)

            
            self.con_status = SignalConnector(ioc_dispatcher,
                                              var=motor_prefix+separator+"STATUS",
                                              access=lambda: 0x02 if self.engine.state == "BUSY" else 0x00,
                                              kind="integer",
                                              poll_period=self.pollPeriod)
        
                   
        ## Enable 'HOMF' command
        #self.pv_homf = builder.aOut(axvar+"_HOMF", initial_value=0, always_update=True,
        #                            on_update=TriggerAndStatus(lambda: axobj.homing = True,
        #lambda: axobj.homing)]

        #class rel_add(object):
        #    def __init__(self, pos_prop):
        #        self.pos_prop = pos_prop
        #        self.my_pv = None
        #    def __call__(self, value):
        #        self.pos_prop += val
        #        if self.my_pv:
        #            self.my_pv.set(0)
        #           
        #self.rel_mover = rel_add(motor_engine.position)
        #
        #self.pv_relpos = ActorConnector(var=motor_prefix+"_RLV",
        #                                access=self.rel_mover,
        #                                kind='analog',
        #                                validator=None)
        #
        #self.rel_mover = self.pv_relpos

    def conPollDmov(self):
        return int(self.engine.state == "IDLE")

    async def conExecStop(self, val):
        '''
        EPICS motor STOP command: if val==1, it executes the STOP command,
        then it sets VAL to current position and resets itself to 0.
        '''
        if val != 1:
            return

        self.engine.state = "STOP"
        self.con_stop.pv.set(0)
        
        while self.engine.state != "IDLE":
            await asyncio.sleep(self.pollPeriod)
            
        self.con_val.set(self.engine.position)
            
        


from softioc import builder as IocBuilder
        
'''
List of connector kinds we support. "in"/"out" should return the
correct builder function (lambda parameter being the softioc builder
object itself), and "args" is a list of initial arguments for the
builder function. Typically you'd want to set default values,
and/or sizes, and/or data types.
'''
ConnectorKinds = {
    "analog": { "in": IocBuilder.aIn,
                "out": IocBuilder.aOut,
                "create": { "initial_value": 0.0 },
                "to-epics": IdentityValidator(),
                "from-epics": IdentityValidator() },

    "switch": { "in": IocBuilder.boolIn,
                "out": IocBuilder.boolOut,
                "create": { 'ZNAM': 'OFF', 'ONAM': 'ON' },
                "to-epics": MappingValidator(values={"ON": 1, True: 1, 1: 1,
                                                     "OFF": 0, False: 0, 0: 0}),
                "from-epics": MappingValidator(values={1: "ON",
                                                       0: "OFF"}) },

    "strings": { "in": IocBuilder.stringIn,
                 "out": IocBuilder.stringOut,
                 "create": { },
                 "to-epics": SetValidator,
                 "from-epics": SetValidator },

    # untested:
    
    "text":  {  "in": IocBuilder.stringIn,
                "out": IocBuilder.stringOut,
                "create": { },
                "to-epics": SliceValidator(stop=39),
                "from-epics": IdentityValidator() },

    "map": { "in": IocBuilder.stringIn,
             "out": IocBuilder.stringOut,
             "create": { "initial_value": "n/a" },
             "to-epics": MappingValidator,
             "from-epics": MappingValidator },

    "values": { "in": IocBuilder.longIn,
                "out": IocBuilder.longOut,
                "create": { "initial_value": 0 },
                "to-epics": SetValidator,
                "from-epics": SetValidator },

    "integer": { "in": IocBuilder.longIn,
                 "out": IocBuilder.longOut,
                 "create": { "initial_value": 0 },
                 "to-epics": IdentityValidator(),
                 "from-epics": IdentityValidator() },
}
    
        
class SignalConnector(object):
    '''
    Connects a sensoric signal (i.e. a reading of a measurement) to an
    EPICS PV. The data is retrieved from either a Python property or
    from a getter function.
    '''

    def __init__(self, ioc_dispatch, var=None, access=None, kind="analog",
                 validator=None, poll_period=1.0):
        '''
        Parameters:
          - `ioc_dispatch`: dipatcher to use

          - `name`: String, will be used throughout the application
            for referencing and recognition (e.g. error messages)
        
          - `var`: PV name to use; defaults to `name`.
        
          - `access`: Callable or (obj, propname) tuple of a Python
            property to set or get data from.

          - `kind`: one of the `eda.ConnectorKinds` keys

          - `poll_period`: poll period for the data to publish (i.e.
            calling of `access`)

          - `validator`: If not `None`, the validator of the property
            updater will be initialized using this dictionary of values.
        '''
        k = ConnectorKinds[kind]

        self.pv = k["in"](var, **(k["create"]))

        access_dict = { "getter": access } if hasattr(access, "__call__") \
            else { "obj": access[0], "prop": access[1] }

        # sometimes the validator in ConnectorKinds is an explicit
        # instance (which we can use right away); sometimes it's just
        # a class type, which we have to instantiate first
        valdtr = k['to-epics'](**(validator or {})) if type(k['to-epics']) == type \
            else k['to-epics']

        getter = PropertyUpdater(name=var, validator=valdtr,
                                 pv=self.pv, period=poll_period,
                                 **access_dict)
        
        ioc_dispatch(getter)

        logging.debug("%s: '%s' sensor, access %r" % (var, kind, access))
        

class ActorConnector(object):
    '''
    Connects an action signal (i.e. button, knob, setting etc) to an EPICS PV.
    '''
    
    def __init__(self, var=None, access=None, kind="analog", validator=None):
        '''
        Parameters:
          - `var`: PV name to use
        
          - `access`: Either a callable for reading/setting data,
            or (obj, propname) tuple of a Python
            property to set or get data from.

          - `kind`: one of the `eda.ConnectorKinds` keys

          - `validator`: property dictionary for kind-specific validator
            configuration
        '''
        
        k = ConnectorKinds[kind]

        access_args = {'proc': access} if hasattr(access, "__call__") \
            else { 'obj': access[0], 'prop': access[1] }

        # sometimes the validator in ConnectorKinds is an explicit
        # instance (which we can use right away); sometimes it's just
        # a class type, which we have to instantiate first
        valdtr = k['from-epics'](**(validator or {})) if type(k['from-epics']) == type \
            else k['from-epics']        
        
        setter = PropertySetter(name=var, validator=valdtr, **access_args)

        if validator:
            setter.validator.setup(**validator)
        
        self.pv = k["out"](var, always_update=True, on_update=setter, **(k["create"]))
        logging.debug("%s: '%s' actor, access %r" % (var, kind, access))
    
        
class PropertyConnector(object):
    '''
    Conenctor for a get/set type of property; uses `eda.SignalConnector`
    and `eda.ActorConnector` under the hood to export two PVs, one for
    setting, one for reading back the property. By default the variable
    names end in "VAL" (for setting), respectively "RBV" (for reading).

    A `sync()` method is available to programatically set the
    "VAL" part to its current readback value "RBV".
    '''

    def __init__(self, ioc_dispatcher, prefix=None, access=None,
                 kind="analog", validator=None, signal={}, actor={}):
        '''
        Parameters:
          - `ioc_dispatcher`: connection to pythonSoftIOC to use.

          - `prefix`: PV prefix, will be prepended to the variable names. By
            default the variable names end in "VAL" (for setting), respectively
            "RBV" (for reading), but they can be overridden by using the `sensor`
            and `actor` parameters. Defaults to `name`.

          - `access`: Access method or (obj, prop) to use for both reading and
            writing. If there are different methods for reading and writing,
            this should be set to `None` and the appropriate methods should
            be set via the `sensor` and `actor` dictionaries.

          - `kind`: The kind of signal to use; must be one of the `eda.ConnectorKinds`
            items.
        
          - `signal`: Dictionary with optional variables to pass on to
            `eda.SignalConnenctor` for the reading part.
        
          - `actor`: Dictionary with optional variables to pass on to
             `eda.ActorConnector` for the setting part.
        '''

        ad = {}
        ad.update(actor)
        ad.setdefault("kind", kind)
        ad.setdefault("access", access)
        ad.setdefault("validator", validator)
        ad.setdefault("var", prefix+"VAL")
        self.val = ActorConnector(**ad)

        sd = {}
        sd.update(signal)
        sd.setdefault("kind", kind)
        sd.setdefault("access", access)
        sd.setdefault("validator", validator)
        sd.setdefault("var", prefix+"RBV")
        self.rbv = SignalConnector(ioc_dispatcher, **sd)

        logging.info ("Registering property: %s" % (prefix))
