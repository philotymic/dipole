import ipdb
import sys, os
import prctl, signal
from flask import Flask
from flask_socketio import SocketIO, emit
import json, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#@dipole.exportclass
class Hello:
    def sayHello(self):
        print "Hello World!"
        return "Hello, World!"

    def sayAloha(self, language):
        print "Aloha"
        return language + "Ahoha"

class Dispatcher:
    def __init__(self):
        self.objects = {}

    def add_object(self, object_id, obj):
        self.objects[object_id] = obj

dispatcher = Dispatcher()
        
@socketio.on('connect')
def on_connect():
    print('user connected')    
    #emit('topics', {'/status': 'INIT'}, broadcast=True)

@socketio.on('remote-call')
def on_remote_call(call_args):
    print 'on_remote_call:', call_args
    #ipdb.set_trace()
    call_id = call_args['call_id']
    object_id = call_args['obj_id']
    method = call_args['call_method']
    args = call_args['args']
    
    obj = dispatcher.objects[object_id]
    b_method = getattr(obj, method)
    ret = None; exc = None
    ret = b_method(**args)
    print "ret:", ret, call_id

    socketio.emit('remote-call-response', {'call_id': call_id, 'ret': ret})
    
if __name__ == "__main__":
    port = 8080
    if 0:
        # https://github.com/seveas/python-prctl -- prctl wrapper module
        # more on pdeathsignal: https://stackoverflow.com/questions/284325/how-to-make-child-process-die-after-parent-exits
        prctl.set_pdeathsig(signal.SIGTERM) # if parent dies this child will get SIGTERM

        xfn_fn = sys.argv[1]
        print "running server at port", port
        xfn_fd = open(xfn_fn, "w+b")
        print >>xfn_fd, port
        xfn_fd.close()
        sys.stdout.flush()

    print "adding object Hello"
    dispatcher.add_object("Hello", Hello())
    
    # server
    socketio.run(app, host = "localhost", port = port, debug = True)
