%module(directors="1") mod_libdipole
%{
#include "libdipole.h"
%}

%feature("director") DipoleEventHandler;

%feature("director:except") {
    if ($error != NULL) {
        throw Swig::DirectorMethodException();
    }
}

%exception {
    try { $action }
    catch (Swig::DirectorException &e) { SWIG_fail; }
}

%include <std_string.i>
%include "libdipole.h"
