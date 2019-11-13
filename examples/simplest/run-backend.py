#import ipdb
import Ice, sys

Ice.loadSlice('--all -I. ./Hello.ice')
import Hello

class HelloI(Hello.HelloIfc):
    def sayHello(self, current):
        print "Hello World!"
        return "Hello, World!"
    
if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        with Ice.initialize() as communicator:
            o_prx = communicator.stringToProxy("hello:ws -p %d" % port)
            prx = Hello.HelloIfcPrx.checkedCast(o_prx)
            print prx.sayHello()
            sys.exit(0)

    port = 0
    print "running server at port", port
    with Ice.initialize() as communicator:
        # set port to zero to make automatic choice
        adapter = communicator.createObjectAdapterWithEndpoints("", "ws -p %d" % port)
        # shows information about endpoint
        for ep in adapter.getEndpoints():
            ep_info = ep.getInfo()
            #ipdb.set_trace()
            print 'port:', ep_info.underlying.port
        adapter.add(HelloI(), Ice.stringToIdentity("hello"))
        adapter.activate()
        communicator.waitForShutdown()

