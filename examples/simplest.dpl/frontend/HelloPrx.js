class HelloPrx {
    constructor(proxy, remote_obj_id) {
	this.proxy = proxy;
	this.remote_obj_id = remote_obj_id;
    }

    sayHello() {
	let args = {'obj_id': this.remote_obj_id,
		    'call_method': 'sayHello',
		    'args': {}};
	return this.proxy.do_call(args);
    }
};

export default HelloPrx;
