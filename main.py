import pygame
import numpy as np
from math import sqrt, sin, cos, tan, degrees as deg

g = 9.81
m = .17
r = 10
timeInterval = 1/150

def rollingFriction(m , v):
    c = 0
    Fn = m*g
    v = np.abs(v)
    if v <= 0:
        rollingFriction = 0
    else:
        rollingFriction = c*Fn
    return 0

def getValue(value):
    absValue = np.abs(value)
    if value == 0:
        return 0

    if value / absValue == 1:
        return 1
    elif value / absValue == -1:
        return -1



def checkCollison(Ball):
    collided = []
    instances = Ball.instances
    for a in range(len(instances)):
        for b in range(len(instances) - 1, a, -1):
            ballA, ballB = instances[a], instances[b]
            dist = ((ballA.x - ballB.x)**2 + (ballA.y - ballB.y)**2 + (ballA.z - ballB.z)**2)**0.5
            if dist <= 2*r and dist != 0 and not(f"{a}{b}" in collided):
                collided.append(f"{a}{b}")
                BallCollision(ballA, ballB, m, m, (ballA.vx, ballA.vy), (ballB.vx, ballB.vy))




def BallCollision(b1, b2, m1, m2, u1, u2):
    u1x = u1[0] #INITIAL VELOCITY
    u1y = u1[1]

    u2x = u2[0]
    u2y = u2[1]

    v1x = ((m1 - m2) / (m1 + m2)) * u1x + ((2 * m2) / (m1 + m2)) * u2x #FINAL VELOCITY
    v1y = ((m1 - m2) / (m1 + m2)) * u1y + ((2 * m2) / (m1 + m2)) * u2y

    v2x = ((2 * m1) / (m1 + m2)) * u1x + ((m2 - m1) / (m1 + m2)) * u2x
    v2y = ((2 * m1) / (m1 + m2)) * u1y + ((m2 - m1) / (m1 + m2)) * u2y

    #b1.vx, b1.vy = 0, 50
    #b2.vx, b2.vy = 0, 0

    v1 = sqrt(v1x**2 + v1y**2)
    v2 = sqrt(v2x**2 + v2y**2)
    theta = deg(tan((b2.y-b1.y)/(b2.x-b1.x)))


    b1.vx, b1.vy = v1*sin(theta), v1*cos(theta)
    b2.vx, b2.vy = v2*sin(theta), v2*cos(theta)

    #return ((v1x, v1y),(v2x,v2y))

class Ball:
    instances = []
    def __init__(self, x, y, z, vx, vy, vz, ax, ay, az, m):
        self.__class__.instances.append(self)
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz
        self.ax, self.ay, self.az = ax, ay, az
        self.m = m

    def motion(self):
        data = []
        Ax = (getValue(self.vx) * rollingFriction(self.m, self.vx)) / self.m
        Ay = (getValue(self.vy) * rollingFriction(self.m, self.vy)) / self.m

        self.vx = self.vx + Ax * timeInterval
        self.vy = self.vy + Ay * timeInterval
        self.vz = self.vy #+ Az * timeInterval

        self.x = self.x + self.vx * timeInterval + 1 / 2 * (Ax) * (timeInterval ** 2)
        self.y = self.y + self.vy * timeInterval + 1 / 2 * (Ay) * (timeInterval ** 2)
        self.z = self.y + self.vy * timeInterval #+ 1 / 2 * (Ay) * (timeInterval ** 2)
        checkCollison(Ball)


        #data.append([x, y, Vx, Vy, Ax, Ay, t])

ball1 = Ball(*(100,100,0,0,100,0,0,0,0, m))
ball2 = Ball(*(100,300,0,0,-100,0,0,0,0, m))
ball3 = Ball(*(200,250,0,5,-5,0,0,0,0, m))

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
WHITE  = (255, 255, 255)


def draw_window():
    WIN.fill(WHITE)

    ball1.motion()
    ball2.motion()
    ball3.motion()

    pygame.draw.circle(WIN, (0,0,0), (ball1.x,ball1.y), r)
    pygame.draw.circle(WIN, (0,0,0), (ball2.x,ball2.y), r)
    pygame.draw.circle(WIN, (0,0,0), (ball3.x,ball3.y), r)

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        print(ball1.vx)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
