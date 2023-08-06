from Ledart.Tools.Graphics import Graphics, BLACK, GREEN, RED, CYAN, YELLOW, WHITE
from Ledart.stripinfo import strip_width, strip_height
import random


class GraphicsPixelTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, strip_width, strip_height)
        self.color = GREEN
        self.pos = (random.randint(1, strip_width - 1),
                    random.randint(1, strip_height - 1))
        self.speed = 1
        self.deltax, self.deltay = self.speed, self.speed

    def generate(self):
        self.fill(BLACK)
        x, y = self.pos
        self.draw_pixel(x, y, self.color)
        if x >= strip_width - 1 or x <= 0:
            self.deltax *= -1
        if y >= strip_height - 1 or y <= 0:
            self.deltay *= -1
        self.pos = x + self.deltax, y + self.deltay


class GraphicsLineScroll(Graphics):
    def __init__(self):
        Graphics.__init__(self, strip_width, strip_height)
        self.color = RED
        self.pos = 0,0
        self.vertical = True
        self.horizontal = False

    def generate(self):
        self.fill(BLACK)
        if(self.vertical):
            x, y = self.pos
            # self.draw_pixel(x, y, self.color)
            self.draw_line(x, y, x, strip_height, self.color)
            x += 1
            if(x == strip_width):
                x = 0
                self.horizontal = True
                self.vertical = False
            self.pos = x, y
        if(self.horizontal):
            x, y = self.pos
            # self.draw_pixel(x, y, self.color)
            self.draw_line(x, y, strip_width, y, self.color)
            y += 1
            if(y == strip_height):
                y = 0
                self.horizontal = False
                self.vertical = True
            self.pos = x, y

class GraphicsLineTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, strip_width, strip_height)
        self.color = YELLOW
        self.pos = 0, 0

    def generate(self):
        self.fill(BLACK)
        x, y = self.pos
        self.draw_line(strip_width - x, strip_height - y,
                                x, y, self.color)
        if x >= strip_height:
            x = 0
            y = 0
        self.pos = x + 1, y


class GraphicsRectTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, strip_width, strip_height)
        self.color = CYAN
        self.rect_size = strip_width
        self.pos = 0, 0

    def generate(self):
        # self.fill(BLACK)
        self.draw_rect(0, 0, strip_width, strip_height, self.color)
        # clear the drawing surface
        # self.fill(BLACK)
        # put a rectangle on the surface
        # x, y = self.pos
        # if x >= strip_width:
        #     x = 0
        # if y >= strip_height:
        #     y = 0
        # self.draw_rect(x, y, strip_width - x,
        #                         strip_height - y, self.color)
        # self.pos = x + 1, y + 1


class GraphicsCircleTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, strip_width, strip_height)
        self.radius = 0
        self.direction = 1
        self.color = RED

    def generate(self):
        # clear the drawing surface
        self.fill(BLACK)
        # put a circle on our surface
        self.draw_circle(strip_width / 2, strip_height / 2,
                                  self.radius, self.color)

        # circle grows and shrinks based on direction.
        if self.direction:
            self.radius += 1
        else:
            self.radius -= 1

        # if the circle is to big or to small inverse growth direction.
        if self.radius >= (strip_height / 2) or self.radius <= 0:
            self.direction = not self.direction


class GraphicsDotTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, strip_width, strip_height)
        self.color = (123, 111, 222)

    def generate(self):
        self.fill(BLACK)
        for i in range(0, 5):
            self.draw_pixel(i, i, self.color)
