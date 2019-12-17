import React from 'react';
let Hello = window.Hello;

let c = 0;

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: '--'};
	this.hello_prx = null;
	this.onClick = this.onClick.bind(this);
    }

    componentDidMount() {	
	getBackendPort().then((backend_port) => {
	    let backend_proxy_s = `hello:ws -h localhost -p ${backend_port}`;
	    return window.ic.stringToProxy(backend_proxy_s);
	}).then((o_prx) => {
	    return Hello.HelloIfcPrx.checkedCast(o_prx);
	}).then((prx) => {
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
	    this.setState({greeting2: ret + c.toString()});
	    c++;
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
