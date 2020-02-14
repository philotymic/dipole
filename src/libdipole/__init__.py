from . import mod_libdipole
import json
import sys

def exportclass(cls):
    print("decorator")
    return cls

class Dispatcher:
    def __init__(self, ws_server):
        self.ws_server = ws_server
        self.objects = {}

    def add_object(self, object_id, obj):
        self.objects[object_id] = obj

    def do_message_action(self, call_args):
        #print 'do_message_action:', call_args
        #ipdb.set_trace()
        call_id = call_args['call_id']
        object_id = call_args['obj_id']
        method = call_args['call_method']
        args = call_args['args']

        print("looking up obj", object_id)
        obj = self.objects[object_id]
        b_method = getattr(obj, method)
        ret = None; exc = None
        ret = b_method(**args)
        print("ret:", call_id)

        return {'call_return': ret, 'call_id': call_id}

class BackendEventHandler(mod_libdipole.DipoleEventHandler):
    def __init__(self, port_assignment_handler, xfn_fn):        
        mod_libdipole.DipoleEventHandler.__init__(self)
        self.dispatcher = None
        self.port_assignment_handler = port_assignment_handler
        self.xfn_fn = xfn_fn

    def on_port_assignment(self, assigned_port):
        print("assigned port:", assigned_port)
        self.port_assignment_handler(assigned_port, self.xfn_fn)
        
    def on_connect(self):
        print("on_connect")
        
    def on_message(self, message):
        print("on_message:")
        message_json = json.loads(message)
        #print message_json, self.dispatcher
        if message_json['action'] == 'remote-call':
            call_args = message_json['action-args']
            message_action_ret = self.dispatcher.do_message_action(call_args)
        #print "message_action_ret:", message_action_ret
        return json.dumps(message_action_ret)

def port_assignment_handler(assigned_port, named_pipe_fn):
    print("running server at port", assigned_port, named_pipe_fn)
    with open(named_pipe_fn, "w") as named_pipe_fd:
        print(assigned_port, file = named_pipe_fd)
        
