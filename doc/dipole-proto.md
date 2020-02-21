Serialized call request has JSON form as below. Callee object identified by obj_id is used to perform method call. Method is identified by call_method.

```
{
 call_id: string, // uniq call id assigned by caller
 action: string, // remote-call
 action-args: {
  obj_id: string, // callee object id, used to lookup callee object
  call_method: string, // callee method
  pass_calling_context: boolean, // should ObjectServer add ctx argument
  args: string // serialized arguments used to make method call
 }
}
```
