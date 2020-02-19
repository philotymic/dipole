import React from 'react';
import ReactDOM from 'react-dom';
import {connectToBackend} from 'libdipole-js';
import App from './App.js';

connectToBackend().then((ws_handler) => {
    ReactDOM.render(<App object_client={ws_handler.object_client}
		    object_server={ws_handler.object_server}/>,
		    document.getElementById('root'));
});
