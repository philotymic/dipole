export interface DipoleRequest {
    obj_id: string,
    call_method: string,
    pass_calling_context: boolean,
    args: string // serialized call arguments
};

export interface DipoleResponse {
    action: string,
    call_id: string,
    call_return: string
};

export interface DipoleCall {
    call_request: DipoleRequest,
    call_id: string,
    promise_cbs: [(x: string) => void, (x: string) => void]
};

export interface DipoleMessage {
    call_id: string,
    action: string,
    action_args: DipoleRequest
};
