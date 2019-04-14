import socket
import pickle
import random
import time
import config
import threading
import sys

class Network:
    uid = None
    sleep_time = .016
    to_send = None
    socket_lock = False
    last_received = None
    last_received_lock = False
    to_send_lock = False
    data_has_been_sent = False
    stop = False
    sequence_number = 0
    def __init__(self):
        self.host = config.host_ip
        self.outgoing_port = 6555
        self.outgoing_addr = (self.host, self.outgoing_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(0)
        outgoing = threading.Thread(target=self.outgoing,args = (sock,))
        outgoing.start()
        incoming = threading.Thread(target=self.incoming,args = (sock,))
        incoming.start()


    def set_uid(self, uid):
        self.uid = uid

    def incoming(self,sock):
        # print("start incoming")
        while True:
            time.sleep(self.sleep_time)
            if not self.socket_lock:
                # print("incoming, socket wasnt locked, now it is")

                self.socket_lock = True
                data_rec = None
                if self.data_has_been_sent:
                    try:
                        print("waiting to receive")
                        data_rec,addr_rec = sock.recvfrom(1024)

                        self.last_received = pickle.loads(data_rec)
                        print(self.last_received)
                        # print(data_rec)
                        # print("incoming received",self.last_received)
                        if self.uid is None:
                            self.set_uid(self.last_received[0]['uid'])
                    except Exception as e:
                        print("incoming",e)

                self.socket_lock = False
                # print("incoming, socket wasnt locked, now it isnt")


                if self.stop:
                    # print("xxx I BROKE THE LOOP")
                    break



    def outgoing(self,sock):
        # print("start outgoing")

        while True:
            time.sleep(self.sleep_time)
            if not self.socket_lock:

                self.socket_lock = True
                # print("outgoing, socket wasnt locked, now it is")
                if not self.to_send_lock:
                    self.to_send_lock = True
                    if self.to_send is not None:

                        # print("outgoing ",self.to_send)
                        pickled = pickle.dumps(self.to_send)
                        print(self.to_send)
                        self.to_send = None
                        self.data_has_been_sent = True
                        try:
                            sock.sendto(pickled, self.outgoing_addr)
                        except Exception as e:
                            print("outgoing",e)
                    else:
                        # print("but there was no data to send")
                        pass
                    self.to_send_lock = False
                    # print(self.to_send)

                    # print("outgoing sent", self.to_send)


                self.socket_lock = False
                # print("outgoing, socket wasnt locked, now it isnt")



                if self.stop:
                    # print("xxx I BROKE THE LOOP")
                    break

    def stop_networking(self):
        # print("Calling stop")
        self.stop = True

    def send(self, data_to_send):
        # print("send trying to send")
        if not self.to_send_lock:
            # print("send wasnt locked")
            self.to_send_lock = True
            if self.sequence_number >= 600:
                self.sequence_number = 0
            data_to_send['s'] = self.sequence_number
            self.sequence_number+=1
            self.to_send = data_to_send
            self.to_send_lock = False
            return True
        return False

    def receive(self):
        # print("receive is being called")
        if not self.last_received_lock:
            self.last_received_lock = True
            # print("receive it's not locked")
            if self.last_received is not None:
                # print("receive It isnt none")
                data_to_return = self.last_received
                # print(data_to_return)
                self.last_received = None
            else:
                # print("receive It is none")
                self.last_received_lock = False
                return False
            self.last_received_lock = False
            return data_to_return
        return False
#FIRST POC
# UDP_IP = "127.0.0.1"
# UDP_PORT = 5555
# MESSAGE = "Hello, World!"
#
# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
# data,addr = sock.recvfrom(2048)
# print(data.decode())


#SECOND POC
# N = Network()
# last_sent = None
# while True:
#     now = time.time()
#     if last_sent == None or now - last_sent >= .06:
#         data_to_send = {"x": random.randint(0, 1024), 'y': random.randint(0, 768),'mouse_x':random.randint(0, 768),'mouse_y':random.randint(0, 768)}
#         response = False
#         response = N.send(data_to_send)
#         if response:
#             # print("data was Qd to be sent")
#             pass
#         received = N.recieve()
#         if received != False:
#             # print("was received",received)
#             pass
#
#         # print("My UID is {}".format(N.uid))
#         last_sent = now
