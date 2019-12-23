// -*- c++ -*-
//
#ifndef __MYWS_HH__
#define __MYWS_HH__

#include <memory>
using namespace std;

class MyWSEventHandler {
public:
  MyWSEventHandler() {}
  virtual ~MyWSEventHandler();

  virtual void on_port_assignment(int assigned_port) = 0;
  virtual void on_connect() = 0;
  virtual string on_message(const char* message) = 0;
};   

namespace uWS {
  template <bool SSL> struct TemplatedApp;
  typedef struct TemplatedApp<false> App;
};

class MyWSServer {
 private:
  uWS::App* ws = 0;
  MyWSEventHandler* event_handler = 0;

 public:
  MyWSServer();
  void set_event_handler(MyWSEventHandler*);
  void run_listener(int port);
};

#endif
