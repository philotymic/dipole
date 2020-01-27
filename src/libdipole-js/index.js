import Communicator from './Communicator.js';

export function getArgv() {
    return new Promise((resolve, reject) => {
	// this function is defined in python
	dpl_getArgv(null, (argv) => {
	    //console.log("getArgv:", argv);
	    resolve(argv);
	});
    });
}

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
	let communicator = new Communicator(`ws://localhost:${port}`);
	return communicator.connect();
    });
}
