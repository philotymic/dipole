// -*- mode: C++ -*-
//

#include <Ice/BuiltinSequences.ice>
#include <Ice/Identity.ice>

module Topics {
  //sequence<string> StringSeq;
  interface TopicSubscriber;
  interface TopicsSubscriptions {
    Ice::StringSeq getTopicPathes();
    string getTopicState(string topicPath);
    
    void publish(string topicPath, string newTopicState);
    void subscribeViaProxy(TopicSubscriber* subscriber);
    void subscribeViaIdentity(Ice::Identity subscriberId);
  };

  interface TopicSubscriber {
    void onTopicStateChange(string topicPath, string newTopicState);
  };
};
