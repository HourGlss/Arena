import pygame
import Utility


class Player:
    radius = 25
    uid = None

    # MOVEMENT
    acceleration_maximum = 5
    acceleration_minimum = -acceleration_maximum
    velocity_maximum = 15
    velocity_minimum = -velocity_maximum
    horizontal_velocity = 0
    vertical_velocity = 0
    horizontal_acceleration = 0
    vertical_acceleration = 0
    accelerate_tick_wait = 0
    accelerate_tick_wait_default = 5
    can_accelerate = False

    def __init__(self, startx, starty, color=(255, 0, 0)):
        self.x = startx
        self.y = starty
        self.color = color

    def request_movement(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        """
        # this controls your movement
        if dirn == 0:
            if self.can_accelerate:
                self.horizontal_acceleration += 1
                if self.horizontal_acceleration > self.acceleration_maximum:
                    self.horizontal_acceleration = self.acceleration_maximum
        elif dirn == 1:
            if self.can_accelerate:
                self.horizontal_acceleration -= 1
                if self.horizontal_acceleration < self.acceleration_minimum:
                    self.horizontal_acceleration = self.acceleration_minimum
        elif dirn == 2:
            if self.can_accelerate:
                self.vertical_acceleration -= 1
                if self.vertical_acceleration < self.acceleration_minimum:
                    self.vertical_acceleration = self.acceleration_minimum
        elif dirn == 3:
            if self.can_accelerate:
                self.vertical_acceleration += 1
                if self.vertical_acceleration > self.acceleration_maximum:
                    self.vertical_acceleration = self.acceleration_maximum
        elif dirn == 4:
            self.horizontal_velocity = 0
            self.vertical_velocity = 0
            self.horizontal_acceleration = 0
            self.vertical_acceleration = 0

    def draw(self, g):
        # your player
        pos = [self.x, self.y]
        pygame.draw.circle(g, self.color, pos, self.radius)

        # heathbar
        health_length = 20
        health_height = 3
        up = 40
        healthbar_vert = [self.x + health_length, (self.y - up) + health_height], [self.x - health_length,
                                                                                   (self.y - up) + health_height], [
                             self.x - health_length, (self.y - up) - health_height], [self.x + health_length,
                                                                                      (self.y - up) - health_height]
        pygame.draw.polygon(g, Utility.COLORS['RED'], healthbar_vert)

        # manabar
        mana_length = 20
        mana_height = 3
        up = 32
        manabar_vert = [self.x + mana_length, (self.y - up) + mana_height], [self.x - mana_length,
                                                                             (self.y - up) + mana_height], [
                           self.x - mana_length, (self.y - up) - mana_height], [self.x + mana_length,
                                                                                (self.y - up) - mana_height]
        pygame.draw.polygon(g, Utility.COLORS['DEEPSKYBLUE'], manabar_vert)