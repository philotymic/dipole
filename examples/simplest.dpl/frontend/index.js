import React from 'react';
import ReactDOM from 'react-dom';
import App from './App.js';

const socket = io('http://localhost:8080');
ReactDOM.render(<App socket={socket}/>, document.getElementById('root'));
