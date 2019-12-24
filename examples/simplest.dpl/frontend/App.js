import React from 'react';
import Communicator from 'libdipole-js';
import HelloPrx from './gen-js/HelloPrx.js';

function getBackendPort() {
    return new Promise((resolve, reject) => {
        // this function is defined in python
        dpl_getBackendPort("hello from js", (port) => {
            if (port) {
		resolve(port);
            } else {
		reject("getBackendPort returns null/undef");
            }
        });
    });
}

function getBackendCommunicator() {
    return getBackendPort().then((port) => {
	const socket = new WebSocket(`ws://localhost:${port}`);
	return Promise.resolve(new Communicator(socket));
    });
}

let c = 0;
class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: 'none'};
	this.onClick = this.onClick.bind(this);
	this.hello_prx = null;
    }

    componentDidMount() {
	getBackendCommunicator().then((communicator) => {
	    this.props.communicator = communicator;
	    this.hello_prx = new HelloPrx(this.props.communicator, 'Hello');
	});
    }
    
    onClick() {
	this.hello_prx.sayHello().then((res) => {
	    c += 1;
	    this.setState({...this.state, greeting: res + c});
	});
	this.hello_prx.sayAloha('hawaii').then((res) => {
	    this.setState({...this.state, greeting2: res});
	});
    }
    
    render() {
	return (<div>
		<h1>Hello from modules</h1>
		<h2>{this.state.greeting}</h2>
		<h2>{this.state.greeting2}</h2>
		<button onClick={this.onClick}>PRESS</button>
	       </div>);
    }
};

export default App;
