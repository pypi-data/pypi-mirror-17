# raindrop by Duality

from Ledart.stripinfo import strip_width, strip_height
from Ledart.Tools.Graphics import Graphics, BLACK
import random


class RainDrop(object):
    def __init__(self, color=(100, 255, 100)):
        self.color = color
        self.y = 0
        self.x = random.randint(0, strip_width)
        self.pos = (self.x, self.y)
        self.height = self.y

    def getPos(self):
        return self.pos

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def incrementHeight(self):
        self.height += 1
        self.y = self.height
        self.pos = (self.x, self.y)


class RainPattern(Graphics):
    """
        rain pattern implementation by Duality
        will call 2.0 :D
    """
    def __init__(self, color=(80, 255, 100), chance=0.04):
        Graphics.__init__(self, width=strip_width, height=strip_height)
        self.color = color
        self.chance = chance
        # insert single drop for testing
        self.drops = [RainDrop(color)]

    def generate(self):
        self.fill(BLACK)
        # put drop in data and increment it's position
        for drop in self.drops:
            # calculate where to put it
            index = ((drop.y - 1) * strip_width + drop.x) - 1
            # put drop oN strip screen
            if index >= 0:
                self.draw_pixel(drop.x, drop.y - 1, drop.color)
            # increment it's height
            drop.incrementHeight()
            # if it falls of the screen remove it.
            if drop.getHeight() > strip_height:
                self.drops.remove(drop)
        # add a random chance for drops to appear.
        if(random.random() < self.chance):
            raindrop = RainDrop(self.color)
            self.drops.append(raindrop)


# class RainPattern_original:
#     # Falling drops, default color white/blue-ish
#     def __init__(self, color=(100, 255, 100), chance=0.04):
#         # Init empty data list
#         self.color = color
#         self.chance = chance
#         self.data = []
#         for i in xrange(strip_size):
#             self.data.insert(0, (0, 0, 0))  # black/off

#     def generate(self):
#         # Pop 7 times to move one line down
#         for i in xrange(strip_width):
#             self.data.pop()
#             if (random.random() < self.chance):  # random chance of raindrop
#                 self.data.insert(0, self.color)
#             else:
#                 self.data.insert(0, (0, 0, 0))  # black/off
#         return self.data
