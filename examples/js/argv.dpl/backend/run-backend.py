#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

sys.path.append(os.path.join(os.environ['topdir'], "backend", "gen-py"))
import backend

class ArgvI(backend.Argv):
    async def sayHello(self):
        print("Hello World!")
        return "Hello, World!"
    
if __name__ == "__main__":
    if 1:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM

    xfn = sys.argv[1]

    object_server = libdipole.ObjectServer()
    ws_handler_f = libdipole.WSHandlerFactory(object_server);
    print("adding object Argv")
    object_server.add_object("Argv", ArgvI())

    ws_l = websockets.serve(ws_handler_f.server_message_loop, 'localhost', 0)
    asyncio.get_event_loop().run_until_complete(ws_l)
    assigned_port = libdipole.autoport.find_ws_port(ws_l)
    libdipole.__save_assigned_port(assigned_port, xfn)
    asyncio.get_event_loop().run_forever()
