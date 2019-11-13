# python run-backend.py               -- publish/subscriber server
# python run-tests.py test-publish    -- publisher
# python run-tests.py test-subscriber -- subscriber
#
import Ice, sys

Ice.loadSlice("--all -I{ICE_SLICE_DIR} ./Topics.ice".format(ICE_SLICE_DIR = Ice.getSliceDir()))
import Topics

class TopicSubscriptionsI(Topics.TopicsSubscriptions):
    def __init__(self):
        self.topics = {} # topic -> text
        self.subscribers = [] # proxies to TopicSubsriber objects
        
    def getTopicPathes(self, curr = None):
        return self.topics.keys()

    def getTopicState(self, topic_path, curr = None):
        return self.topics[topic_path] if topic_path in self.topics else None

    def publish(self, topic_path, topic_state, curr = None):
        print "TopicSubscriptionsI::publish:", topic_path, topic_state, len(self.subscribers)
        self.topics[topic_path] = topic_state
        for subscriber in self.subscribers[:]:
            try:
                subscriber.onTopicStateChange(topic_path, topic_state)
            except Ice.Exception as ex:
                print "ice exception:", ex
                self.subscribers.remove(subscriber)
                print "len of subscriber:", len(self.subscribers)

    def subscribeViaProxy(self, subscriber_prx, curr = None):
        print "TopicsSubscriptionsI::subscribeViaProxy:", subscriber_prx
        self.subscribers.append(subscriber_prx)

    def subscribeViaIdentity(self, subscriber_id, curr = None):
        print "TopicsSubscriptionsI::subscribeViaIdentity:", subscriber_id
        #subscriber_ice_identity = Ice.Identity(name = subscriber_id)
        bidir_prx = Topics.TopicSubscriberPrx.uncheckedCast(curr.con.createProxy(subscriber_id))
        self.subscribers.append(bidir_prx)
        
if __name__ == "__main__":
    port = 12345

    props = Ice.createProperties()
    props.setProperty("Ice.ThreadPool.Server.Size", "2")
    props.setProperty("Ice.ACM.Close", "0")
    props.setProperty("Ice.MessageSizeMax", "0")
    #props.setProperty("Ice.Trace.Protocol", "1")
    #props.setProperty("Ice.Trace.Network", "3")

    init_data = Ice.InitializationData()
    init_data.properties = props

    with Ice.initialize(sys.argv, init_data) as communicator:
        # server
        print "running server at port", port
        adapter = communicator.createObjectAdapterWithEndpoints("", "ws -p %d" % port)
        adapter.add(TopicSubscriptionsI(), Ice.stringToIdentity("topics"))
        adapter.activate()
        communicator.waitForShutdown()
        
        

