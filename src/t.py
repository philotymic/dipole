import example

callback = example.Callback()
example.setCallback(callback)
example.doSomeWithCallback()

class Callback(example.Callback):
    def run(self, n):
        print 'This print from Python: n =', n

callback = Callback()
example.setCallback(callback)
example.doSomeWithCallback()
