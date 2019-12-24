#include <iostream>
#include "example.h"

Callback::~Callback()
{
}

int n = 0;

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
