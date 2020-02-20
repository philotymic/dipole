#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

import threading, time
import json

def thread_w_loop(target, args):    
    nl = asyncio.new_event_loop()
    asyncio.set_event_loop(nl)
    nl.run_until_complete(target(*args))

def run_thread_w_loop(target, args):
    t = threading.Thread(target = thread_w_loop, args = (target, args))
    t.start()

class CountUp:
    def do_one_count_up(self, countup_v): pass

class CountUpPrx(CountUp):
    def __init__(self, object_client, remote_obj_id):
        self.object_client = object_client
        self.remote_obj_id = remote_obj_id
        
    async def do_one_count_up(self, countup_v):
        call_req = {
            'obj_id': self.remote_obj_id,
            'call_method': 'do_one_count_up',
            'args': json.dumps({'countup_v': countup_v})
        }
        print("CountUpPrx::do_one_count_up:", call_req)
        call_ret = await self.object_client.do_call(call_req)
        return call_ret

async def countup_thread(object_client, remote_obj_id):
    print("countup_thread started")
    countup_prx = CountUpPrx(object_client, remote_obj_id)
    c = 0
    while 1:
        res = await countup_prx.do_one_count_up(c)
        print("response from JS:", res)
        c += 1
        await asyncio.sleep(2)
    
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

    def run_countup(self, remote_obj_id):
        t_args = (self.ws_handler.object_client, remote_obj_id)
        run_thread_w_loop(target = countup_thread, args = t_args)
    
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