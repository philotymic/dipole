import React from 'react';
import HelloPrx from './gen-js/HelloPrx.js';
//import SomethingHappen from './gen-js/SomethingHappen.js';

/*
class SomethingHappen {
    when_something_happen(what_happen) {
	throw new Error("not implemented");
    }
};

class SomethingHappenI extends SomethingHappen {
    when_something_happen(what_happen) {
	console.log("SomethingHappenI::when_something_happen:", what_happen);
    }
};
*/

let c = 0;
class App extends React.Component {
    constructor(props) {
	super(props);
	this.hello_prx = new HelloPrx(this.props.communicator, 'Hello');
	//let somethinghappeni = new SomethingHappenI(this.props.communicator);
	//this.props.communicator.add_object("SOMETHING_CB", somethinghappeni);
	this.state = {greeting: 'none', greeting2: 'none', holidays: null};
	this.onClick = this.onClick.bind(this);
    }

    componentDidMount() {
	this.hello_prx.sayHello().then((res) => {
	    this.setState({...this.state, greeting: res + " first time"});
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
	this.hello_prx.get_holidays().then(x => {
	    this.setState({holidays: x});
	});
    }
    
    render() {
	return (<div>
		<h1>Hello from modules</h1>
		<h2>{this.state.greeting}</h2>
		<h2>{this.state.greeting2}</h2>
		<h2>{this.state.holidays}</h2>
		<button onClick={this.onClick}>PRESS</button>
	       </div>);
    }
};

export default App;
