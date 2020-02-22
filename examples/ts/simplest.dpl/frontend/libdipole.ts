import * as DipoleProto from './DipoleProto';

function generateQuickGuid(): string
{
    return Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15);
}

export class ObjectClient {
    ws_handler: WSHandler;
    pending_calls: Map<string, DipoleProto.DipoleCall>;
    
    constructor(ws_handler: WSHandler) {
	this.ws_handler = ws_handler;
	this.pending_calls = new Map<string, DipoleProto.DipoleCall>()
    }

    do_remote_call(call_req: DipoleProto.DipoleRequest): Promise<string> {
	return new Promise<string>(
	    (resolve: (arg: string)=>void, reject: (arg: string)=>void) => {
		 if (this.pending_calls.size > 1) {
		     console.error("this.pending_calls is too big");
		 }
		 let call_o: DipoleProto.DipoleCall = {
		     call_request: call_req,
		     call_id: generateQuickGuid(),
		     promise_cbs: [resolve, reject]
		 };
		 this.pending_calls.set(call_o.call_id, call_o);
		 
		 let call_message: DipoleProto.DipoleMessage = {
		     call_id: call_o.call_id,
		     action: 'remote-call',
		     action_args: call_o.call_request
		 };
		 console.log("socket.send, call_id:", call_o.call_id);
		 console.log("socket.send:", call_message);	    
		 this.ws_handler.ws!.send(JSON.stringify(call_message));
	     });
    };
    
    deliver_response = (res: DipoleProto.DipoleResponse): void => {
	console.log("deliver_response, call_id:", res.call_id);
	let call_obj = this.pending_calls.get(res.call_id);
	if (!call_obj) {
	    throw new Error("pending calls lookup failed");
	}
	this.pending_calls.delete(res.call_id);
	let resolve: (x: string) => void = call_obj.promise_cbs[0];
	resolve(res.call_return);
	// or reject(res) if res is actually remote exception
    }
};


export class ObjectServer
{
    objects: Map<string, DipoleObjBase>;
    constructor() {
	this.objects = new Map<string, DipoleObjBase>();
    }

    add_object(obj_id: string, obj: DipoleObjBase): void
    {
	this.objects.set(obj_id, obj);
    }

    do_message_action(call_id: string,
    		      call_args: DipoleProto.DipoleRequest,
		      ws_handler: WSHandler): DipoleProto.DipoleResponse
    {
	console.log("do_message_action:", call_args);
	let object_id = call_args.obj_id;
	let method = call_args.call_method;
	let args = JSON.parse(call_args.args);
	let pass_calling_context = call_args.pass_calling_context;
	if (pass_calling_context) {
	    args = {...args, ctx: {ws_handler: ws_handler}};
	}
	
	console.log("lookup up obj", object_id);
	let obj = this.objects.get(object_id);
	if (!obj) {
	    throw new Error("objects lookup failed");
	}
	let call_return = obj.__call_method(method, args);
	console.log("ret:", call_return)

	let res: DipoleProto.DipoleResponse = {
	    action: 'remote-call-response',
	    call_id: call_id,
	    call_return: call_return
	};
	return res;
    }
};

export class WSHandler
{
    ws: WebSocket | null;
    object_client: ObjectClient;
    object_server: ObjectServer;
    
    constructor(object_server: ObjectServer) {
	this.ws = null;
	this.object_client = new ObjectClient(this);
	this.object_server = object_server;
    }

    connect(ws_server_url: string): Promise<WSHandler> {
	return new Promise<WSHandler>(
	       (resolve: (arg: WSHandler) => void,
	        reject: (arg: WSHandler) => void) => {
	    this.ws = new WebSocket(ws_server_url);
	    this.ws.onopen = (e: any) => {
		console.log("[open] Connection established");
		resolve(this);
	    };

	    this.ws.onerror = function(error: any) {
		console.log(`[error] ${error.message}`);
		reject(error);
	    }

	    this.ws.onmessage = (event: any) => {
		console.log(`from server: ${event.data}`);
		let m = JSON.parse(event.data);
		if (m['action'] == 'remote-call-response') {
		    this.object_client.deliver_response(m as DipoleProto.DipoleResponse);
		} else if (m['action'] == 'remote-call') {
		    let message: DipoleProto.DipoleMessage = m as DipoleProto.DipoleMessage;
		    let call_id: string = message.call_id;
		    let message_action_ret: DipoleProto.DipoleResponse;
		    message_action_ret = this.object_server.do_message_action(call_id, message.action_args, this);
		    console.log("message_action_ret:", message_action_ret);
		    this.ws!.send(JSON.stringify(message_action_ret))
		}
	    };

	    this.ws.onclose = function(event: any) {
		if (event.wasClean) {
		    console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		} else {
		    // e.g. server process killed or network down
		    // event.code is usually 1006 in this case
		    console.log('[close] Connection died');
		}
	    };
	});
    }
};

export class DipoleObjBase {
    __call_method(method: string, args: object): string {
	throw new Error("not implemented");
    }
};

