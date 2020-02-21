
function generateQuickGuid() {
    return Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15);
}

class ObjectClient {
    constructor(ws_handler) {
	this.ws_handler = ws_handler;
	this.pending_calls = new Map();
	this.deliver_response = this.deliver_response.bind(this);
    }

    do_remote_call(call_req) {
	return new Promise((resolve, reject) => {
	    if (this.pending_calls.size > 1) {
		console.error("this.pending_calls is too big");
	    }
	    let call_o = {
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
	    this.ws_handler.ws.send(JSON.stringify(call_message));
	});
    };
    
    deliver_response(res) {
	let call_id = res['call_id'];
	console.log("deliver_response, call_id:", res['call_id']);
	let call_obj = this.pending_calls.get(call_id);
	this.pending_calls.delete(call_id);
	let [resolve, reject] = call_obj['promise_cbs'];
	resolve(res['call_return']);
	// or reject(res) if res is actually remote exception
    }
};

export default ObjectClient;
