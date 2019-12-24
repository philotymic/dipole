// -*- c++ -*-
//

class Callback{
public:
  virtual void run(int n) = 0;
  virtual ~Callback() = 0; 
};   

class CallBacker {
  Callback* callback = 0;

public:
  void doSomeWithCallback();
  void setCallback(Callback * cb);
};

