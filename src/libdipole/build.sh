rm -f *.so *.o *_wrap.* *.pyc mod_libdipole.py
swig -c++ -python -py3 libdipole.i
g++ --std=c++17 -c -fPIC libdipole.cpp libdipole_wrap.cxx -I/usr/local/anaconda3/include/python3.7m -I$HOME/uWebSockets/src -I$HOME/uWebSockets/uSockets/src

# uSockets
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/*.c
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/eventing/*.c
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/crypto/*.c

g++ -shared *.o -o _mod_libdipole.so -lz

#g++ -g -flto -lpthread -std=c++17 -I$HOME/uWebSockets/src -I$HOME/uWebSockets/uSockets/src MyEchoServer.cpp -o MyEchoServer $HOME/uWebSockets/uSockets/uSockets.a -lz
