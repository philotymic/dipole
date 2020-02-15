import {Communicator, DipoleRequest} from './Communicator';

class HelloPrx {
    communicator: Communicator;
    remote_obj_id: string;
      
    constructor(communicator: Communicator, remote_obj_id: string) {
        this.communicator = communicator;
        this.remote_obj_id = remote_obj_id;
    }

    sayHello (): Promise<string> {
        let call_req: DipoleRequest = {
	    obj_id: this.remote_obj_id,
	    call_method: 'sayHello',
	    args: JSON.stringify({})
	};
	return this.communicator.do_call(call_req).then((ret: string) => {
	    return ret as string;
	});
    }
        
    sayAloha ( language: string ) : Promise<string> {
	let call_req: DipoleRequest = {
            obj_id: this.remote_obj_id,
	    call_method: 'sayAloha',
	    args: JSON.stringify({'language': language})
	};
	return this.communicator.do_call(call_req).then((ret: string) => {
	    return ret as string;
	});
    }
    
};
export default HelloPrx ;
