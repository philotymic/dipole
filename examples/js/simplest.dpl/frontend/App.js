import React from 'react';
import HelloPrx from './gen-js/HelloPrx.js';

let c = 0;
class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: 'none',
		      holidays: null, countup: null};
	this.onClick = this.onClick.bind(this);
    }

    componentDidMount() {
	this.hello_prx = new HelloPrx(this.props.ws_handler, 'Hello');
	this.hello_prx.sayHello().then((res) => {
	    this.setState({...this.state, greeting: res + " first time"});
	});
    }
    
    onClick() {
	Promise.resolve().then(() => {
	    return this.hello_prx.sayHello();
	}).then((res) => {
	    c += 1;
	    this.setState({...this.state, greeting: res + c});
	}).then(() => {
	    return this.hello_prx.sayAloha('hawaii');
	}).then((res) => {
	    this.setState({...this.state, greeting2: res});
	}).then(() => {
	    return this.hello_prx.get_holidays();
	}).then(x => {
	    this.setState({holidays: x});
	});
    }
    
    render() {
	return (<div>
		<h1>Hello from modules</h1>
		<h2>{this.state.greeting}</h2>
		<h2>{this.state.greeting2}</h2>
		<h2>{this.state.holidays}</h2>
		<h1>{this.state.countup}</h1>
		<button onClick={this.onClick}>PRESS</button>
	       </div>);
    }
};

export default App;
