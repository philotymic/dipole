import Communicator from './Communicator.js';

function getBackendPort() {
    return new Promise((resolve, reject) => {
        // this function is defined in python
        dpl_getBackendPort("hello from js", (port) => {
            if (port) {
		resolve(port);
            } else {
		reject("getBackendPort returns null/undef");
            }
        });
    });
}

export function getBackendCommunicator() {
    return getBackendPort().then((port) => {
	const socket = new WebSocket(`ws://localhost:${port}`);
	return Promise.resolve(new Communicator(socket));
    });
}
