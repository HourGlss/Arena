import socket
from server_client import Client
import random
import pickle
import time


def generate_options():
    numbers = [str(i) for i in range(10)]
    low_letters = [chr(97 + e) for e in range(0, 26)]
    high_letters = [chr(65 + e) for e in range(0, 26)]
    symbols = [chr(33 + e) for e in range(0, 15)]
    symbols2 = [chr(58 + e) for e in range(0, 7)]
    all_options = symbols2 + symbols + numbers + high_letters + low_letters
    return all_options


options = generate_options()


def generate_uid():
    uid = ""
    for i in range(20):
        uid += options[random.randint(0, len(options) - 1)]
    return uid


import socket
import pickle
import random
import time
import threading
import sys


class Server:
    sleep_time = .016
    to_send = None
    to_send_lock = False
    last_received = None
    last_received_lock = False

    clients = []

    def __init__(self):
        self.incoming_port = 5555
        self.outgoing_port = 5556
        self.incoming_addr = (self.host, self.incoming_port)
        self.outgoing_addr = (self.host, self.outgoing_port)
        outgoing = threading.Thread(target=self.outgoing)
        outgoing.start()
        incoming = threading.Thread(target=self.incoming)
        incoming.start()

    def set_uid(self, uid):
        self.uid = uid

    def incoming(self):
        incoming = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        incoming.bind(("", self.incoming_port))
        while True:
            if not self.last_received_lock:
                self.last_received_lock = True
                data_rec, addr_rec = incoming.recvfrom(1024)
                self.last_received = pickle.loads(data_rec)
                client_received_from = None
                for client in self.clients:
                    if client.addr == addr_rec:
                        if self.last_received['time_made'] > client.last_seen:
                            client.set_pos((self.last_received['x'], self.last_received['y']))
                            client.set_target((self.last_received['mouse_x'], self.last_received['mouse_y']))
                            client_received_from = client
                        break
                else:
                    print("Client connected", str(addr_rec))
                    client_to_add = Client(addr_rec, generate_uid())
                    client_to_add.set_pos((self.last_received['x'], self.last_received['y']))
                    self.clients.append(client_to_add)
                    client_received_from = client_to_add
                if client_received_from is None:
                    continue
                # print(data_rec)
                # print(self.last_received)
                self.last_received_lock = False
                time.sleep(self.sleep_time)
                if self.stop:
                    # print("xxx I BROKE THE LOOP")
                    break

    def stop_networking(self):
        # print("Calling stop")
        self.stop = True

    def outgoing(self):
        outgoing = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            if not self.to_send_lock:
                # print("within outgoing, wasnt locked")
                self.to_send_lock = True
                if self.to_send is not None:
                    # print("data was actually sent")
                    pickled = pickle.dumps(self.to_send)

                    outgoing.sendto(pickled, self.outgoing_addr)
                self.to_send_lock = False
                time.sleep(self.sleep_time)

                if self.stop:
                    # print("xxx I BROKE THE LOOP")
                    break

    def send(self, data_to_send):
        # print("net-udp trying to send")
        if not self.to_send_lock:
            # print("wasnt locked")
            self.to_send_lock = True
            self.to_send = data_to_send
            self.to_send_lock = False
            return True
        return False

    def receive(self):
        # print("receive is being called")
        if not self.last_received_lock:
            self.last_received_lock = True
            # print("it's not locked")
            if self.last_received is not None:
                # print("It isnt none")
                data_to_return = self.last_received
                # print(data_to_return)
                self.last_received = None
            else:
                # print("It is none")
                self.last_received_lock = False
                return False
            self.last_received_lock = False
            return data_to_return
        return False


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ''
incoming_port = 6555
try:
    s.bind((server, incoming_port))
    print("Starting this UDP server on", str(incoming_port))

except socket.error as e:
    print(str(e))
# print("we got here")
clients = []

while True:
    now = time.time()
    data_rec = None
    # print("wait for data")
    data_rec, addr_rec = s.recvfrom(1024)  # buffer size is 1024 bytes
    # print("never getting here")
    # print("data received",data_rec)
    data = pickle.loads(data_rec)
    client_received_from = None
    for client in clients:
        if client.addr == addr_rec:
            if data['time_made'] > client.last_seen:
                client.set_pos((data['x'], data['y']))
                client.set_target((data['mouse_x'], data['mouse_y']))
                client_received_from = client
            break
    else:
        print("Client connected", str(addr_rec))
        client_to_add = Client(addr_rec, generate_uid())
        print(addr_rec)
        client_to_add.set_pos((data['x'], data['y']))
        clients.append(client_to_add)
        client_received_from = client_to_add
    if client_received_from is None:
        continue
    client_received_from.last_seen = data['time_made']
    data_to_send = []
    for client in clients:
        if now - client.last_seen >= 3.5:
            print("Removing", client.addr, " -- ", client.uid)

            clients.remove(client)
        elif now - client.last_seen >= 3:
            if client.connected:
                print("attempting to drop", client.uid)
                client.connected = False

        if client.addr != addr_rec:
            data_to_send.append(client.get_status())
    data_to_send.insert(0, client_received_from.get_status())
    s.sendto(pickle.dumps(data_to_send), addr_rec)
