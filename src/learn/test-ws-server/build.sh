# uSockets
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/*.c
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/eventing/*.c
gcc -c -fPIC -DLIBUS_NO_SSL -I$HOME/uWebSockets/uSockets/src $HOME/uWebSockets/uSockets/src/crypto/*.c

g++ -g -flto -lpthread -std=c++17 -I$HOME/uWebSockets/src -I$HOME/uWebSockets/uSockets/src MyEchoServer.cpp -o MyEchoServer *.o -lz
