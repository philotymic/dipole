g++ -g -flto -lpthread -std=c++17 -I$HOME/uWebSockets/src -I$HOME/uWebSockets/uSockets/src MyEchoServer.cpp -o MyEchoServer $HOME/uWebSockets/uSockets/uSockets.a -lz
