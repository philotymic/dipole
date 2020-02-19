import ObjectClient from './ObjectClient.js';

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

export function connectToBackend() {
    return getBackendPort().then((port) => {
	let object_client = new ObjectClient(`ws://localhost:${port}`);
	return object_client.connect();
    });
}
