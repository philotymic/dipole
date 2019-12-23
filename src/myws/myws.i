%module(directors="1") myws
%{
#include "myws.h"
%}

%feature("director") MyWSEventHandler;

%include <std_string.i>
%include "myws.h"
