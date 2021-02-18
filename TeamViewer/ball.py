import pygame
import numpy as np
from utils import *

class Ball():
    def __init__(self, pos, display):
        self.pos = np.array([pos[0], pos[1]])
        self.current_speed = np.array([0, 0])
        self.display = display
        self.resistance = 0.1
        self.speed = 2
        self.dir = 0
        self.sprite = pygame.image.load("./assets/ball.png")

    def kick(self, dir):
        self.dir = dir
        self.current_speed[0] = self.speed * np.sin(deg2rad(dir))
        self.current_speed[1] = self.speed * np.cos(deg2rad(dir))

    def update(self):
        if not np.allclose(self.speed, np.zeros(2), atol=0.5):     
            self.current_speed[0] -= self.resistance * np.sin(deg2rad(self.dir + 180))
            self.current_speed[1] -= self.resistance * np.cos(deg2rad(self.dir + 180))
        self.display.blit(self.sprite, vec2tuple(self.pos))
