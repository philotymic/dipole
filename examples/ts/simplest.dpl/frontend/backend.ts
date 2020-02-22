import * as DipoleProto from './DipoleProto';
import {WSHandler} from './libdipole';

export class HelloPrx {
    ws_handler: WSHandler;
    remote_obj_id: string;
    
    constructor(ws_handler: WSHandler, remote_obj_id: string) {
	this.ws_handler = ws_handler;
	this.remote_obj_id = remote_obj_id;
    }
            
    sayHello(): Promise<string> {
        let call_req: DipoleProto.DipoleRequest = {
	    obj_id: this.remote_obj_id,
            call_method: 'sayHello',
            pass_calling_context: false,
            args: JSON.stringify([])
	};
        return this.ws_handler.object_client.do_remote_call(call_req).then((ret: string) => {return ret as string});
    }
                
    sayAloha(language:string): Promise<string> {
        let call_req: DipoleProto.DipoleRequest = {
	    obj_id: this.remote_obj_id,
            call_method: 'sayAloha',
            pass_calling_context: false,
            args: JSON.stringify([language])
	};
        return this.ws_handler.object_client.do_remote_call(call_req).then((ret:string) => {return ret});
    }
};
