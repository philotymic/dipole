import React from 'react';
import ReactDOM from 'react-dom';
import App from './App.js';


class Communicator {
    constructor(socket) {
	this.socket = socket;
	this.response_handler = null;
	this.socket.on('remote-call-response', (res) => this.response_handler(res));
    }
    
    do_call(args) {
	return new Promise((resolve, reject) => {	    
	    this.response_handler = (res) => {
		resolve(res);
	    };
	    this.socket.emit('remote-call', args);
	});
    };
};

const socket = io('http://localhost:8080');
const comm = new Communicator(socket);

ReactDOM.render(<App communicator={comm}/>, document.getElementById('root'));
