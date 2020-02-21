class ObjectServer
{
    constructor() {
	this.objects = new Map();	    
    }

    add_object(obj_id, obj) {
	this.objects.set(obj_id, obj);
    }

    do_message_action(call_id, call_args) {
	console.log("do_message_action:", call_args);
	let object_id = call_args['obj_id'];
	let method = call_args['call_method'];
	let args = JSON.parse(call_args['args']);

	console.log("lookup up obj", object_id);
	let obj = this.objects.get(object_id);
	let ret = obj.__call_method(method, args);
	console.log("ret:", ret)

	return {'action': 'remote-call-response',
		'call_id': call_id,
		'call_return': ret};
    }
    
};

export default ObjectServer;

