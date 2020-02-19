class ObjectServer
{
    constructor(obj_client) {
	this.objects = new Map();	    
    }

    add_object(obj_id, obj) {
	this.objects.add(obj_id, obj);
    }

};

export default ObjectServer;

