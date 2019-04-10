import time
class GameData:

    def __init__(self,player):
        self.x = player.x
        self.y =player.y
        self.mx = player.target_x
        self.my = player.target_y
        self.health = player.health
        self.mana = player.mana
        self.time_made = time.time()

    def get_dictionary(self):
        return {"x": self.x,
                'y': self.y,
                'mouse_x': self.mx,
                'mouse_y': self.my,
                'health':self.health,
                'mana':self.mana,
                'time_made':self.time_made
                }