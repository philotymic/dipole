#import ipdb
import sys, os
import prctl, signal
import time

sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole

@libdipole.exportclass
class Argv:
    def sayHello(self):
        print("Hello World!")
        return "Hello, World!"
    
if __name__ == "__main__":
    if 1:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM

    dpl_server = libdipole.mod_libdipole.DipoleServer()
    dpl_event_handler = libdipole.BackendEventHandler(libdipole.port_assignment_handler, sys.argv[1])
    dpl_server.set_event_handler(dpl_event_handler)
    dispatcher = libdipole.Dispatcher(dpl_server)
    dpl_event_handler.dispatcher = dispatcher
    
    print("adding object Argv")
    dispatcher.add_object("Argv", Argv())

    dpl_server.run_listener(0)
