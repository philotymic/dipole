import React from 'react';

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {server_port: null, greeting: ''};
	this.onClick = this.onClick.bind(this);
	this.connect = this.connect.bind(this);
	this.handle_server_port = this.handle_server_port.bind(this);
	this.socket = null;
    }

    componentDidMount() {
    }

    connect() {
	this.socket_init();
    }	
    
    socket_init() {
	this.socket = new WebSocket(`ws://localhost:${this.state.server_port}`);

	this.socket.onopen = function(e) {
	    console.log("[open] Connection established");
	    //console.log("Sending to server");
	    //socket.send("My name is John");
	};

	this.socket.onmessage = function(event) {
	    console.log(`from server: ${event.data}`);
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

	this.socket.onerror = function(error) {
	    console.log(`[error] ${error.message}`);
	};
    }

    handle_server_port(evt) {
	this.setState({server_port: evt.target.value});
    }
    
    onClick() {
	console.log("Hello");
	//debugger;

	console.log("Sending to server");
	this.socket.send("My name is mine");
    }
    
    render() {
	return (<div>
		<h1>Hello from modules</h1>
		<h2>Enter port:</h2><input type="text" value={this.state.server_port} onChange={this.handle_server_port}/>
		<button onClick={this.connect}>CONNECT</button>
		<h2>{this.state.greeting}</h2>
		<button onClick={this.onClick}>PRESS</button>
	       </div>);
    }
};

export default App;
