import pygame
import numpy as np
from .utils import *

class Ball():
    def __init__(self, pos, display):
        self.pos = np.array([pos[0], pos[1]])
        self.current_speed = np.array([0, 0])
        self.display = display
        self.resistance = 0.01  #rolling resistance
        self.speed = 3          #'force' of the kick
        self.dir = 0
        self.sprite = pygame.image.load("./TeamViewer/assets/ball.png")

    def kick(self, dir):
        self.dir = dir
        self.current_speed[0] = self.speed * np.sin(deg2rad(dir))
        self.current_speed[1] = self.speed * np.cos(deg2rad(dir))

    def set_pos(self, pos_x, pos_y):
        self.pos = np.array([pos_x, pos_y])
        print("ball has set pos!")

    def bounce(self, normal):
        self.pos = self.pos - 2 * self.current_speed
        if np.abs(normal[0]) < np.abs(normal[1]):
            self.current_speed[1] = -self.current_speed[1]
        else:
            self.current_speed[0] = -self.current_speed[0]
        bounce_vec = normalize(self.current_speed)
        #self.debug_print(self.dir)
        self.dir = rad2deg(np.arctan2(bounce_vec[0], bounce_vec[1]))
        #self.debug_print(self.dir)

    def bump(self, dir):
        self.dir = dir
        self.current_speed[0] = 1.55 * np.sin(deg2rad(dir))
        self.current_speed[1] = 1.55 * np.cos(deg2rad(dir))
        self.pos = self.pos + 2 * self.current_speed

    def draw_helper_lines(self):
        pygame.draw.line(self.display, (102, 0, 102), (self.pos[0] + 20, self.pos[1]), (self.pos[0] - 20, self.pos[1]))
        pygame.draw.line(self.display, (102, 0, 102), (self.pos[0], self.pos[1] + 20), (self.pos[0], self.pos[1] - 20))

    def update(self):
        if not np.isclose(self.current_speed[0], 0, atol=0.001) or not np.isclose(self.current_speed[1], 0, atol=0.001):     
            self.current_speed[0] += self.resistance * np.sin(deg2rad(self.dir + 180))
            self.current_speed[1] += self.resistance * np.cos(deg2rad(self.dir + 180))
            self.pos = self.pos + self.current_speed
        else:
            self.current_speed = np.zeros(2)
        self.display.blit(self.sprite, (self.pos[0] - 8, self.pos[1] - 8))
        self.draw_helper_lines()

    def debug_print(self, out):
        print("Ball: {}".format(out))
