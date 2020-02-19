import React from 'react';
import ReactDOM from 'react-dom';
import {connectToBackend} from 'libdipole-js';
import App from './App.js';

connectToBackend().then((obj_client) => {
    ReactDOM.render(<App obj_client={obj_client}/>, document.getElementById('root'));
});
