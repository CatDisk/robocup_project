from typing import Tuple
import pygame

class Player():
    def __init__(self, position: Tuple, direction, sprite, display):
        self.sprite = sprite
        self.acc = 0
        self.speed = 0
        self.dir = direction
        self.position = position
        self.display = display

    def set_speed(self, speed):
        self.speed = speed

    def update(self):
        self.display.blit(pygame.transform.rotate(self.sprite, self.dir), self.position)
