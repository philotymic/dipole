#import ipdb
import asyncio, websockets
import json, uuid

def exportclass(cls):
    print("decorator")
    return cls

def __save_assigned_port(assigned_port, named_pipe_fn):
    print("running server at port", assigned_port, named_pipe_fn)
    with open(named_pipe_fn, "w") as named_pipe_fd:
        print(assigned_port, file = named_pipe_fd)

class CallingContext:
    def __init__(self, ws_handler):
        self.ws_handler = ws_handler
        
class ObjectServer:
    def __init__(self):
        self.objects = {}

    def add_object(self, object_id, obj):
        self.objects[object_id] = obj
        
    async def do_message_action(self, call_id, call_args, ws_handler):
        print('handle_message:', call_args)
        #ipdb.set_trace()
        object_id = call_args['obj_id']
        method = call_args['call_method']
        args = json.loads(call_args['args'])
        pass_calling_context = call_args['pass_calling_context']
        if pass_calling_context:
            args.append(CallingContext(ws_handler))

        print("looking up obj", object_id)
        if not object_id in self.objects:
            raise Exception("do_message_action: can't find object", object_id)
        obj = self.objects[object_id]
        b_method = getattr(obj, method)
        if b_method == None:
            raise Exception("do_message_action: can't find method", method, object_id)
        ret = None; exc = None
        ret = await b_method(*args)
        print("ret:", ret)

        return {'action': 'remote-call-response',
                'call_id': call_id,
                'call_return': ret}

def set_result_f(args):
    fut = args[0]
    result = args[1]
    fut.set_result(result)
    
class ObjectClient:
    def __init__(self, ws_handler):
        self.pending_calls = {} # call_id -> call_o
        self.ws_handler = ws_handler
        
    async def do_remote_call(self, call_req):
        result_fut = asyncio.Future()
        call_o = {
            'call_request': call_req,
            'call_id': str(uuid.uuid1()),
            'result_fut': result_fut,
            'loop': asyncio.get_event_loop()
            }
        self.pending_calls[call_o['call_id']] = call_o

        call_message = {
            'call_id': call_o['call_id'],
            'action': 'remote-call',
            'action_args': call_o['call_request']
            }
        
        print("socket.send, call_id:", call_o['call_id'])
        print("socket.send:", call_message)
        await self.ws_handler.ws.send(json.dumps(call_message))
        ret = await result_fut
        return ret
        
    def deliver_response(self, res):
        call_id = res['call_id']
        print("deliver_response, call_id:", call_id)
        call_o = self.pending_calls[call_id]
        del self.pending_calls[call_id]
        result_fut = call_o['result_fut']
        thread_loop = call_o['loop']
        #call_o['result_fut'].set_result(res['call_return'])
        call_return_v = res['call_return'] if 'call_return' in res else None
        thread_loop.call_soon_threadsafe(set_result_f, [result_fut, call_return_v])

class WSHandler:
    def __init__(self, object_server):
        self.object_server = object_server
        self.object_client = ObjectClient(self)
        self.ws = None
        
    async def client_message_loop(self, ws_url):
        print(f"connecting to {ws_url}")
        self.ws = await websockets.connect(ws_url)
        asyncio.create_task(self.run_message_loop())
        
    async def run_message_loop(self):
        print("entering message loop")
        while 1:
            message = await self.ws.recv()
            print("async on_message:", message)
            message_json = json.loads(message)
            if message_json['action'] == 'remote-call':
                call_args = message_json['action_args']
                call_id = message_json['call_id']
                message_action_ret = await self.object_server.do_message_action(call_id, call_args, self)
                print("message_action_ret:", message_action_ret)
                await self.ws.send(json.dumps(message_action_ret))
            elif message_json['action'] == 'remote-call-response':
                self.object_client.deliver_response(message_json)
        
class WSHandlerFactory:
    def __init__(self, object_server):
        self.object_server = object_server
        
    async def server_message_loop(self, ws, path):
        print("accept passed")
        #ipdb.set_trace()
        ws_handler = WSHandler(self.object_server)
        ws_handler.ws = ws
        await ws_handler.run_message_loop()
                
