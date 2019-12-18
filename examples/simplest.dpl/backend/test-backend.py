import sys
import socketio

sio = socketio.Client()

@sio.on('remote-call-response')
def remote_call_response(response):
    print 'remote_call_response:', response

if __name__ == "__main__":
    sio.connect('http://localhost:8080')
    sio.emit('remote-call', {'obj_id': 'Hello', 'call_method': 'sayHello', 'args': {}})
    #sio.emit('remote-call', {'obj_id': 'Hello', 'call_method': 'sayAloha', 'args': {'language': 'russian'}})
    sio.wait()
    
