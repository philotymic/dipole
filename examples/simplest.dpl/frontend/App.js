import React from 'react';

let c = 0;

class Communicator {
    constructor(socket) {
	this.socket = socket;
	this.response_handler = null;
	this.socket.on('remote-call-response', (res) => this.response_handler(res));
    }
    
    do_call(args) {
	return new Promise((resolve, reject) => {	    
	    this.response_handler = (res) => {
		resolve(res);
	    };
	    this.socket.emit('remote-call', args);
	});
    };
}

class Hello {
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
}

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none'};
	this.onClick = this.onClick.bind(this);
	this.communicator = new Communicator(this.props.socket);
	this.hello_prx = new Hello(this.communicator, 'Hello');
    }

    onClick() {
	this.hello_prx.sayHello().then((res) => {
	    console.log("received", res);
	    this.setState({greeting: res.ret});
	});
    }
    
    render() {
	return (<div>
		<h1>Hello from modules</h1>
		<h2>{this.state.greeting}</h2>
		<button onClick={this.onClick}>PRESS</button>
	       </div>);
    }
};

export default App;
