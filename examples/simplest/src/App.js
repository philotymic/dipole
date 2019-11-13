import React from 'react';

import './generated/Hello.js';
let Hello = window.Hello;

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: '--'};
	this.hello_prx = null;
	this.onClick = this.onClick.bind(this);
    }

    componentDidMount() {	
	let o_prx = window.ic.stringToProxy("hello:ws -h localhost -p 46399");
	//window.Hello.HelloIfcPrx.checkedCast(o_prx).then((prx) => {
	Hello.HelloIfcPrx.checkedCast(o_prx).then((prx) => {
	    this.hello_prx = prx;
	    let ret = this.hello_prx.sayHello().then((ret) => {
		//console.log("server responsed:", ret);
		this.setState({'greeting': ret});
	    });
	});
    }

    onClick() {
	//debugger;
	this.hello_prx.sayHello().then((ret) => {
	    this.setState({greeting2: ret});
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
