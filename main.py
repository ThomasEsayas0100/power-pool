import pygame
import numpy as np
from math import pi, sin, cos, tan, atan2, degrees as deg, floor

g = 9.81
m = .17
r = 10
t = 1 / 60

#Coeficients of Friction:
coRR = 0.01 #Rolling Resistance
coSF = 0.2 #Sliding Friction

redBall = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20,20))

def mag(value):
    absValue = np.abs(value)
    return absValue

def friction(b):
    Ff = coSF * (b.m * g) # Slipping
    if mag(b.wz*r) >= np.hypot(b.vx, b.vy): # Fully rolling
        Ff = coRR * (b.m * g)
    return Ff


def checkCollison(Ball):
    instances = Ball.instances
    for a in range(len(instances)):
        for b in range(len(instances) - 1, a, -1):
            ballA, ballB = instances[a], instances[b]
            dist = ((ballA.x - ballB.x)**2 + (ballA.y - ballB.y)**2)**0.5
            if dist <= 2*r:
                BallCollision(ballA, ballB)
                return True

def BallCollision(b1, b2):
    dX = b2.x - b1.x
    dY = b2.y - b1.y

    angle = atan2(dY, dX)
    # Rotate it to where the collision line is parallel to the horizontal
    u1x = b1.vx * cos(angle) + b1.vy * sin(angle)
    u1y = b1.vy * cos(angle) - b1.vx * sin(angle)
    u2x = b2.vx * cos(angle) + b2.vy * sin(angle)
    u2y = b2.vy * cos(angle) - b2.vx * sin(angle)

    v1x = ((b1.m-b2.m)*u1x+2*b2.m*u2x)/(b1.m+b2.m)
    v1y = u1y

    v2x = ((b2.m-b1.m)*u2x+2*b1.m*u1x)/(b1.m+b2.m)
    v2y = u2y

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
    def __init__(self, ID, x, y, vx, vy, ax, ay):
        super(Ball, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20,20))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        self.__class__.instances.append(self)
        self.ID = ID

        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.ax, self.ay = ax, ay

        self.u = 0
        self.wx, self.wy, self.wz = 0, 0, 0
        self.tau, self.alpha = 0, 0

        self.m = m
        self.I = 2/5*m*r**2

        self.isRolling = False

    def rolling(self):
        Fnet = friction(self) * 100
        a = atan2(self.vy, self.vx)

        Ax = -Fnet * cos(a)
        Ay = -Fnet * sin(a)

        self.vx = self.vx + Ax * t
        self.vy = self.vy + Ay * t

        self.x = self.x + self.vx * t + 1 / 2 * Ax * (t ** 2)
        self.y = self.y + self.vy * t + 1 / 2 * Ay * (t ** 2)

        self.wx = -1 / r * (abs(np.hypot(self.vx, self.vy))) * sin(a)
        self.wy = -1 / r * (abs(np.hypot(self.vx, self.vy))) * cos(a)

        if self.ID == '1':
            print(self.wx, self.wy, self.wz)

        self.tau = r * mag(Fnet)
        # Angular acceleration will be dependent on if the ball is sliding or rolling.
        self.alpha = -(mag(self.wz) / self.wz) * 15
        if -0.1 <= (np.hypot(self.vx, self.vy)) <= 0.1:
            self.alpha = 0

        self.wz = self.wz + self.alpha * t  # r*np.hypot(self.vx, self.vy)

    def sliding(self):
        Fnet = friction(self) * 100
        a = atan2(self.vy, self.vx)

        Ax = -Fnet * cos(a)
        Ay = -Fnet * sin(a)

        self.vx = self.vx + Ax * t
        self.vy = self.vy + Ay * t

        self.x = self.x + self.vx * t + 1 / 2 * Ax * (t ** 2)
        self.y = self.y + self.vy * t + 1 / 2 * Ay * (t ** 2)

        self.wx = self.wx - (self.tau / self.I)*t
        self.wy = self.wy - (self.tau / self.I)*t

        if self.ID == '1':
            print(self.wx, self.wy, self.wz)

        self.tau = r * mag(Fnet)
        # Angular acceleration will be dependent on if the ball is sliding or rolling.
        self.alpha = self.alpha = self.tau / self.I
        self.wz = self.wz + self.alpha * t  # r*np.hypot(self.vx, self.vy)

    def motion(self):
        if mag(self.wz * r) >= np.hypot(self.vx, self.vy) or self.isRolling:
            self.rolling()
            self.isRolling = True
        else:
            self.sliding()
        checkCollison(self)




