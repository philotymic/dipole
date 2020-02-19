#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

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

    xfn = sys.argv[1]
    o_server = libdipole.ObjectServer()
    print("adding object Argv")
    o_server.add_object("Argv", Argv())

    o_server_l = websockets.serve(o_server.message_loop, 'localhost', 0)
    asyncio.get_event_loop().run_until_complete(o_server_l)
    assigned_port = libdipole.autoport.find_ws_port(o_server_l)
    libdipole.__save_assigned_port(assigned_port, xfn)
    asyncio.get_event_loop().run_forever()
