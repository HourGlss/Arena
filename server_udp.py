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


print("Starting this UDP server on 5555")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ''
incoming_port = 5555
outgoing_port = 5556
try:
    s.bind((server, incoming_port))

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
                client.set_target((data['mouse_x'],data['mouse_y']))
                client_received_from = client
            break
    else:
        print("Client connected",str(addr_rec))
        client_to_add = Client(addr_rec, generate_uid())
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
                print("attempting to drop",client.uid)
                client.connected = False

        if client.addr != addr_rec:
            data_to_send.append(client.get_status())
    data_to_send.insert(0,client_received_from.get_status())
    addr_rec = list(addr_rec)
    addr_rec[1] = 5556
    addr_rec = tuple(addr_rec)
    s.sendto(pickle.dumps(data_to_send), addr_rec)
