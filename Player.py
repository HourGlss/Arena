import pygame
class Player:
    radius = 25
    uid = None

    def __init__(self,startx, starty, color=(255, 0, 0)):
        self.x = startx
        self.y = starty
        self.color = color
        self.velocity = 7

    def draw(self, g):
        #your player
        pos = [self.x, self.y]
        pygame.draw.circle(g, self.color, pos, self.radius)

        #heathbar
        health_length = 20
        height = 3
        up = 35
        healthbar_vert = [self.x + length, (self.y - up) + height], [self.x - length, (self.y - up) + height], [
            self.x - length, (self.y - up) - height], [self.x + length, (self.y - up) - height]
        pygame.draw.polygon(g, pygame.Color(255, 0, 0), healthbar_vert)

        #manabar
        length = 20
        height = 3
        up = 35
        healthbar_vert = [self.x + length, (self.y - up) + height], [self.x - length, (self.y - up) + height], [
            self.x - length, (self.y - up) - height], [self.x + length, (self.y - up) - height]
        pygame.draw.polygon(g, pygame.Color(255, 0, 0), healthbar_vert)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        """
        #this controls your movement
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        elif dirn == 3:
            self.y += self.velocity
        else:
            print("Direction is off.")
