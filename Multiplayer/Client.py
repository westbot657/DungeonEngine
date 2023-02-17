# pylint: disable=[W,R,C,import-error]

from threading import Thread

import sys
import socket
import selectors
import types


class Client:
    
    def __init__(self, host, port):
        self.server_addr = (host, port)
        self.sel = selectors.DefaultSelector()
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_queue = []

    def connect(self):
        
        self.sock.setblocking(False)
        self.sock.connect_ex(self.server_addr)
        self.running = True
        self.sel.register(self.sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=None)
        
        self._inputThread = Thread(target=self.consoleInputThread)
        self._inputThread.start()
        
        self.mainLoop()

    def mainLoop(self):
        while self.running:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                self.update(key, mask)

    def update(self, key, mask):
        sock = key.fileobj
        #data = key.data
        if mask & selectors.EVENT_READ:
            try:
                recv_data = sock.recv(1024)  # Should be ready to read
            except ConnectionError:
                self.sel.unregister(sock)
                sock.close()
                self.running = False
                return
            if recv_data:
                print(f"Received {recv_data!r}") # do stuff with recieved data
                #data.recv_total += len(recv_data)
                ...
            if not recv_data:# or data.recv_total == data.msg_total:
                print("Closing connection")
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if self.send_queue:
                t = self.send_queue.pop(0)
                
                s = self.sock.send(t)
                if len(t) > 1024:
                    self.send_queue.insert(0, t[s:])


    def consoleInputThread(self):
        while self.running:
            i = input("> ")
            
            if i.strip():
                self.send_queue.append(i.strip().encode("utf-8")) # send data to the server


if __name__ == "__main__":
    c = Client("127.0.0.1", 5000)
    c.connect()
    