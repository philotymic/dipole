// -*- mode: C++ -*-
//

module Hello {
  interface HelloIfc;     
  interface HelloIfc2 {
    string sayHello2(HelloIfc* prx);
  };
};
