import pygame
from main import *
from vector import Vector

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 1 / t
WHITE  = (255, 255, 255)

ball1 = Ball(*("1", 100+100,200,500, 0, 0, m, Vector))
ball2 = Ball(*("2", 330,200,0,0, 0, m, Vector))
#ball3 = Ball(*(200,250,0,5,-5,0,0,0,0, m))

def draw_window():
    WIN.fill(WHITE)
    ball1.motion()
    ball2.motion()
    #ball3.motion()

    #pygame.draw.circle(WIN, (0,0,0), (ball1.x,ball1.y), r)
    #pygame.draw.circle(WIN, (0,0,0), (ball3.x,ball3.y), r)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

dem = input("Velocity: Vx, Vy, Spin: Wx, Wy, Wz ::")
ball1.v.x, ball1.v.y = int(dem.split(',')[0]), int(dem.split(',')[1])
ball1.wxy.x, ball1.wxy.y = int(dem.split(',')[2]), int(dem.split(',')[3])

if __name__ == "__main__":
    main()