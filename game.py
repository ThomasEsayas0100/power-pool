import pygame
from main import *

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
WHITE  = (255, 255, 255)

ball1 = Ball(*(100,100,0,100,0, m))
ball2 = Ball(*(115,200,0,-10,0, m))
#ball3 = Ball(*(200,250,0,5,-5,0,0,0,0, m))

def draw_window():
    WIN.fill(WHITE)

    ball1.motion()
    ball2.motion()
    #ball3.motion()

    pygame.draw.circle(WIN, (0,0,0), (ball1.x,ball1.y), r)
    WIN.blit(redBall, (ball1.x-r, ball1.y-r))
    pygame.draw.circle(WIN, (0,0,0), (ball2.x,ball2.y), r)
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

if __name__ == "__main__":
    main()