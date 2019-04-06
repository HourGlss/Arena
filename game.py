import pygame
from networkTCP import Network
import time
import math

# GITKRACKEN
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


class Player():
    radius = 25
    uid = None
    def __init__(self,startx, starty, color=(255, 0, 0)):
        self.x = startx
        self.y = starty
        self.velocity = 7
        self.color = color

    def draw(self, g):
       self.draw_regular_polygon(g, self.color, 5, math.pi / 5, self.x, self.y, self.radius)

    def draw_regular_polygon(self, surface, color, numSides, tiltAngle, x, y, radius):
        pts = []
        for i in range(numSides):
            x = x + radius * math.cos(tiltAngle + math.pi * 2 * i / numSides)
            y = y + radius * math.sin(tiltAngle + math.pi * 2 * i / numSides)
            pts.append([int(x), int(y)])
        pygame.draw.polygon(surface, color, pts)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def rotate(self, angle):
        thingtorotate = pygame.transform.rotozoom(self.surface, angle, 1)


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(100, 100)
        self.canvas = Canvas(self.width, self.height, "Testing...")

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
                elif event.type == pygame.MOUSEMOTION:
                    mouse_x = pygame.mouse.get_pos()[0]
                    mouse_y = pygame.mouse.get_pos()[1]
                    angle = math.atan2(mouse_y - self.player.y, mouse_x - self.player.x)
                    angle = angle * (180 / math.pi)
                    self.player.rotate(angle)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)
            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
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
    g = Game(500, 500)
    g.run()
