from emmi.eda import MotorEngine, MockMotor
import time

def test_engine():
    '''
    Very rudimentary test of the engine, using a Mock motor:
      - Initial state is INIT or IDLE
      - After setting position we're BUSY for a while, then IDLE
      - After setting and stopping we're going back to IDLE
    '''
    
    e = MotorEngine(motor=MockMotor(mock_timeslice=1.0))
    assert e.state in [ "INIT", "IDLE" ]

    # Setting the position.
    # Will need 1 second to move, may or may not need 1 second to stop (?)
    e.position = 3.14
    end = time.time()+2.5
    while time.time() < end:
        time.sleep(0.1)
        assert e.state in [ "BUSY", "IDLE", "STOP" ]

    e.position = 10.0
    assert e.state == "BUSY"
    
    e.state = "STOP"
    assert e.state == "STOP"

    end = time.time()+1.5
    while time.time() < end:
        time.sleep(0.1)
        s = e.state
        
    assert e.state == "IDLE"

    ## Also need to test that setting a position while already
    ## moving results in ignoring the command.
