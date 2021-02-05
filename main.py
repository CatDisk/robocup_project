import pygame
from pygame import display
from pygame.locals import *

from field import Field
from player import Player

pygame.init()

HEIGHT = 64 * 7
WIDTH = 64 * 12
FPS = 60

FramePerSec = pygame.time.Clock()

def main():
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Robocup")

    running = True

    #init Field
    field = Field(display)
    field.update()

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()