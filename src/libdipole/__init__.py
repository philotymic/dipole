import json

def exportclass(cls):
    print("decorator")
    return cls


def __save_assigned_port(assigned_port, named_pipe_fn):
    print("running server at port", assigned_port, named_pipe_fn)
    with open(named_pipe_fn, "w") as named_pipe_fd:
        print(assigned_port, file = named_pipe_fd)

class ObjectServer:
    def __init__(self):
        self.objects = {}

    def add_object(self, object_id, obj):
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
        print("ret:", call_id)

        return {'call_return': ret, 'call_id': call_id}
        
    async def message_loop(self, ws, path):
        async for message in ws:
            print("async on_message:", message)
            message_json = json.loads(message)
            if message_json['action'] == 'remote-call':
                call_args = message_json['action-args']
                call_id = message_json['call_id']
                message_action_ret = self.do_message_action(call_id, call_args)
            print("message_action_ret:", message_action_ret)
            await ws.send(json.dumps(message_action_ret))
