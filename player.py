from typing import Tuple
import pygame
import numpy as np
from utils import *

class Player():
    def __init__(self, pos, direction, speed, sprite, display):
        self.sprite = sprite
        self.speed = speed
        self.current_speed = np.zeros(2)
        self.dir = direction
        self.target = np.array([pos[0], pos[1]])
        self.position = np.array([pos[0], pos[1]])
        self.display = display
        self.fov = 90

    def set_speed(self, speed):
        self.speed = speed

    def get_position(self):
        return vec2tuple(self.position)

    def update(self):
        if np.isclose(self.target[0], self.position[0], atol= 0.5):
            self.go_to(vec2tuple(self.target))
        elif np.isclose(self.target[1], self.position[1], atol= 0.5):
            self.current_speed[0] = 0
            self.current_speed[1] = 0
        else:
            self.position = self.position + self.current_speed
        self.display.blit(pygame.transform.rotate(self.sprite, -self.dir), vec2tuple(self.position))

    def go_to(self, pos):
        width, height = self.display.get_size()
        if (pos[0] < 0 or pos[0] > width) or (pos[1] < 0 or pos[1] > height):
            print("posiiton is outside of map")
            return -1
        else:
            self.target[0] = pos[0]
            self.target[1] = pos[1]
            vec_dir = self.target - self.position
            vec_dir = vec_dir / np.linalg.norm(vec_dir)
            vec_zero = np.array([1, 0])
            self.dir = rad2deg(np.arccos(np.dot(vec_dir, vec_zero)))
            self.current_speed[0] = self.speed * np.cos(deg2rad(self.dir))
            self.current_speed[1] = self.speed * np.sin(deg2rad(self.dir))