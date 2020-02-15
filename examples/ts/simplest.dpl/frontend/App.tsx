import * as React from 'react';
import {Communicator} from './Communicator';
import HelloPrx from './HelloPrx';

interface AppProps {
    communicator: Communicator
};

interface AppState {
    greeting: string,
    greeting2: string
};

let c: number = 0;
class App extends React.Component<AppProps, AppState> {
    hello_prx: HelloPrx;
    state: AppState = {greeting: 'none', greeting2: 'none'};
    constructor(props: AppProps) {
	super(props);
	this.hello_prx = new HelloPrx(this.props.communicator, 'Hello');
    }

    componentDidMount() {
	this.hello_prx.sayHello().then((res: string) => {
	    this.setState({...this.state, greeting: res + " first time"});
	});
    }	
    
    onClick = () => {
	this.hello_prx.sayHello().then((res: string) => {
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
