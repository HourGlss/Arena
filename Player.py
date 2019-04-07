import pygame
import Utility
class Player:
    radius = 25
    uid = None
    acceleration_max = 5
    acceleration_minimum = -acceleration_max
    velocity_max = 15
    velocity_minimum = -velocity_max
    horizontal_velocity = 0
    vertical_velocity = 0
    horizontal_acceleration = 0
    vertical_acceleration = 0


    def __init__(self,startx, starty, color=(255, 0, 0)):
        self.x = startx
        self.y = starty
        self.color = color

    def draw(self, g):
        #your player
        pos = [self.x, self.y]
        pygame.draw.circle(g, self.color, pos, self.radius)

        #heathbar
        health_length = 20
        health_height = 3
        up = 40
        healthbar_vert = [self.x + health_length, (self.y - up) + health_height], [self.x - health_length, (self.y - up) + health_height], [
            self.x - health_length, (self.y - up) - health_height], [self.x + health_length, (self.y - up) - health_height]
        pygame.draw.polygon(g, pygame.Color(255, 0, 0), healthbar_vert)

        #manabar
        mana_length = 20
        mana_height = 3
        up = 32
        manabar_vert = [self.x + mana_length, (self.y - up) + mana_height], [self.x - mana_length, (self.y - up) + mana_height], [
            self.x - mana_length, (self.y - up) - mana_height], [self.x + mana_length, (self.y - up) - mana_height]
        pygame.draw.polygon(g, pygame.Color(0, 0, 255), manabar_vert)

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
