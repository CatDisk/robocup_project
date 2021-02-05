from typing import Tuple
import pygame
import numpy as np
import utils

class Player():
    def __init__(self, pos, direction, sprite, display):
        self.sprite = sprite
        self.acc = 0
        self.speed = np.zeros(2)
        self.dir = direction
        self.position = np.array([pos[0], pos[1]])
        self.display = display
        self.fov = 90

    def set_speed(self, speed):
        self.speed[0] = speed * np.cos(utils.deg2rad(self.dir))
        self.speed[1] = speed * np.sin(utils.deg2rad(self.dir))

    def get_position(self):
        return self.position

    def update(self):
        self.position = self.position + self.speed

        self.display.blit(pygame.transform.rotate(self.sprite, -self.dir), utils.vec2tuple(self.position))
