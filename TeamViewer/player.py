from typing import Tuple
import pygame
import numpy as np
from utils import *

class Player():
    def __init__(self, id, pos, direction, speed, sprite, display):
        self.id = id
        self.sprite = sprite
        self.speed = speed
        self.head_yaw_speed = 45 / 60
        self.current_speed = np.zeros(2)
        self.current_head_speed = 0
        self.target_head_angle = 0
        self.dir_body = direction
        self.dir_head = 0 #'head' position relative to self.dir
        self.target = np.array([pos[0], pos[1]])
        self.position = np.array([pos[0], pos[1]])
        self.display = display
        self.fov = 56.3 #HFOV of the NAO robot Camera (67.4°DFOV)

    def set_speed(self, speed):
        self.speed = speed

    def get_position(self):
        return vec2tuple(self.position)

    def update(self):
        #update movement
        if np.isclose(self.target[0], self.position[0], atol= 0.5) and np.isclose(self.target[1], self.position[1], atol= 0.5):
            self.current_speed[0] = 0
            self.current_speed[1] = 0
        else:
            self.position = self.position + self.current_speed
        #update looking direction
        if not np.isclose(self.target_head_angle, self.dir_head, atol= 0.5):
            self.dir_head += self.current_head_speed

        self.display.blit(pygame.transform.rotate(self.sprite, (self.dir_body - 90 + self.dir_head)), vec2tuple(self.position))

    def move_head(self, target_dir):
        if target_dir > 119.5:
            print("Angle too great!")
            target_dir = 119.5
        elif target_dir < -119.5:
            print("Angle too small!")
            target_dir = -119.5
        self.target_head_angle = target_dir
        if self.target_head_angle < self.dir_head:
            self.current_head_speed = -self.head_yaw_speed
        else:
            self.current_head_speed = self.head_yaw_speed

    
    def go_to(self, pos, dir):
        width, height = self.display.get_size()
        if (pos[0] < 0 or pos[0] > width) or (pos[1] < 0 or pos[1] > height):
            print('Posiiton is outside of map. Current map size is {} x {}'.format(width, height))
            return -1
        else:
            self.target[0] = pos[0]
            self.target[1] = pos[1]
            vec_dir = self.target - self.position
            vec_dir = normalize(vec_dir)
            self.dir_body = rad2deg(np.arctan2(vec_dir[0], vec_dir[1]))
            if dir == "forward":
                self.current_speed[0] = self.speed * np.sin(deg2rad(self.dir_body))
                self.current_speed[1] = self.speed * np.cos(deg2rad(self.dir_body))
            elif dir == "right":
                self.current_speed[0] = self.speed * np.sin(deg2rad(self.dir_body))
                self.current_speed[1] = self.speed * np.cos(deg2rad(self.dir_body))
                self.dir_body += -90
            elif dir == "left":
                self.current_speed[0] = self.speed * np.sin(deg2rad(self.dir_body))
                self.current_speed[1] = self.speed * np.cos(deg2rad(self.dir_body))
                self.dir_body += 90
            elif dir == "back":
                self.current_speed[0] = self.speed * np.sin(deg2rad(self.dir_body))
                self.current_speed[1] = self.speed * np.cos(deg2rad(self.dir_body))
                self.dir_body += 180
            else:
                print("\"{}\" is not a valid direction".format(dir))

    def print_display_size(self):
        print(self.display.get_size())