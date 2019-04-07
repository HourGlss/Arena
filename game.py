import pygame
from networkTCP import Network
from Player import Player
import time
import math
window = (1920,1080)
# https://www.rapidtables.com/web/color/RGB_Color.html
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'BLUE': (0, 0, 255),
    'GREEN': (100, 200, 62),
    'RED': (205, 30, 16),
    'PURPLE': (76, 14, 119),
    'YELLOW': (255, 255, 0),
    'ORANGE': (241, 171, 0),
    'BROWN': (118, 57, 49)
}
available_colors = list(COLORS.keys())

class Game:

    tiltAngle = 0
    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(100, 100)
        self.canvas = Canvas(self.width, self.height, "Testing...")
        # pygame.mouse.set_visible(False)

    def run(self):
        clock = pygame.time.Clock()
        run = True

        player_can_accelerate = False
        while run:
            clock.tick(60)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False


            keys = pygame.key.get_pressed()



            #fucking accel
            if self.player.ticks_until_acceleration >0:
                self.player.ticks_until_acceleration -=1
            elif self.player.ticks_until_acceleration == 0:
                player_can_accelerate = True
                self.player.ticks_until_acceleration = self.player.ticks_until_acceleration_default


            #this keeps you on screen

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity_east:
                    if player_can_accelerate:
                        self.player.accelerate_east += 1
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity_west:
                    if player_can_accelerate:
                        self.player.accelerate_west += 1
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity_north:
                    if player_can_accelerate:
                        self.player.accelerate_north += 1
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity_south:
                    if player_can_accelerate:
                        self.player.accelerate_south += 1
                    self.player.move(3)

            if self.player.accelerate_east > 0:
                self.player.accelerate_east -= 1
            if self.player.accelerate_east < 0:
                self.player.accelerate_east == 0
            if self.player.accelerate_west > 0:
                self.player.accelerate_west -= 1
            if self.player.accelerate_west < 0:
                self.player.accelerate_west == 0
            if self.player.accelerate_south > 0:
                self.player.accelerate_south -= 1
            if self.player.accelerate_south < 0:
                self.player.accelerate_south == 0
            if self.player.accelerate_north > 0:
                self.player.accelerate_north -= 1
            if self.player.accelerate_north < 0:
                self.player.accelerate_north == 0




            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())

            #point cursor towards mouse
            mouse_x,mouse_y= pygame.mouse.get_pos()
            self.tiltAngle  = math.atan2(mouse_y - self.player.y, mouse_x - self.player.x)
            target_x = self.player.x + (self.player.radius * math.cos(self.tiltAngle))
            target_y = self.player.y + (self.player.radius * math.sin(self.tiltAngle))
            pygame.draw.circle(self.canvas.get_canvas(), COLORS['BLACK'], [int(target_x), int(target_y)], 5)

            self.player2.draw(self.canvas.get_canvas())
            player_can_accelerate = False
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0


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
        text = font.render(text, True, COLORS[color])
        textRect = text.get_rect()
        textRect.center = (x // 2, x // 2)
        self.screen.blit(text, textRect)

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(COLORS['WHITE'])


if __name__ == "__main__":
    g = Game(window[0],window[1])
    g.run()
