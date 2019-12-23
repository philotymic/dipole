%module(directors="1") myws
%{
#include "myws.h"
%}

%feature("director") MyWSEventHandler;

%include "myws.h"
