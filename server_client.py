class Client:
    x = 0
    y = 0
    target_x = 0
    target_y = 0
    address = None
    uid = None
    connected = True
    last_seen = None

    def __init__(self, addr, uid):
        # print("New client",addr)
        self.uid = uid
        self.address = addr

    def set_pos(self, pos):
        self.x, self.y = pos

    def set_target(self,pos):
        self.target_x,self.target_y = pos

    def __eq__(self, other):
        if self.address == other.addr:
            return True
        return False

    def get_addr(self):
        return self.address

    def get_status(self):
        #THIS IS OUTGOING DATA FROM THE SERVER
        return {'uid':self.uid,'x':self.x,'y':self.y,'mx':self.target_x,'my':self.target_y,'c':self.connected}

    def __repr__(self):
        return self.get_status()

    def __str__(self):
        return "{} - {}".format(self.uid,self.address)