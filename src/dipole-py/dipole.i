%module(directors="1") dipole
%{
#include "dipole.h"
%}

%feature("director") DipoleEventHandler;

%include <std_string.i>
%include "dipole.h"
