import example

#callback = example.Callback()
#example.setCallback(callback)
#example.doSomeWithCallback()

class PyCallback(example.Callback):
    def run(self, n):
        print 'This print from Python: n =', n

py_callback = PyCallback()
example.setCallback(py_callback)
example.doSomeWithCallback()
