%module(directors="1") dipolepy
%{
#include "dipolepy.h"
%}

%feature("director") DipoleEventHandler;

%include <std_string.i>
%include "dipolepy.h"
