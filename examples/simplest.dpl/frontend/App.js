import React from 'react';

let c = 0;

class App extends React.Component {
    constructor(props) {
	super(props);
	this.state = {greeting: 'none'};
	this.onClick = this.onClick.bind(this);
    }

    setSocketListeners () {
	this.props.socket.on('remote-call-response', (res) => {
	    console.log("received", res);
	    this.setState({greeting: res.ret});
	});
    }
    
    componentDidMount() {
	this.setSocketListeners();
    }

    onClick() {
	//debugger;
	this.props.socket.emit('remote-call', {'obj_id': 'Hello', 'call_method': 'sayHello', 'args': {}});
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
