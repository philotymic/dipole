
function generateQuickGuid(): string {
    return Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15);
}

export interface DipoleRequest {
    obj_id: string,
    call_method: string,
    args: string, // serialized call arguments
};

interface DipoleCall {
    call_request: DipoleRequest,
    call_id: string,
    promise_cbs: [(x: string) => void, (x: string) => void]
};

export interface DipoleResponse {
    call_id: string,
    call_return: string
};

export class Communicator {
    server_url: string;
    pending_calls: Map<string, DipoleCall>;
    socket: WebSocket | null;
    
    constructor(server_url: string) {
	this.server_url = server_url;
	this.pending_calls = new Map<string, DipoleCall>();
	this.socket = null;
    }	

    connect() {
	return new Promise<Communicator>((resolve, reject) => {
	    this.socket = new WebSocket(this.server_url);

	    this.socket.onopen = (e) => {
		console.log("[open] Connection established");
		resolve(this);
	    };

	    this.socket.onerror = function(error: any) {
		console.log(`[error] ${error.message}`);
		reject(error);
	    }

	    this.socket.onmessage = (event: any) => {
		//console.log(`from server: ${event.data}`);	    
		this.deliver_response(event.data);
	    };

	    this.socket.onclose = function(event: any) {
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
    
    deliver_response = (res_: string) => {
	let res: DipoleResponse = JSON.parse(res_) as DipoleResponse;
	console.log("deliver_response, call_id:", res.call_id);
	let call_obj: DipoleCall | undefined = this.pending_calls.get(res.call_id);
	if (!call_obj) {
	    console.log("FATAL: deliver_resonse lookup of pending_call failed");
	    throw new Error("FATAL: deliver_resonse lookup of pending_call failed");
	}
	let resolve: (x: string) => void = call_obj.promise_cbs[0];
	let reject: (x: string) => void = call_obj.promise_cbs[1];
	this.pending_calls.delete(res.call_id);
	resolve(res.call_return);
	// or reject(res) if res is actually remote exception
    }
    
    do_call(call_req: DipoleRequest): Promise<string> {
	return new Promise<string>((resolve, reject) => {
	    if (this.pending_calls.size > 1) {
		console.error("this.pending_calls is too big");
	    }
	    let call_o: DipoleCall = {
		call_request: call_req,
		call_id: generateQuickGuid(),
		promise_cbs: [resolve, reject]
	    };
	    this.pending_calls.set(call_o.call_id, call_o);
	    
	    let call_message = {
		'call_id': call_o.call_id,
		'action': 'remote-call',
		'action-args': call_o.call_request
	    };
	    console.log("socket.send, call_id:", call_o.call_id);
	    console.log("socket.send:", call_message);
	    this.socket!.send(JSON.stringify(call_message))
	});
    };
};

declare function dpl_getBackendPort(s: string, cb: (port: number) => void): void;

function getBackendPort() {
    return new Promise<number>((resolve, reject) => {
        // this function is defined in python
        dpl_getBackendPort("hello from js", (port: number) => {
            if (port) {
		resolve(port);
            } else {
		reject("getBackendPort returns null/undef");
            }
        });
    });
}

export function getBackendCommunicator() {
    return getBackendPort().then((port: number) => {
	let communicator = new Communicator(`ws://localhost:${port}`);
	return communicator.connect();
    });
}

