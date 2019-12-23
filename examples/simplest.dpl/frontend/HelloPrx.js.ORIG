class HelloPrx {
    constructor(communicator, remote_obj_id) {
	this.communicator = communicator;
	this.remote_obj_id = remote_obj_id;
    }

    sayHello() {
	let args = {'obj_id': this.remote_obj_id,
		    'call_method': 'sayHello',
		    'args': {}};
	return this.communicator.do_call(args);
    }

    sayAloha(language) {
	let args = {'obj_id': this.remote_obj_id,
		    'call_method': 'sayAloha',
		    'args': {'language': language}};
	return this.communicator.do_call(args);
    }
};

export default HelloPrx;
