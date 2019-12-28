import React from 'react';
import ReactDOM from 'react-dom';
import {getBackendCommunicator} from 'libdipole-js';
import App from './App.js';

getBackendCommunicator().then((communicator) => {
    ReactDOM.render(<App communicator={communicator}/>, document.getElementById('root'));
});
