#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

#@libdipole.interface
"""
class SomethingHappen:
    def when_something_happen(self, what_happen): pass

class SomethingHappenPrx(SomethingHappen):
    def when_something_happen(self, what_happen):
        call_o = ...
        call_o.call_id = ...
        call_o.object_id = ...
        call_o.method = 'when_something_happen'
        call_o.args = JSON.parse(what_happen)
        self.communicator.do_call(call_o)
        res = self.communicator.wait_for_response(call_o.call_id)
        return res

def monitor_thread():
    i = 0
    while 1:
        SERVER_CB.when_something_happen("hello" + str(i))
        time.sleep(2)

"""

#@libdipole.interface
#class Hello:
#    def sayHello(self): pass
#    def sayAloha(self, language): pass
#    def get_holidays(self): pass
#    
#class HelloI(Hello):
@libdipole.exportclass
class Hello:
    def sayHello(self):
        print("Hello World!")
        return "Hello, World!"

    def sayAloha(self, language):
        print("Aloha")
        #time.sleep(3)
        return language + "Aloha"

    def get_holidays(self):
        print("get_holidays")
        return ["20190101", "20200101"]
    
if __name__ == "__main__":
    if 1:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM
    xfn = sys.argv[1]
    
    dispatcher = libdipole.Dispatcher()
    dpl_server = libdipole.DipoleServer(dispatcher)

    print("adding object Hello")
    dispatcher.add_object("Hello", Hello())

    dpl_server_l = websockets.serve(dpl_server.message_loop, 'localhost', 0)
    asyncio.get_event_loop().run_until_complete(dpl_server_l)
    assigned_port = libdipole.autoport.find_ws_port(dpl_server_l)
    print("assigned_port:", assigned_port)
    libdipole.port_assignment_handler(assigned_port, xfn)
    asyncio.get_event_loop().run_forever()
