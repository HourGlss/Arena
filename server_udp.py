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


print("Starting UDP server")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ''
port = 5555

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

clients = []
currentId = "0"

while True:
    now = time.time()
    data_rec, addr_rec = s.recvfrom(1024)  # buffer size is 1024 bytes
    # print(addr_rec)
    data = pickle.loads(data_rec)
    # print(data)
    client_received_from = None
    for client in clients:
        if client.addr == addr_rec:
            client.set_pos((data['x'], data['y']))
            client.set_target((data['mouse_x'],data['mouse_y']))
            client_received_from = client
            break
    else:
        client_to_add = Client(addr_rec, generate_uid())
        client_to_add.set_pos((data['x'], data['y']))
        clients.append(client_to_add)
        client_received_from = client_to_add
    client_received_from.last_seen = time.time()
    data_to_send = []
    for client in clients:
        if now - client.last_seen >= 10:
            # print("removing",client.uid)
            clients.remove(client)

        if client.addr != addr_rec:
            data_to_send.append(client.get_status())
    data_to_send.insert(0,client_received_from.get_status())
    s.sendto(pickle.dumps(data_to_send), addr_rec)
