import math
import sys
import pygame
from itertools import chain

pygame.init()
screen = pygame.display.set_mode((800, 800))

walls = [
    pygame.Rect((0, 0), (10, 800)), # left
    pygame.Rect((0, 0), (800, 10)), # top
    pygame.Rect((790, 0), (10, 800)), # right
    pygame.Rect((0, 790), (800, 10)), # bottom
    pygame.Rect((100, 100), (100, 100)), # block
]


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class Ray:
    def __init__(self, angle, colour):
        self.speed = 2
        self.angle = angle
        self.colour = colour
        self.vector = pygame.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))) * self.speed

        self.point = pygame.Vector2(400, 400)
        self.old_point = self.point.copy()

    def update(self):
        self.old_point = self.point.copy()

        # Update vector movement
        self.vector = pygame.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))) * self.speed

        # move ray forward
        self.point += self.vector

        for rect in walls:
            if rect.collidepoint(self.point):
                sides = {
                    "left": (self.point[0] - rect.left),
                    "right": (self.point[0] - rect.right),
                    "bottom": (self.point[1] - rect.bottom),
                    "top": (self.point[1] - rect.top)
                }
                sides = sorted(sides.items(), key=lambda y: abs(y[1]), reverse=False)

                if sides[0][0] == 'bottom' or sides[0][0] == 'top':
                    self.angle = 360 - self.angle
                else:
                    self.angle = 180 - self.angle

    def draw(self):
        pygame.draw.lines(screen, self.colour, False, [self.point, self.old_point])


rays = []
colours = []
for r, g, b in zip(
    chain(reversed(range(256)), [0] * 256),
    chain(range(256), reversed(range(256))),
    chain([0] * 256, range(256))):
    colours.append((r, g, b))

for i, colour in enumerate(colours):
    angle = translate(i, 0, 512, 0, 360)
    rays.append(Ray(angle=angle, colour=colour))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for ray in rays:
        ray.update()
        ray.draw()

    pygame.display.update()
    # screen.fill("black")
pygame.quit()
sys.exit()