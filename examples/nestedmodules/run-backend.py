import Ice, sys

Ice.loadSlice('--all -I. ./Hello.ice')
import Hello

class HelloI(Hello.HelloIfc):
    def sayHello(self, hello2_prx, current):
        print "Hello World!", hello2_prx
        return "Hello, World!"

class Hello2I(Hello.HelloIfc2):
    def sayHello2(self, hello_prx, current):
        print "Zdrastvuy Mir!", hello_prx
        return "Zdrastvuy Mir!"

    
if __name__ == "__main__":
    port = 10001
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        with Ice.initialize() as communicator:
            o_prx = communicator.stringToProxy("hello:ws -p %d" % port)
            prx = Hello.HelloIfcPrx.checkedCast(o_prx)
            o_prx = communicator.stringToProxy("hello2:ws -p %d" % port)
            prx2 = Hello.HelloIfc2Prx.checkedCast(o_prx)
            print prx.sayHello(prx2)
            print prx2.sayHello2(prx)
            sys.exit(0)

    print "running server at port", port
    with Ice.initialize() as communicator:
        adapter = communicator.createObjectAdapterWithEndpoints("", "ws -p %d" % port)
        adapter.add(HelloI(), Ice.stringToIdentity("hello"))
        adapter.add(Hello2I(), Ice.stringToIdentity("hello2"))
        adapter.activate()
        communicator.waitForShutdown()

