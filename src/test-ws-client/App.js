import React from 'react';

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: ''};
	this.onClick = this.onClick.bind(this);
	this.socket = null;
    }

    componentDidMount() {
	this.socket_init();
    }
    
    socket_init() {
	this.socket = new WebSocket("wss://javascript.info/article/websocket/demo/hello");

	this.socket.onopen = function(e) {
	    console.log("[open] Connection established");
	    //console.log("Sending to server");
	    //socket.send("My name is John");
	};

	this.socket.onmessage = function(event) {
	    console.log(`[message] Data received from server: ${event.data}`);
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
    
    onClick() {
	console.log("Hello");
	//debugger;

	console.log("Sending to server");
	this.socket.send("My name is John");
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
