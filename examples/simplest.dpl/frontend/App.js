import React from 'react';
import Communicator from './Communicator.js';
import HelloPrx from './HelloPrx.js';

let c = 0;

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: 'none'};
	this.onClick = this.onClick.bind(this);
	this.hello_prx = null;
    }

    componentDidMount() {
	getBackendPort().then((port) => {
	    const socket = new WebSocket(`ws://localhost:${port}`);
	    this.props.communicator = new Communicator(socket);
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
