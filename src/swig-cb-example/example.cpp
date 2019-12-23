#include <iostream>
#include "example.h"

int n = 0;

void Callback::run(int n)
{ 
  std::cout << "This print from C++: n = " << n << std::endl;
}   

void CallBacker::setCallback(Callback * cb)
{
  callback = cb; 
}    

void CallBacker::doSomeWithCallback()
{
  if (callback == NULL){
    std::cout << "Must set callback first!" << std::endl;
  } else {
    callback->run(n++);
  }
}
