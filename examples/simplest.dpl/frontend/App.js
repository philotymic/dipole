import React from 'react';
import HelloPrx from './HelloPrx.js';

let c = 0;

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none'};
	this.onClick = this.onClick.bind(this);
	this.hello_prx = new HelloPrx(this.props.communicator, 'Hello');
    }

    onClick() {
	this.hello_prx.sayHello().then((res) => {
	    c += 1;
	    this.setState({greeting: res.ret + c});
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
