class Client:
    def __init__(self, addr, uid):
        self.uid = uid
        self.addr = addr

    def set_pos(self, pos):
        self.x, self.y = pos
        self.pos = pos

    def __eq__(self, other):
        if self.addr == other.addr:
            return True
        return False

    def get_addr(self):
        return self.addr

    def get_status(self):
        return {'uid':self.uid,'x':self.x,'y':self.y}