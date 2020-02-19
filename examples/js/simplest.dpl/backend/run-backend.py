#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

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

    ws_handler = libdipole.WSHandler();
    print("adding object Hello")
    ws_handler.object_server.add_object("Hello", Hello())

    ws_l = websockets.serve(ws_handler.message_loop, 'localhost', 0)
    asyncio.get_event_loop().run_until_complete(ws_l)
    assigned_port = libdipole.autoport.find_ws_port(ws_l)
    libdipole.__save_assigned_port(assigned_port, xfn)
    asyncio.get_event_loop().run_forever()
