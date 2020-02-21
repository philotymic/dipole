import React from 'react';
import * as backend from './gen-js/backend.js';

class CountUp {
    __call_method(method, args_json) {
	if (method == 'do_one_count_up') {
	    let args = [args_json['countup_v']];
	    return this.do_one_count_up(...args);
	}
    }

    do_one_count_up(countup_v) {
	throw new Error("not implemnted");
    }
}    

class CountUpI extends CountUp
{
    constructor(app) {
	super();
	this.app = app;
	this.countup = 0;
    }

    do_one_count_up(countup_v) {
	console.log("CountUp::do_one_count_up:", countup_v)
	this.countup += 1;
	let old_state = this.app.state;
	old_state.countup = countup_v;
	console.log("old_state:", old_state)
	this.app.setState(old_state);
	return this.countup;
    }
};

let c = 0;
class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none', greeting2: 'none',
		      holidays: [], countup: 'none'};
	this.onClick = this.onClick.bind(this);
    }

    componentDidMount() {
	console.log("componentDidMount");
	this.hello_prx = new backend.HelloPrx(this.props.ws_handler, 'Hello');	
	let new_obj = new CountUpI(this);
	this.props.ws_handler.object_server.add_object("countup", new_obj);
	this.hello_prx.sayHello().then((res) => {
	    this.setState({...this.state, greeting: res + " first time"});
	});
	this.hello_prx.run_countup("countup").then(() => {
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
