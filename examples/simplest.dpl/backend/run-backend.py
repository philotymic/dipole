#import ipdb
import sys, os
import prctl, signal
import time

sys.path.append("/home/asmirnov/dipole/src")
import libdipole

@libdipole.exportclass
class Hello:
    def sayHello(self):
        print "Hello World!"
        return "Hello, World!"

    def sayAloha(self, language):
        print "Aloha"
        #time.sleep(3)
        return language + "Aloha"

def port_assignment_handler(assigned_port):
    xfn_fn = sys.argv[1]
    print "running server at port", assigned_port
    xfn_fd = open(xfn_fn, "w+b")
    print >>xfn_fd, assigned_port
    xfn_fd.close()
    sys.stdout.flush()
        
if __name__ == "__main__":
    if 1:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM

    dpl_server = libdipole.DipoleServer()
    dpl_event_handler = libdipole.BackendEventHandler(port_assignment_handler)
    dpl_server.set_event_handler(dpl_event_handler)
    dispatcher = libdipole.Dispatcher(dpl_server)
    dpl_event_handler.dispatcher = dispatcher
    
    print "adding object Hello"
    dispatcher.add_object("Hello", Hello())

    dpl_server.run_listener(port = 0)
