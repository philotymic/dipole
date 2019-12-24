%module(directors="1") dipole_py
%{
#include "dipole_py.h"
%}

%feature("director") DipoleEventHandler;

%include <std_string.i>
%include "dipole_py.h"
