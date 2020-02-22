import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {WSHandler, ObjectServer} from './libdipole';
import App from './App';

declare function dpl_getBackendPort(s: string, cb: (port: number) => void): void;
function getBackendPort(): Promise<number> {
    return new Promise((resolve, reject) => {
        // this function is defined in python
        dpl_getBackendPort("hello from js", (port: number) => {
            if (port) {
		resolve(port);
            } else {
		reject("getBackendPort returns null/undef");
            }
        });
    });
}

export function connectToBackend(): Promise<WSHandler> {
    return getBackendPort().then((port: number) => {
	let object_server = new ObjectServer();
	let ws_handler = new WSHandler(object_server);
	return ws_handler.connect(`ws://localhost:${port}`);
    });
}


connectToBackend().then((ws_handler: WSHandler) => {
    ReactDOM.render(<App ws_handler={ws_handler}/>,
    		    document.getElementById('root'));
});
