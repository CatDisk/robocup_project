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
    entities = []
    field = Field(display)
    field.update()
    for _ in range(1):
        entities.append(Player((200, 200), 0, 0.8, pygame.image.load("./assets/player_blue.png"), display))
    for elem in entities:
        elem.go_to((300, 300))

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        field.update()
        for entity in entities:
            entity.update()

        pygame.display.flip()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()