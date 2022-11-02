import pygame
import numpy as np
from math import pi, sin, cos, tan, atan, degrees as deg

g = 9.81
m = .17
r = 10
timeInterval = 1/60

redBall = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20,20))

def rollingFriction(m , v):
    c = 0
    Fn = m*g
    v = np.abs(v)
    if v <= 0:
        rollingFriction = 0
    else:
        rollingFriction = c*Fn
    return 0

def vector_angle(a, b):
    """
    Calculates the angle between two 2D vectors, A and B, in radians.
    """

    alpha_rad = np.arccos((a[0]*b[0] + a[1]*b[1])
                            /((a[0]**2 + a[1]**2)**0.5
                              * (b[0]**2 + b[1]**2)**0.5))
    return alpha_rad

def getValue(value):
    absValue = np.abs(value)
    if value == 0:
        return 0

    if value / absValue == 1:
        return 1
    elif value / absValue == -1:
        return -1


def checkCollison(Ball):
    global prior
    collided = []
    instances = Ball.instances



    for a in range(len(instances)):
        for b in range(len(instances) - 1, a, -1):
            ballA, ballB = instances[a], instances[b]
            dist = ((ballA.x - ballB.x)**2 + (ballA.y - ballB.y)**2 + (ballA.z - ballB.z)**2)**0.5
            if dist <= 2*r and not(f"{a}{b}" in collided) and dist != 0:
                balls = pygame.sprite.Group()
                balls.add(ballA)
                balls.add(ballB)
                if pygame.sprite.collide_rect(*balls):
                    collision = pygame.sprite.collide_circle(*balls)
                    if collision:
                        BallCollision(ballA, ballB, (ballA.vx, ballA.vy), (ballB.vx, ballB.vy))

                collided.append(f"{a}{b}")

def BallCollision(b1, b2, u1, u2):
    u1x = u1[0]  # INITIAL VELOCITY
    u1y = u1[1]

    u2x = u2[0]
    u2y = u2[1]

    deltaX = b2.x - b1.x
    deltaY = b2.y - b1.y

    if b1.x != b2.x:
        angle = atan(deltaY / deltaX)
    else:
        angle = 0

    # Rotate it to where the collision line is parallel to the horizontal
    u1x = b1.vx * cos(angle) + b1.vy * sin(angle)
    u1y = b1.vy * cos(angle) - b1.vx * sin(angle)
    u2x = b2.vx * cos(angle) + b2.vy * sin(angle)
    u2y = b2.vy * cos(angle) - b2.vx * sin(angle)

    v1x = ((b1.m - b2.m) / (b1.m + b2.m)) * u1x + ((2 * b2.m) / (b1.m + b2.m)) * u2x
    v1y = u1y#((b1.m - b2.m) / (b1.m + b2.m)) * u1y + ((2 * b2.m) / (b1.m + b2.m)) * u2y

    v2x = ((2 * b1.m) / (b1.m + b2.m)) * u1x + ((b2.m - b1.m) / (b1.m + b2.m)) * u2x
    v2y = u2y#((2 * b1.m) / (b1.m + b2.m)) * u1y + ((b2.m - b1.m) / (b1.m + b2.m)) * u2y

    midpointX = (b1.x + b2.x) / 2
    midpointY = (b1.y + b2.y) / 2

    b1.x += (b1.x - midpointX)/2
    b1.y += (b1.y - midpointY)/2
    b2.x += (b2.x - midpointX)/2
    b2.y += (b2.y - midpointY)/2
    x1, y1 = 0, 0
    x2, y2 = deltaX/2, deltaY/2
    overlap = 20 - ((deltaX)**2 + (deltaY)**2)**0.5
    #b1.x += overlap*cos(angle)


    #Rotate back
    v1x = v1x * cos(angle) - v1y * sin(angle)
    v1y = v1y * cos(angle) + v1x * sin(angle)
    v2x = v2x * cos(angle) - v2y * sin(angle)
    v2y = v2y * cos(angle) + v2x * sin(angle)

    b1.vx, b1.vy = v1x, v1y
    b2.vx, b2.vy = v2x, v2y
    print(b1.vx, b1.vy)



class Ball(pygame.sprite.Sprite):
    instances = []
    def __init__(self, x, y, z, vx, vy, vz, ax, ay, az, m):
        super(Ball, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets/1.png"), (20,20))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())

        self.__class__.instances.append(self)
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz
        self.ax, self.ay, self.az = ax, ay, az
        self.m = m

    def motion(self):
        Ax = 0 #(getValue(self.vx) * rollingFriction(self.m, self.vx)) / self.m
        Ay = 0 #(getValue(self.vy) * rollingFriction(self.m, self.vy)) / self.m

        self.vx = self.vx + Ax * timeInterval
        self.vy = self.vy + Ay * timeInterval
        self.vz = self.vy #+ Az * timeInterval
        self.x = self.x + self.vx * timeInterval + 1 / 2 * (Ax) * (timeInterval ** 2)
        self.y = self.y + self.vy * timeInterval + 1 / 2 * (Ay) * (timeInterval ** 2)
        self.z = self.y + self.vy * timeInterval #+ 1 / 2 * (Ay) * (timeInterval ** 2)

        checkCollison(Ball)


