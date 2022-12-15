import pygame
import numpy as np
from math import pi, sin, cos, tan, atan2, degrees as deg, floor, isclose
from vector import *

g = 9.81
m = .17
r = 10
t = 1 / 60
time = 0

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 1 / t
WHITE  = (255, 255, 255)

# Coeficients of Friction:
coRR = 0.01  # Rolling Resistance
coSF = 0.2  # Sliding Friction

redBall = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20, 20))


def hat(x):
    try:
        return x / abs(x)
    except:
        return 0


def friction(b):
    Ff = coSF * (b.m * g)  # Slipping
    if b.isRolling:  # Fully rolling
        Ff = coRR * (b.m * g)
    return Ff


def checkCollison(Ball):
    instances = Ball.instances
    for a in range(len(instances)):
        for b in range(len(instances) - 1, a, -1):
            ballA, ballB = instances[a], instances[b]
            dist = ((ballA.x - ballB.x) ** 2 + (ballA.y - ballB.y) ** 2) ** 0.5
            if dist <= 2 * r:
                BallCollision(ballA, ballB)
                print('True')


def BallCollision(b1, b2):
    dX = b2.x - b1.x
    dY = b2.y - b1.y

    angle = atan2(dY, dX)
    # Rotate it to where the collision line is parallel to the horizontal
    u1x = b1.v.x * cos(angle) + b1.v.y * sin(angle)
    u1y = b1.v.y * cos(angle) - b1.v.x * sin(angle)
    u2x = b2.v.x * cos(angle) + b2.v.y * sin(angle)
    u2y = b2.v.y * cos(angle) - b2.v.x * sin(angle)

    v1x = ((b1.m - b2.m) * u1x + 2 * b2.m * u2x) / (b1.m + b2.m)
    v1y = u1y

    v2x = ((b2.m - b1.m) * u2x + 2 * b1.m * u1x) / (b1.m + b2.m)
    v2y = u2y

    midpointX = (b1.x + b2.x) / 2
    midpointY = (b1.y + b2.y) / 2

    b1.x += (b1.x - midpointX) / 2
    b1.y += (b1.y - midpointY) / 2
    b2.x += (b2.x - midpointX) / 2
    b2.y += (b2.y - midpointY) / 2

    # Rotate back
    b1.v.x = v1x * cos(angle) - v1y * sin(angle)
    b1.v.y = v1y * cos(angle) + v1x * sin(angle)
    b2.v.x = v2x * cos(angle) - v2y * sin(angle)
    b2.v.y = v2y * cos(angle) + v2x * sin(angle)

    b1.isRolling, b2.isRolling = False, False


class Ball(pygame.sprite.Sprite):
    instances = []

    def __init__(self, ID, x, y, vx, vy, ax, ay, Vector):
        super(Ball, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        self.__class__.instances.append(self)
        self.ID = ID

        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.v = Vector(self.vx, self.vy)

        self.ax, self.ay = ax, ay

        self.wx, self.wy, self.wz = 0, 0, 0
        self.wxy = Vector(self.wx, self.wy)
        self.angU = angle_between(normalize(self.v), normalize(self.wxy))
        self.uO = (self.v + self.wxy)
        self.u = self.uO

        self.tau, self.alpha = 0, 0

        self.ux, self.uy = self.vx + r * self.wx, self.vy + r * self.wy

        self.uxO, self.uyO = self.vx + r * self.wx, self.vy + r * self.wy

        self.m = m
        self.I = 2 / 5 * m * r ** 2

        self.isRolling = False

    def rolling(self):
        #print(self.ux, self.uy)

        Fnet = -friction(self) * 1000
        a = atan2(self.v.y, self.v.x)

        Ax = Fnet * cos(a)
        Ay = Fnet * sin(a)

        self.v.x = self.v.x + Ax * t
        self.v.y = self.v.y + Ay * t

        self.x = self.x + self.v.x * t + 1 / 2 * Ax * (t ** 2)
        self.y = self.y + self.v.y * t + 1 / 2 * Ay * (t ** 2)

        self.wxy = Vector(1 / r * self.v.x, 1 / r * self.v.y)

        self.angU = atan2(self.uO.y, self.uO.x)

        self.tau = r * abs(Fnet)
        self.alpha = self.tau / self.I
        self.wz = self.wz - self.alpha * t  # r*np.hypot(self.vx, self.vy)

        if self.I / self.tau * self.wz < (np.hypot(self.vx, self.vy)) / (coSF * g):
            if t > self.I / self.tau * self.wz:
                self.wz = 0

        if self.ID == '1':
            pass

    def sliding(self):
        Fnet = friction(self) * 100
        a = atan2(self.vy, self.vx)

        Ax = -Fnet * cos(a)
        Ay = -Fnet * sin(a)


        self.u = self.uO - Vector(Fnet, Fnet)

        self.angU = atan2(self.v.y, self.v.x)

        self.v = self.v + normalize(self.u) * Vector(-Fnet * t, -Fnet * t)

        self.x = self.x + self.v.x * t + 1 / 2 * Ax * (t ** 2)
        self.y = self.y + self.v.y * t + 1 / 2 * Ay * (t ** 2)


        self.tau = r * abs(Fnet)
        self.alpha = self.tau / self.I

        self.wxy = self.wxy - normalize(self.wxy) * Vector((self.tau / self.I) * t, (self.tau / self.I) * t)

        if self.I / self.tau * self.wz < 2 / 7 * length(self.u):
            if t > self.I / self.tau * self.wz:
                self.wz = 0

    def motion(self):
        global time

        if length(self.wxy) * r <= length(self.v) or self.isRolling:
            self.rolling()
            self.isRolling = True

        else:
            self.sliding()

        checkCollison(self)
        WIN.blit(pygame.transform.scale(pygame.image.load(f"Assets/{self.ID}.png"), (20, 20)), (self.x - r, self.y - r))
        time += t
