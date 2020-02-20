import asyncio
import json, uuid

def exportclass(cls):
    print("decorator")
    return cls

def __save_assigned_port(assigned_port, named_pipe_fn):
    print("running server at port", assigned_port, named_pipe_fn)
    with open(named_pipe_fn, "w") as named_pipe_fd:
        print(assigned_port, file = named_pipe_fd)

class ObjectServer:
    def __init__(self, ws_handler):
        self.ws_handler = ws_handler
        self.objects = {}

    def add_object(self, object_id, obj):
        obj.ws_handler = self.ws_handler
        self.objects[object_id] = obj

    def do_message_action(self, call_id, call_args):
        print('do_message_action:', call_args)
        #ipdb.set_trace()
        object_id = call_args['obj_id']
        method = call_args['call_method']
        args = json.loads(call_args['args'])

        print("looking up obj", object_id)
        obj = self.objects[object_id]
        b_method = getattr(obj, method)
        ret = None; exc = None
        ret = b_method(**args)
        print("ret:", ret)

        return {'action': 'remote-call-response',
                'call_id': call_id,
                'call_return': ret}

class ObjectClient:
    def __init__(self, ws_handler):
        self.pending_calls = {} # call_id -> call_o
        self.ws_handler = ws_handler
        
    async def do_call(self, call_req):
        result_fut = asyncio.Future()
        call_o = {
            'call_request': call_req,
            'call_id': str(uuid.uuid1()),
            'result_fut': result_fut
            }
        self.pending_calls[call_o['call_id']] = call_o

        call_message = {
            'call_id': call_o['call_id'],
            'action': 'remote-call',
            'action-args': call_o['call_request']
            }
        
        print("socket.send, call_id:", call_o['call_id'])
        print("socket.send:", call_message)
        await self.ws_handler.ws.send(json.dumps(call_message))
        #ret = await result_fut
        ret = None
        return ret
        
    def deliver_response(self, res):
        call_id = res['call_id']
        print("deliver_response, call_id:", call_id)
        call_o = self.pending_calls[call_id]
        del self.pending_calls[call_id]
        call_o['result_fut'].set_result(res['call_return'])        
        
class WSHandler:
    def __init__(self):
        self.object_server = ObjectServer(self)
        self.object_client = ObjectClient(self)
        self.ws = None
        
    async def message_loop(self, ws, path):
        self.ws = ws
        while 1:
            message = await ws.recv()
            print("async on_message:", message)
            message_json = json.loads(message)
            if message_json['action'] == 'remote-call':
                call_args = message_json['action-args']
                call_id = message_json['call_id']
                message_action_ret = self.object_server.do_message_action(call_id, call_args)
                print("message_action_ret:", message_action_ret)
                await ws.send(json.dumps(message_action_ret))
            elif message_json['action'] == 'remote-call-response':
                self.object_client.deliver_response(message_json)
                
