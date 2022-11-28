from pygame.locals import *
import pygame
import sys
import random

def main():
    gamescene = 0
    pygame.init()
    screen = pygame.display.set_mode((1060, 720))
    pygame.display.set_caption("Hit & Blow game")

    gamebutton = []
    gamebuttonrect = Rect(100, 100, 200, 50)
    gamebutton.append(pygame.image.load("tanuki.png"))
    gamebutton.append(pygame.image.load("tanuki_sleep.png"))
    gamebutton.append(pygame.image.load("tanuki_smile.png"))

    running = True

    while running:
        screen.fill((100, 100, 100))
        if gamescene == 0:
            screen.blit(gamebutton[0], gamebuttonrect)
        elif gamescene == 1:
            screen.blit(gamebutton[1], gamebuttonrect)
        elif gamescene ==2:
            screen.blit(gamebutton[2], gamebuttonrect)
        else:
            print("error")

        for event in pygame.event.get():
            if event.type == QUIT: 
                running = False
                pygame.quit() 
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if gamebuttonrect.collidepoint(event.pos):
                    if gamescene == 0:
                        gamescene = 1
                    elif gamescene == 1:
                        gamescene = 2
                    elif gamescene == 2:
                        gamescene = 0
                    else:
                        gamescene = -1

        pygame.display.update()


if __name__ == "__main__":
    main()