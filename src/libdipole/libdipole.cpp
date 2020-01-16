#include "libdipole.h"
#include <App.h>

#include <internal/internal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>

DipoleEventHandler::~DipoleEventHandler()
{
}

DipoleServer::DipoleServer()
{
  this->ws = new uWS::App();
}

void DipoleServer::set_event_handler(DipoleEventHandler* eh)
{
  this->event_handler = eh;
}

void DipoleServer::run_listener(int port)
{
  struct PerSocketData {
  };

  this->ws->ws<PerSocketData>("/*", {
      /* Settings */
      .compression = uWS::DISABLED,
        .maxPayloadLength = 16 * 1024,
        .idleTimeout = 10000,
        .maxBackpressure = 1 * 1024 * 1204,
        /* Handlers */
        .open = [this](auto *ws, auto *req) {
	/* Open event here, you may access ws->getUserData() which points to a PerSocketData struct */
	this->event_handler->on_connect();
      },
        .message = [this](auto *ws, std::string_view message, uWS::OpCode opCode) {
	string message_s(message.begin(), message.end());
	string event_handler_res = this->event_handler->on_message(message_s.c_str());
	cerr << "event_handler->on_message returns: " << event_handler_res << endl;
	ws->send(event_handler_res, opCode);
	
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
    }).listen(port, [this](auto* l) {
	int sock_fd = l->s.p.state.fd;
	struct sockaddr_in sin;
	socklen_t len = sizeof(sin);
	if (::getsockname(sock_fd, (sockaddr*)&sin, &len) == -1) {
	  throw new runtime_error("getsockname error");	  
	}
	int assigned_port = ::ntohs(sin.sin_port);
	this->event_handler->on_port_assignment(assigned_port);
      }).run();
}
