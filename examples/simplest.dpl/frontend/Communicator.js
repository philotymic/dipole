
function generateQuickGuid() {
    return Math.random().toString(36).substring(2, 15) +
        Math.random().toString(36).substring(2, 15);
}

class Communicator {
    constructor(socket) {
	this.socket = socket;
	this.pending_calls = new Map();
	this.deliver_response = this.deliver_response.bind(this);
	this.socket.on('remote-call-response', this.deliver_response);
    }

    deliver_response(res) {
	let call_id = res['call_id'];
	let call_obj = this.pending_calls.get(call_id);
	this.pending_calls.delete(call_id);
	let [resolve, reject] = call_obj['promise_cbs'];
	resolve(res);
	// or reject(res) if res is actually remote exception
    }
    
    do_call(args) {
	return new Promise((resolve, reject) => {	    
	    args = {...args, 'call_id': generateQuickGuid(),
		    'promise_cbs': [resolve, reject]};
	    this.pending_calls.set(args['call_id'], args);
	    this.socket.emit('remote-call', args);
	});
    };
};

export default Communicator;
