import pygame
class Player:
    radius = 25
    uid = None
    ticks_until_acceleration_default = 5
    ticks_until_acceleration = 5

    def __init__(self,startx, starty, color=(255, 0, 0)):
        self.x = startx
        self.y = starty
        self.color = color
        self.accelerate_north = 0
        self.accelerate_south = 0
        self.accelerate_east = 0
        self.accelerate_west = 0
        self.velocity_north = 0
        self.velocity_south = 0
        self.velocity_east = 0
        self.velocity_west = 0

    def draw(self, g):
        pos = [self.x, self.y]
        pygame.draw.circle(g, self.color, pos, self.radius)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        """
        #this controls your movement
        n = False
        e = False
        s = False
        w = False
        if dirn == 0:
            self.velocity_east += self.accelerate_east
            e= True
            self.x += self.velocity_east
        elif dirn == 1:
            self.velocity_west += self.accelerate_west
            w = True
            self.x -= self.velocity_west
        elif dirn == 2:
            self.velocity_north += self.accelerate_north
            n = True
            self.y -= self.velocity_north
        elif dirn == 3:
            self.velocity_south += self.accelerate_south
            s = True
            self.y += self.velocity_south
        else:
            if not n:
                self.velocity_north -= 10
            if not s:
                self.velocity_south -= 10
            if not e:
                self.velocity_east -= 10
            if not w:
                self.velocity_west -= 10
