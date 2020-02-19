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
    
    dispatcher = libdipole.Dispatcher()
    dpl_server = libdipole.DipoleServer(dispatcher)

    print("adding object Argv")
    dispatcher.add_object("Argv", Argv())

    dpl_server_l = websockets.serve(dpl_server.message_loop, 'localhost', 0)
    asyncio.get_event_loop().run_until_complete(dpl_server_l)
    assigned_port = libdipole.autoport.find_ws_port(dpl_server_l)
    print("assigned_port:", assigned_port)
    libdipole.port_assignment_handler(assigned_port, xfn)
    asyncio.get_event_loop().run_forever()
