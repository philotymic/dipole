import React from 'react';
import ReactDOM from 'react-dom';
//import {getBackendCommunicator} from 'libdipole-js';
import {getBackendCommunicator, Communicator} from './Communicator';
import App from './App';

getBackendCommunicator().then((communicator: Communicator) => {
    ReactDOM.render(<App communicator={communicator}/>, document.getElementById('root'));
});
