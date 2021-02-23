import pygame
import numpy as np
from utils import *
from ball import Ball

class Player():
    def __init__(self, id, pos, direction, speed, sprite, display, def_pos = (0,0)):
        self.id = id
        self.sprite = sprite
        self.speed = speed
        self.head_yaw_speed = 45 / 60
        self.current_speed = np.zeros(2)
        self.current_head_speed = 0
        self.target_head_angle = 0
        self.dir_body = direction
        self.dir_head = 0 #'head' position relative to self.dir_body
        self.target = np.array([pos[0], pos[1]])
        self.position = np.array([pos[0], pos[1]])
        self.defend_pos = np.array([def_pos[0], def_pos[1]])
        self.display = display
        self.fov = 56.3 #HFOV of the NAO robot Camera (67.4°DFOV)
        self.ball_pos = None

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
        else:
            self.current_head_speed = 0
        sprite_offset = np.array([16, 22.5])
        self.display.blit(pygame.transform.rotate(self.sprite, (self.dir_body - 90 + self.dir_head)), vec2tuple(self.position - sprite_offset))

    def move_head(self, target_dir):
        if target_dir > 119.5:
            self.debug_print("Angle too great!")
            target_dir = 119.5
        elif target_dir < -119.5:
            self.debug_print("Angle too small!")
            target_dir = -119.5
        self.target_head_angle = target_dir
        if self.target_head_angle < self.dir_head:
            self.current_head_speed = -self.head_yaw_speed
        else:
            self.current_head_speed = self.head_yaw_speed

    def can_see_ball(self, ball_pos):
        ball_dir = normalize(ball_pos - self.position)
        ball_dir = np.rad2deg(np.arctan2(ball_dir[0], ball_dir[1]))
        if np.isclose(ball_dir, (self.dir_body + self.dir_head), atol=self.fov):
            self.ball_pos = ball_pos
            self.debug_print("can see the ball at {}".format(self.ball_pos))
            return True
        else:
            self.ball_pos = None
            self.debug_print("can't see the ball")
            return False

    def kick(self, ball: Ball):
        dist = ball.pos - self.position
        angle = rad2deg(np.arctan2(dist[0], dist[1]))
        dist = np.linalg.norm(dist)
        if dist < 40 and np.isclose(angle, self.dir_body, atol=30):
            ball.kick(self.dir_body)
            self.debug_print("kick success")
            return True
        else:
            self.debug_print("kick failure")
            return False


    def report_collision(self, pos) -> str:
        #check if responsible
        #TODO fix collsions when walking direction != body direction
        impact_dir = normalize(pos - self.position)
        impact_dir = rad2deg(np.arctan2(impact_dir[0], impact_dir[1]))
        if np.isclose(impact_dir, rad2deg(np.arctan2(self.current_speed[0], self.current_speed[1])), atol = 30):
            if not np.allclose(self.current_speed, np.zeros(2), atol= 0.001):
                self.debug_print("Responsible for collision")
                #'bounce' player out of colision retection range
                self.position -= 2 * self.current_speed
            if impact_dir < rad2deg(np.arctan2(self.current_speed[0], self.current_speed[1])):
                self.debug_print("Impact on the right")
                self.current_speed = self.current_speed * 0
                return "right"
            else:
                self.debug_print("Impact on the left")
                self.current_speed = self.current_speed * 0
                return "left"
        else:
            return "none"
    
    def go_to(self, pos, dir):
        width, height = self.display.get_size()
        if (pos[0] < 0 or pos[0] > width) or (pos[1] < 0 or pos[1] > height):
            self.debug_print('Posiiton is outside of map. Current map size is {} x {}'.format(width, height))
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
                self.debug_print("\"{}\" is not a valid direction".format(dir))

    def debug_print(self, output):
        print("Player {}: {}".format(self.id, output))