import ipdb
import sys, os
import prctl, signal
import json, time

sys.path.append("/home/asmirnov/dipole/src")
import myws

#@dipole.exportclass
@myws.exportclass
class Hello:
    def sayHello(self):
        print "Hello World!"
        return "Hello, World!"

    def sayAloha(self, language):
        print "Aloha"
        #time.sleep(3)
        return language + "Aloha"

class Dispatcher:
    def __init__(self, ws_server):
        self.ws_server = ws_server
        self.objects = {}

    def add_object(self, object_id, obj):
        self.objects[object_id] = obj

    def do_message_action(self, call_args):
        print 'do_message_action:', call_args
        #ipdb.set_trace()
        call_id = call_args['call_id']
        object_id = call_args['obj_id']
        method = call_args['call_method']
        args = call_args['args']

        obj = dispatcher.objects[object_id]
        b_method = getattr(obj, method)
        ret = None; exc = None
        ret = b_method(**args)
        print "ret:", ret, call_id

        return {'call_return': ret, 'call_id': call_id}
        
class EventHandler(myws.MyWSEventHandler):
    def __init__(self):        
        myws.MyWSEventHandler.__init__(self)
        self.dispatcher = None

    def on_port_assignment(self, assigned_port):
        print "assigned port:", assigned_port
        if 1:
            xfn_fn = sys.argv[1]
            print "running server at port", assigned_port
            xfn_fd = open(xfn_fn, "w+b")
            print >>xfn_fd, assigned_port
            xfn_fd.close()
            sys.stdout.flush()
        
    def on_connect(self):
        print "on_connect"
        
    def on_message(self, message):
        print "on_message:", message
        message_json = json.loads(message)
        print message_json
        if message_json['action'] == 'remote-call':
            call_args = message_json['action-args']
            message_action_ret = self.dispatcher.do_message_action(call_args)
        print "message_action_ret:", message_action_ret
        return json.dumps(message_action_ret)
        
if __name__ == "__main__":
    if 1:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM

    ws_server = myws.MyWSServer()
    ws_event_handler = EventHandler()
    ws_server.set_event_handler(ws_event_handler)
    dispatcher = Dispatcher(ws_server)
    ws_event_handler.dispatcher = dispatcher
    
    print "adding object Hello"
    dispatcher.add_object("Hello", Hello())

    ws_server.run_listener(port = 0)
        
    
