from server_client import Client
import socket
import pickle
import random
import time
import threading
import sys


class Server:
    sleep_time = .016
    last_received = None
    clients_lock = False
    stop = False
    clients = []

    options = None

    def __init__(self):
        self.outgoing_port = 6555
        self.options = self.generate_options()
        outgoing = threading.Thread(target=self.outgoing)
        outgoing.start()
        incoming = threading.Thread(target=self.incoming)
        incoming.start()
        self.run()

    def generate_options(self):
        numbers = [str(i) for i in range(10)]
        low_letters = [chr(97 + e) for e in range(0, 26)]
        high_letters = [chr(65 + e) for e in range(0, 26)]
        symbols = [chr(33 + e) for e in range(0, 15)]
        symbols2 = [chr(58 + e) for e in range(0, 7)]
        all_options = symbols2 + symbols + numbers + high_letters + low_letters
        return all_options

    def run(self):
        while True:
            time.sleep(self.sleep_time)
            now = time.time()
            if not self.clients_lock:
                # print("main game loop")
                self.clients_lock = True
                for i in range(len(self.clients)):
                    client = self.clients[i]
                    if now - client.last_seen >= 3.5:
                        print("Removing", client.address, " -- ", client.uid)

                        self.clients.remove(client)
                    elif now - client.last_seen >= 3:
                        if client.connected:
                            print("Attempting to drop", client.uid)
                            client.connected = False
                self.clients_lock = False

    def generate_uid(self):
        uid = ""
        for i in range(4):
            uid += self.options[random.randint(0, len(self.options) - 1)]
        return uid

    def incoming(self):
        # print("start incoming")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = ''
        try:
            s.bind((server, self.outgoing_port))
            print("Starting this UDP server on", str(self.outgoing_port))

        except socket.error as e:
            print(str(e))
        while True:
            time.sleep(self.sleep_time)
            data_received ,address_received_from = s.recvfrom(1024)
            self.last_received = pickle.loads(data_received)
            if not self.clients_lock:
                # print("incoming loop")
                self.clients_lock = True
                client_received_from = None
                for client in self.clients:
                    if client.address == address_received_from:
                        if self.last_received['time_made'] > client.last_seen:
                            client.set_pos((self.last_received['x'], self.last_received['y']))
                            client.set_target((self.last_received['mouse_x'], self.last_received['mouse_y']))
                            client_received_from = client
                        break
                else:
                    print("New client connected", str(address_received_from))
                    client_to_add = Client(address_received_from, self.generate_uid())
                    client_to_add.set_pos((self.last_received['x'], self.last_received['y']))
                    client_to_add.set_target((self.last_received['mouse_x'], self.last_received['mouse_y']))
                    self.clients.append(client_to_add)
                    client_received_from = client_to_add
                if client_received_from is None:
                    continue
                client_received_from.last_seen = self.last_received['time_made']
                self.clients_lock = False


            if self.stop:
                # print("xxx I BROKE THE LOOP")
                break

    def outgoing(self):
        # print("start outgoing")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            time.sleep(self.sleep_time)
            now = time.time()
            if not self.clients_lock:
                self.clients_lock = True
                # print("outgoing loop")
                for i in range(len(self.clients)):
                    client = self.clients[i]
                    self.clients.remove(client)
                    self.clients.insert(0, client)
                    # print("currently sending to",str(client))
                    pickled = pickle.dumps([c.get_status() for c in self.clients])
                    # print("Data looks like",str(pickled))
                    s.sendto(pickled, client.address)
                    self.clients.remove(client)
                    self.clients.insert(i, client)

                self.clients_lock = False

    def stop_networking(self):
        # print("Calling stop")
        self.stop = True


if __name__ == "__main__":
    s = Server()
