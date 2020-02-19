import React from 'react';
import ReactDOM from 'react-dom';
import {getArgv, connectToBackend} from 'libdipole-js';
import ArgvPrx from "./gen-js/ArgvPrx.js";

class App extends React.Component {
    constructor(props) {
	super(props);
	this.test_prx = new ArgvPrx(this.props.object_client, "Argv");
	this.state = {test_response: null};
    }

    componentDidMount() {
	this.test_prx.sayHello().then((s) => this.setState({test_response: s}));
    }
    
    render() {
	return (<div>
		<h1>Hello</h1>
		<h2>{this.props.argv}</h2>
		<h2>{this.state.test_response}</h2>
	       </div>);
    }
};

let argv = null;
getArgv().then((argv_) => {
    argv = argv_;
}).then(() => {
    return connectToBackend();
}).then((ws_handler) => {
    ReactDOM.render(<App object_client={ws_handler.object_client}
		         argv={argv}/>, document.getElementById('root'));
});
