#import ipdb
import sys, os, asyncio
import prctl, signal

import websockets
sys.path.append(os.path.join(os.environ['dipole_topdir'], "src"))
import libdipole
import libdipole.autoport

import threading, time
import json

import backend

def thread_w_loop(target, args):    
    nl = asyncio.new_event_loop()
    asyncio.set_event_loop(nl)
    nl.run_until_complete(target(*args))

def run_thread_w_loop(target, args):
    t = threading.Thread(target = thread_w_loop, args = (target, args))
    t.start()

async def countup_thread(ws_handler, remote_obj_id):
    print("countup_thread started")
    countup_prx = backend.CountUpPrx(ws_handler, remote_obj_id)
    c = 0
    while 1:
        res = await countup_prx.do_one_count_up(c)
        print("response from JS:", res)
        c += 1
        await asyncio.sleep(2)
    
class HelloI(backend.Hello):
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

    def run_countup(self, remote_obj_id, ctx):
        t_args = (ctx.ws_handler, remote_obj_id)
        run_thread_w_loop(target = countup_thread, args = t_args)
    
if __name__ == "__main__":
    if 1:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM
    xfn = sys.argv[1]

    object_server = libdipole.ObjectServer()
    ws_handler = libdipole.WSHandler(object_server);
    print("adding object Hello")
    object_server.add_object("Hello", HelloI())

    ws_l = websockets.serve(ws_handler.message_loop, 'localhost', 0)
    asyncio.get_event_loop().run_until_complete(ws_l)
    assigned_port = libdipole.autoport.find_ws_port(ws_l)
    libdipole.__save_assigned_port(assigned_port, xfn)
    asyncio.get_event_loop().run_forever()
