import React from 'react';
import ReactDOM from 'react-dom';
import {connectToBackend} from 'libdipole-js';
import App from './App.js';

connectToBackend().then((ws_handler) => {
    ReactDOM.render(<App ws_handler={ws_handler}/>,
		    document.getElementById('root'));
});
