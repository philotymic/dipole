import ObjectClient from './ObjectClient.js';
import ObjectServer from './ObjectServer.js';
import WSHandler from './WSHandler.js';

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
	let object_server = new ObjectServer();
	let ws_handler = new WSHandler(object_server);
	return ws_handler.connect(`ws://localhost:${port}`);
    });
}

export function connectToServer(ws_url) {
    let object_server = new ObjectServer();
    let ws_handler = new WSHandler(object_server);
    return ws_handler.connect(ws_url);
}

