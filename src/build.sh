rm -f *.so *.o *_wrap.* *.pyc
swig -c++ -python example.i
g++ -Wall --std=c++17 -c -fPIC example.cpp example_wrap.cxx -I/usr/local/anaconda2/include/python2.7
g++ -shared example.o example_wrap.o -o _example.so
