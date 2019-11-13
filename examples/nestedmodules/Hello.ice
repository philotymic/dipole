// -*- mode: C++ -*-
//

#include <Hello2.ice>

module Hello {
  interface HelloIfc2;
  interface HelloIfc {
    string sayHello(HelloIfc2* prx);
  };
};

