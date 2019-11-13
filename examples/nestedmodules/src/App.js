import React from 'react';
import './generated/all-mods.js';

let Hello = window.Hello;

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: '--', greeting3: '---'};
	this.hello_prx = null;
	this.hello2_prx = null;
	this.onClick = this.onClick.bind(this);
    }

    componentDidMount() {
	let o_prx = window.ic.stringToProxy("hello:ws -h localhost -p 10001");
	Hello.HelloIfcPrx.checkedCast(o_prx).then((prx) => {
	    this.hello_prx = prx;
	});

	let o2_prx = window.ic.stringToProxy("hello2:ws -h localhost -p 10001");
	Hello.HelloIfc2Prx.checkedCast(o2_prx).then((prx) => {
	    this.hello2_prx = prx;
	});

	this.setState({greeting: 'local hi'});
    }

    onClick() {
	//debugger;
	this.hello_prx.sayHello(this.hello2_prx).then((ret) => {
	//this.hello_prx.sayHello(this.hello_prx).then((ret) => {
	    this.setState({greeting2: ret});
	});
	
	this.hello2_prx.sayHello2(this.hello_prx).then((ret) => {
	    this.setState({greeting3: ret});
	});
    }
    
    render() {
	return (<div>
		<h1>Hello from modules</h1>
		<h2>{this.state.greeting}</h2>
		<h2>{this.state.greeting2}</h2>
		<h2>{this.state.greeting3}</h2>
		<button onClick={this.onClick}>PRESS</button>
	       </div>);
    }
};

export default App;
