#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

class CountUp:
    def do_one_count_up(self, countup_v): pass

class CountUpPrx(CountUp):
    def __init__(self, object_client, remote_obj_id):
        self.object_client = object_client
        self.remote_obj_id = remote_obj_id
        
    def do_one_count_up(self, countup_v):
        call_req = {
            'obj_id': self.remote_obj_id,
            'call_method': 'do_one_count_up',
            'args': json.parse({'countup_v': countup_v})
        }
        call_ret = self.object_client.do_call(call_req)
        return call_ret
        
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

def countup_thread(object_client):
    countup_prx = CountUpPrx(object_client, 'count_up')
    c = 0
    while 1:
        print("response from JS:", count_up_prx.do_one_count_up(c))
        c += 1
        time.sleep(3)
    
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
