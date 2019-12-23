rm -f *.so *.o *_wrap.* *.pyc
swig -c++ -python myws.i
g++ --std=c++17 -c -fPIC myws.cpp myws_wrap.cxx -I/usr/local/anaconda2/include/python2.7 -I$HOME/uWebSockets/src -I$HOME/uWebSockets/uSockets/src

# uSockets
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/*.c
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/eventing/*.c
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/crypto/*.c

g++ -shared *.o -o _myws.so -lz

#g++ -g -flto -lpthread -std=c++17 -I$HOME/uWebSockets/src -I$HOME/uWebSockets/uSockets/src MyEchoServer.cpp -o MyEchoServer $HOME/uWebSockets/uSockets/uSockets.a -lz
