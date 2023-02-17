# pylint: disable=[W,R,C,import-error]

from threading import Thread

import sys
import selectors
import socket
import types


HOST = "127.0.0.1"#socket.gethostname()
PORT = 5000



class Server:
    def __init__(self):
        self.server = None
        self.running = False
        self.connections = []
        
    def run(self):
        self.running = True
        self.sel = selectors.DefaultSelector()
        self.server = socket.socket()
        self.server.bind((HOST, PORT))
        self.server.listen(10)
        self.server.setblocking(False)
        self.sel.register(self.server, selectors.EVENT_READ, data=None)
        self.event_loop()
        
    def event_loop(self):
        while self.running:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)
    
    def accept_wrapper(self, sock):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.connections.append(conn)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            try:
                recv_data = sock.recv(1024)
            except ConnectionError:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()
                self.connections.remove(sock)
                return
            if recv_data:
                print(f"Recieved {data.outb!r}")
                data.outb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()
                self.connections.remove(sock)
                return
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                #sent = sock.send("{}".encode("utf-8"))
                sent = sock.send(data.outb) # Send data to client that data was recieved from
                for conn in self.connections:
                    if conn is sock: continue
                    conn.send(data.outb) # Send data to all clients except the one that data was recieved from
                data.outb = data.outb[sent:]

s = Server()

s.run()

