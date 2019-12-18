import React from 'react';
import ReactDOM from 'react-dom';
import App from './App.js';
import Communicator from './Communicator.js';

const socket = io('http://localhost:8080');
const comm = new Communicator(socket);
ReactDOM.render(<App communicator={comm}/>, document.getElementById('root'));
