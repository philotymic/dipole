%module(directors="1") libdipole
%{
#include "libdipole.h"
%}

%feature("director") DipoleEventHandler;

%include <std_string.i>
%include "libdipole.h"
