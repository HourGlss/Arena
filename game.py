import pygame
from networkUDP import Network
from Player import Player
import Utility
import time
import math

window = (1920 , 1080)


class Game:
    tiltAngle = 0
    players = []
    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(int(self.width/2),int(self.height/2))
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.players.append(self.player)
        # pygame.mouse.set_visible(False)

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
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
                self.player.horizontal_velocity = self.player.horizontal_velocity - self.player.horizontal_velocity / 3
            elif self.player.horizontal_velocity < 0:
                self.player.horizontal_velocity = self.player.horizontal_velocity + abs(self.player.horizontal_velocity )/ 3

            if self.player.vertical_velocity > 0:
                self.player.vertical_velocity = self.player.vertical_velocity - self.player.vertical_velocity / 3
            elif self.player.vertical_velocity < 0:
                self.player.vertical_velocity = self.player.vertical_velocity + abs(self.player.vertical_velocity) / 3

            #Friction for acceleration
            # if self.player.horizontal_acceleration > 0:
            #     self.player.horizontal_acceleration = self.player.horizontal_acceleration - 1
            # elif self.player.horizontal_acceleration < 0:
            #     self.player.horizontal_acceleration = self.player.horizontal_acceleration + 1
            #
            # if self.player.vertical_acceleration > 0:
            #     self.player.vertical_acceleration = self.player.vertical_acceleration - 1
            # elif self.player.vertical_acceleration < 0:
            #     self.player.vertical_acceleration = self.player.vertical_acceleration + 1


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
            if requested_x <= self.width - self.player.radius:
                # ALLOW
                self.player.x = requested_x
            else:
                self.player.x = self.width - self.player.radius
                self.player.horizontal_velocity = 0
                self.player.horizontal_acceleration = 0

            if requested_x >= self.player.radius:
                # ALLOW
                self.player.x = requested_x
            else:
                # collide with wall
                self.player.x = self.player.radius
                self.player.horizontal_velocity = 0
                self.player.horizontal_acceleration = 0

            if requested_y >= self.player.radius:
                # ALLOW
                self.player.y = requested_y
            else:
                # collide with wall
                self.player.y = self.player.radius
                self.player.vertical_velocity = 0
                self.player.vertical_acceleration = 0

            if requested_y <= self.height:
                # ALLOW
                self.player.y = requested_y
            else:
                # collide with wall
                self.player.y = self.height - self.player.radius
                self.player.vertical_velocity = 0
                self.player.vertical_acceleration = 0

            # math for reticle
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.tiltAngle = math.atan2(mouse_y - self.player.y, mouse_x - self.player.x)
            self.player.target_x = int(self.player.x + (self.player.radius * math.cos(self.tiltAngle)))
            self.player.target_y = int(self.player.y + (self.player.radius * math.sin(self.tiltAngle)))




            # Send Network Stuff
            # self.player2.x, self.player2.y = self.parse_data(self.send_data())
            server_players = self.send_data()
            if len(server_players) > 1:
                #I have other players
                for information in server_players:
                #check to see if that player already exists
                # if so update
                    for player in self.players:
                        if information['uid'] == player.uid:
                            player.x = information['x']
                            player.y = information['y']
                            player.target_x = information['x']
                            player.target_y = information['y']
                            break
                else:
                    # if not add
                    p = Player(information['x'],information['y'])
                    p.target_x = information['mouse_x']
                    p.target_x = information['mouse_y']
                    p.uid = information['uid']
                    self.players.append(p)




            # Update Canvas
            self.canvas.draw_background()

            #draw all the players
            for player in self.players:
                player.draw(self.canvas.get_canvas())


            self.canvas.draw_status(self.player)
            self.player.can_accelerate = False
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        data_to_send = {"x":self.player.x, 'y': self.player.y, 'mouse_x': self.player.target_x,
                        'mouse_y': self.player.target_y}
        # data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data_to_send)
        if self.player.uid is None:
            self.player.uid = self.net.uid
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


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

    def draw_status(self,player):
        pygame.font.init()

        font = pygame.font.Font('freesansbold.ttf', 32)

        text = "HV: {}".format(player.horizontal_velocity)
        text += "VV: {}".format(player.vertical_velocity)
        text += "HA: {}".format(player.horizontal_acceleration)
        text += "VA: {}".format(player.vertical_acceleration)
        text = font.render(text, True, Utility.COLORS['BLACK'])

        textRect = text.get_rect()
        textRect.center = (1000,1000)
        self.screen.blit(text, textRect)

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(Utility.COLORS['WHITE'])


if __name__ == "__main__":
    g = Game(window[0], window[1])
    g.run()
