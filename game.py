import pygame
from networkUDP import Network
from Player import Player
import Utility
import sys
import time
import math
from GameData import GameData

window = (1920, 1080)

class Game:
    tiltAngle = 0
    players = []

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(int(self.width / 2), int(self.height / 2))
        self.canvas = Canvas(self.width, self.height, "Testing...")
        # pygame.mouse.set_visible(False)
        self.players.append(self.player)
    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.net.stop_networking()
                    run = False

                if event.type == pygame.K_ESCAPE:
                    self.net.stop_networking()
                    run = False

            keys = pygame.key.get_pressed()

            # this controls movement

            if self.player.accelerate_tick_wait == 0:
                self.player.can_accelerate = True
                self.player.accelerate_tick_wait = self.player.accelerate_tick_wait_default
            self.player.accelerate_tick_wait -= 1

            if keys[pygame.K_d]:
                self.player.request_movement(0)

            if keys[pygame.K_a]:
                self.player.request_movement(1)

            if keys[pygame.K_w]:
                self.player.request_movement(2)

            if keys[pygame.K_s]:
                self.player.request_movement(3)

            if keys[pygame.K_x]:
                self.player.request_movement(4)
            # FRICTION for velocity
            if self.player.horizontal_velocity > 0:
                self.player.horizontal_velocity = self.player.horizontal_velocity - self.player.horizontal_velocity / 2
            elif self.player.horizontal_velocity < 0:
                self.player.horizontal_velocity = self.player.horizontal_velocity + abs(
                    self.player.horizontal_velocity) / 2

            if self.player.vertical_velocity > 0:
                self.player.vertical_velocity = self.player.vertical_velocity - self.player.vertical_velocity / 3
            elif self.player.vertical_velocity < 0:
                self.player.vertical_velocity = self.player.vertical_velocity + abs(self.player.vertical_velocity) / 3


            self.player.vertical_velocity = int(self.player.vertical_velocity)
            self.player.horizontal_velocity = int(self.player.horizontal_velocity)
            self.player.vertical_acceleration = int(self.player.vertical_acceleration)
            self.player.horizontal_acceleration = int(self.player.horizontal_acceleration)

            self.player.horizontal_velocity += self.player.horizontal_acceleration
            if self.player.horizontal_velocity > self.player.velocity_maximum:
                self.player.horizontal_velocity = self.player.velocity_maximum
            elif self.player.horizontal_velocity < self.player.velocity_minimum:
                self.player.horizontal_velocity = self.player.velocity_minimum
            requested_x = self.player.x + self.player.horizontal_velocity

            self.player.vertical_velocity += self.player.vertical_acceleration
            if self.player.vertical_velocity > self.player.velocity_maximum:
                self.player.vertical_velocity = self.player.velocity_maximum
            elif self.player.vertical_velocity < self.player.velocity_minimum:
                self.player.vertical_velocity = self.player.velocity_minimum
            requested_y = self.player.y + self.player.vertical_velocity
            # DETECT COLLISION AND ALLOW OR NOT. If collision happens, move the player to the "wall" and then stop acceleration and velocity

            # MAY NEED TO check with radius
            if requested_x <= self.width - (self.player.radius*2):
                # ALLOW
                self.player.x = requested_x
            else:
                self.player.x = self.width - (self.player.radius*2)
                self.player.horizontal_velocity = 0
                self.player.horizontal_acceleration = 0

            if requested_x >= self.player.radius*2:
                # ALLOW
                self.player.x = requested_x
            else:
                # collide with wall
                self.player.x = self.player.radius*2
                self.player.horizontal_velocity = 0
                self.player.horizontal_acceleration = 0

            if requested_y >= self.player.radius*2:
                # ALLOW
                self.player.y = requested_y
            else:
                # collide with wall
                self.player.y = self.player.radius*2
                self.player.vertical_velocity = 0
                self.player.vertical_acceleration = 0

            if requested_y <= self.height-(self.player.radius*2):
                # ALLOW
                self.player.y = requested_y
            else:
                # collide with wall
                self.player.y = self.height - (self.player.radius*2)
                self.player.vertical_velocity = 0
                self.player.vertical_acceleration = 0
            # math for reticle
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.tiltAngle = math.atan2(mouse_y - self.player.y, mouse_x - self.player.x)
            self.player.target_x = int(self.player.x + (self.player.radius * math.cos(self.tiltAngle)))
            self.player.target_y = int(self.player.y + (self.player.radius * math.sin(self.tiltAngle)))
            # Send Network Stuff
            # self.player2.x, self.player2.y = self.parse_data(self.send_data())
            if keys[pygame.K_q]:
                self.player.x,self.player.y = pygame.mouse.get_pos()
            self.send_data()
            server_players = self.receive_data()
            if server_players != False:
                if self.player.uid is None:
                    self.player.uid = self.net.uid
                    # print("my id is",self.player.uid)

            # I have other players
            #     print(server_players)
                for information in server_players:
                    # check to see if that player already exists
                    # if so update
                    # print("inf",str(information))
                    for player in self.players:
                        if information['uid'] != self.player.uid:
                            if not information['c']:
                                print("Trying to remove",player.uid)
                                if player in self.players:
                                    print("removed",player.uid)
                                    self.players.remove(player)
                                break
                            if information['uid'] == player.uid:

                                player.x = information['x']
                                player.y = information['y']
                                player.target_x = information['mx']
                                player.target_y = information['my']

                                break
                    else:
                        # if not add
                        if information['uid'] != self.player.uid:
                            p = Player(information['x'], information['y'])
                            p.uid = information['uid']
                            print("adding player from network",p.uid)
                            p.target_x = information['mx']
                            p.target_y = information['my']

                            self.players.append(p)
            # print(len(self.players))

            # Update Canvas2
            self.canvas.draw_background()

            # draw all the players
            for player in self.players:
                player.draw(self.canvas.get_canvas())
            # self.canvas.draw_status(self.player)
            self.canvas.update()
            clock.tick(60)
            self.player.can_accelerate = False
        pygame.quit()

    def send_data(self):
        print("Trying to send data")
        data_to_send = GameData(self.player).get_dictionary()
        self.net.send(data_to_send)

    def receive_data(self):
        return self.net.receive()

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))

        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y, color):
        pygame.font.init()

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(text, True, Utility.COLORS[color])
        textRect = text.get_rect()
        textRect.center = (x // 2, x // 2)
        self.screen.blit(text, textRect)

    def draw_status(self, player):
        pygame.font.init()

        font = pygame.font.Font('freesansbold.ttf', 32)

        text = "HV: {}".format(player.horizontal_velocity)
        text += "VV: {}".format(player.vertical_velocity)
        text += "HA: {}".format(player.horizontal_acceleration)
        text += "VA: {}".format(player.vertical_acceleration)
        text = font.render(text, True, Utility.COLORS['BLACK'])

        textRect = text.get_rect()
        textRect.center = (1000, 1000)
        self.screen.blit(text, textRect)

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(Utility.COLORS['WHITE'])


if __name__ == "__main__":
    g = Game(window[0], window[1])
    g.run()
