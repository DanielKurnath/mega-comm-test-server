import socketserver
import logging

logging.basicConfig(level=logging.INFO)

class MegaHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logging.info(f"Connection from {self.client_address}")
        buffer = ""
        while True:
            data = self.request.recv(1)
            if not data:
                break
            char = data.decode(errors="ignore")
            buffer += char
            if char == '\n':
                message = buffer.strip()
                logging.info(f"Received: {message}")
                if message == "CMD:RESET":
                    logging.info(f"CMD:RESET received — closing connection from {self.client_address}")
                    break  # Gracefully close connection
                self.request.sendall(b'O')  # ACK
                buffer = ""

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 4000
    with ThreadedTCPServer((HOST, PORT), MegaHandler) as server:
        logging.info(f"Listening on {HOST}:{PORT}")
        server.serve_forever()
