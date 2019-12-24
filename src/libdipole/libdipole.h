// -*- c++ -*-
//
#ifndef __LIBDIPOLE_HH__
#define __LIBDIPOLE_HH__

#include <string>
using namespace std;

class DipoleEventHandler {
public:
  virtual ~DipoleEventHandler() = 0;
  virtual void on_port_assignment(int assigned_port) = 0;
  virtual void on_connect() = 0;
  virtual string on_message(const char* message) = 0;
};   

namespace uWS {
  template <bool SSL> struct TemplatedApp;
  typedef struct TemplatedApp<false> App;
};

class DipoleServer {
 private:
  uWS::App* ws = 0;
  DipoleEventHandler* event_handler = 0;

 public:
  DipoleServer();
  void set_event_handler(DipoleEventHandler*);
  void run_listener(int port);
};

#endif
