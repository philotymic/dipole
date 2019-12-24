import example

class PyCallback(example.Callback):
    def run(self, n):
        print 'This print from Python: n =', n

py_callback = PyCallback()
cber = example.CallBacker()
cber.setCallback(py_callback)
cber.doSomeWithCallback()
