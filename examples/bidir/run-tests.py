import Ice, sys, time

Ice.loadSlice("--all -I{ICE_SLICE_DIR} ./Topics.ice".format(ICE_SLICE_DIR = Ice.getSliceDir()))
import Topics

class TopicSubscriberI(Topics.TopicSubscriber):
    def onTopicStateChange(self, topic_path, topic_state, curr = None):
        print topic_path, topic_state

if __name__ == "__main__":
    test_type = sys.argv[1]
    
    with Ice.initialize() as communicator:
        if test_type == "test-publisher":
            # round-robin test publisher
            port = 12345
            o_prx = communicator.stringToProxy("topics:ws -h localhost -p %d" % port)
            prx = Topics.TopicsSubscriptionsPrx.checkedCast(o_prx)
            test_topics = ["/a", "/a/b", "/b", "/b/c/d"]
            test_topic_states = ["NONE|", "OK|ok", "ERR|system failure"]
            while 1:
                for test_topic in test_topics:
                    for test_topic_state in test_topic_states:
                        prx.publish(test_topic, test_topic_state)
                        time.sleep(5)
        elif test_type in ["test-subscriber", "test-subscriberviaid"]:
            adapter = communicator.createObjectAdapterWithEndpoints("", "ws -p 0")
            adapter.activate()
            
            port = 12345
            o_prx = communicator.stringToProxy("topics:ws -h localhost -p %d" % port)
            center_prx = Topics.TopicsSubscriptionsPrx.checkedCast(o_prx)
            print "topics:", center_prx.getTopicPathes()
            print "topic states:"
            for topic in center_prx.getTopicPathes():
                print topic, "-->", center_prx.getTopicState(topic)
            print "start listening"

            obj = TopicSubscriberI()
            subscriber_o_prx = adapter.addWithUUID(obj)
            if test_type == "test-subscriber":
                subscriber_prx = Topics.TopicSubscriberPrx.uncheckedCast(subscriber_o_prx)
                center_prx.subscribeViaProxy(subscriber_prx)
            else: # test-subscriberviaid
                # this is secret sauce - get connection from existing proxy and connect it to adapter with callback object registered
                con = center_prx.ice_getCachedConnection()
                con.setAdapter(adapter)
                center_prx.subscribeViaIdentity(subscriber_o_prx.ice_getIdentity())
                
            communicator.waitForShutdown()
        else:
            raise Exception("unknown test_type %s" % test_type)
        

            
