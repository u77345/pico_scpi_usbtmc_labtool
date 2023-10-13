import pyvisa
import time
from pyvisa import ResourceManager, constants
import sys, re, traceback, logging
import time

rm = pyvisa.ResourceManager('@ivi') 

logging.basicConfig(level=logging.ERROR)

def handle_event(resource, event, user_handle):
    print(f"Handled event {event.event_type} on {resource}")
    #resource.called = True
    stb = instr.read_stb()
    instr.write("*CLS")

with rm.open_resource("USB0::0xCAFE::0x4000::E660C06213865126::INSTR") as instr:

    print('Opened\n')
    
    instr.called = False

    event_type = constants.EventType.service_request
    event_mech = constants.EventMechanism.handler
    wrapped = instr.wrap_handler(handle_event)
    user_handle = instr.install_handler(event_type, wrapped, 42)
    instr.enable_event(event_type, event_mech, None)
    
    instr.write("STAT:OPER:DIGI:INP:NTR 4\n")
    instr.write("STAT:OPER:DIGI:INP:ENAB 4\n")
    instr.write("STAT:OPER:ENAB 1\n")

    instr.write("*CLS")
    instr.write("*SRE 128") #leaving Bit6 MSS - off
    
    print('Done setting up')
       
    cv = 0
    
    try:
        while not instr.called:
            time.sleep(0.01)
                
    except: 
        instr.close()
        logging.exception("While looping")

try:
    instr.disable_event(event_type, event_mech)
except:
    print('err while disabling event')
try:
    instr.uninstall_handler(event_type, wrapped, user_handle)
except:
    print('err while disabling event')

instr.close()
print("Done.")