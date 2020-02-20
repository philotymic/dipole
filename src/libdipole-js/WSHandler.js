import ObjectClient from './ObjectClient.js';
import ObjectServer from './ObjectServer.js';

class WSHandler
{
    constructor(ws_server_url) {
	this.ws_server_url = ws_server_url;
	this.socket = null;
	this.object_client = null;
	this.object_server = null;
    }

    connect() {
	this.object_client = new ObjectClient(this);
	this.object_server = new ObjectServer();
	return new Promise((resolve, reject) => {
	    this.socket = new WebSocket(this.ws_server_url);

	    this.socket.onopen = (e) => {
		console.log("[open] Connection established");
		resolve(this);
	    };

	    this.socket.onerror = function(error) {
		console.log(`[error] ${error.message}`);
		reject(error);
	    }

	    this.socket.onmessage = (event) => {
		console.log(`from server: ${event.data}`);	    
		let message = JSON.parse(event.data);
		if (message['action'] == 'remote-call-response') {
		    this.object_client.deliver_response(message);
		} else if (message['action'] == 'remote-call') {
		    let call_args = message['action-args']
		    let call_id = message['call_id']
		    let message_action_ret = this.object_server.do_message_action(call_id, call_args);
		    console.log("message_action_ret:", message_action_ret);
		    this.socket.send(JSON.stringify(message_action_ret))
		}
	    };

	    this.socket.onclose = function(event) {
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
export default WSHandler;
