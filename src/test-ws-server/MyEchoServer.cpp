#include "App.h"
#include <iostream>
using namespace std;

/* This is a simple WebSocket echo server example.
 * You may compile it with "WITH_OPENSSL=1 make" or with "make" */

int main() {
    /* ws->getUserData returns one of these */
    struct PerSocketData {
        /* Fill with user data */
    };

    /* Keep in mind that uWS::SSLApp({options}) is the same as uWS::App() when compiled without SSL support.
     * You may swap to using uWS:App() if you don't need SSL */
    uWS::App().ws<PerSocketData>("/*", {
        /* Settings */
        .compression = uWS::DISABLED,
        .maxPayloadLength = 16 * 1024,
        .idleTimeout = 10000,
        .maxBackpressure = 1 * 1024 * 1204,
        /* Handlers */
        .open = [](auto *ws, auto *req) {
            /* Open event here, you may access ws->getUserData() which points to a PerSocketData struct */
	  cerr << "open" << endl;
        },
        .message = [](auto *ws, std::string_view message, uWS::OpCode opCode) {
	  cerr << "getBufferedAmount: " << ws->getBufferedAmount() << endl;
	  cerr << "message: " << message << endl;
	  auto send_res = ws->send(message, opCode);
	  cerr << "send_res: " << send_res << endl;
        },
        .drain = [](auto *ws) {
            /* Check ws->getBufferedAmount() here */
	  cerr << "drain: " << ws->getBufferedAmount() << endl;
        },
        .ping = [](auto *ws) {
            /* Not implemented yet */
        },
        .pong = [](auto *ws) {
            /* Not implemented yet */
        },
        .close = [](auto *ws, int code, std::string_view message) {
            /* You may access ws->getUserData() here */
        }
    }).listen(9001, [](auto *token) {
        if (token) {
            std::cout << "Listening on port " << 9001 << std::endl;
        }
    }).run();
}
