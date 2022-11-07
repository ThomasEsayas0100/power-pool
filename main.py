import pygame
import numpy as np
from math import pi, sin, cos, tan, atan2, degrees as deg

g = 9.81
m = .17
r = 10
timeInterval = 1/60

redBall = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20,20))

def mag(value):
    absValue = np.abs(value)
    return absValue/value

def friction(b):
    Ff = 0.01 * (b.m * g)
    if -b.w*r >= mag(b.vx**2 + b.vy**2): #If sliding
        Ff = 0.2 * (b.m * g)
        print(b, b.w)
    return Ff * 100


def checkCollison(Ball):
    global prior
    instances = Ball.instances
    for a in range(len(instances)):
        for b in range(len(instances) - 1, a, -1):
            ballA, ballB = instances[a], instances[b]
            dist = ((ballA.x - ballB.x)**2 + (ballA.y - ballB.y)**2)**0.5
            if dist <= 2*r:
                BallCollision(ballA, ballB, (ballA.vx, ballA.vy), (ballB.vx, ballB.vy))

def BallCollision(b1, b2, u1, u2):
    deltaX = b2.x - b1.x
    deltaY = b2.y - b1.y

    angle = atan2(deltaY, deltaX)
    print(sin(angle))
    # Rotate it to where the collision line is parallel to the horizontal
    u1x = b1.vx * cos(angle) + b1.vy * sin(angle)
    u1y = b1.vy * cos(angle) - b1.vx * sin(angle)
    u2x = b2.vx * cos(angle) + b2.vy * sin(angle)
    u2y = b2.vy * cos(angle) - b2.vx * sin(angle)

    v1x = ((b1.m-b2.m)*u1x+2*b2.m*u2x)/(b1.m+b2.m)
    v1y = u1y#((b1.m - b2.m) / (b1.m + b2.m)) * u1y + ((2 * b2.m) / (b1.m + b2.m)) * u2y

    v2x = ((b2.m-b1.m)*u2x+2*b1.m*u1x)/(b1.m+b2.m)
    v2y = u2y#((2 * b1.m) / (b1.m + b2.m)) * u1y + ((b2.m - b1.m) / (b1.m + b2.m)) * u2y

    midpointX = (b1.x + b2.x) / 2
    midpointY = (b1.y + b2.y) / 2

    b1.x += (b1.x - midpointX)/2
    b1.y += (b1.y - midpointY)/2
    b2.x += (b2.x - midpointX)/2
    b2.y += (b2.y - midpointY)/2

    #Rotate back
    b1.vx = v1x * cos(angle) - v1y * sin(angle)
    b1.vy = v1y * cos(angle) + v1x * sin(angle)
    b2.vx = v2x * cos(angle) - v2y * sin(angle)
    b2.vy = v2y * cos(angle) + v2x * sin(angle)

class Ball(pygame.sprite.Sprite):
    instances = []
    def __init__(self, x, y, vx, vy, ax, ay):
        super(Ball, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20,20))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        self.__class__.instances.append(self)
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.ax, self.ay = ax, ay
        self.w, self.tau = 0, 0
        self.m = m
        self.I = 2/5*(m)*(r)**2

    def motion(self):
        Fnet = friction(self)

        a = atan2(self.vy, self.vx)
        Ax = -Fnet * cos(a)
        Ay = -Fnet * sin(a)

        self.vx = self.vx + Ax * timeInterval
        self.vy = self.vy + Ay * timeInterval

        self.x = self.x + self.vx * timeInterval + 1 / 2 * (Ax) * (timeInterval ** 2)
        self.y = self.y + self.vy * timeInterval + 1 / 2 * (Ay) * (timeInterval ** 2)

        self.tau = r * mag(Fnet)
        self.w = self.w - (self.tau / self.I) * timeInterval

        checkCollison(self)


