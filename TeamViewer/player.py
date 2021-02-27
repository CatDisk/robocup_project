import pygame
import numpy as np
from .utils import *
from .ball import Ball

class Player():
    def __init__(self, id, pos, direction, speed, team, sprite, display, ball, def_pos = (0,0), atk_pos = (0, 0)):
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
        self.defend_pos = def_pos
        self.attack_pos = atk_pos
        self.display = display
        self.fov = 56.3 #HFOV of the NAO robot Camera (67.4°DFOV)
        self.ball = ball
        self.team = team
        self.searching = False
        self.actions = self.build_action_dict()
        self.opponent_goal_threshold = self.calc_opponent_goal_threshold(team)
        self.opponent_goal = self.calc_opponent_goal_pos(team)
        self.current_goal = ""

    def build_action_dict(self):
        actions = {
            "TurnForOpponentGoal": lambda: self.turn_for_goal(),
            "TurnForBall": lambda: self.turn_for_ball(180),
            "Shoot": lambda: self.kick(),
            "Dribble": lambda: self.go_to((self.position[0] + 40 * np.sin(deg2rad(self.dir_body)),self.position[1] + 40 * np.cos(deg2rad(self.dir_body))), "forward"),
            "LookForBall": lambda: self.finish_current_goal(),
            "LookLeft": lambda: self.look_direction("left"),
            "LookFarLeft": lambda: self.look_direction("left"),
            "LookRight": lambda: self.look_direction("right"),
            "LookFarRight": lambda: self.look_direction("right"),
            "GoToBall": lambda: self.go_to(self.calc_near_ball_pos(), "forward"),
            "GoToAttackPosition": lambda: self.go_to(self.attack_pos, "forward"),
            "GoToDefendPosition": lambda: self.go_to(self.defend_pos, "back"),
            "Pass":1,
            "StayPut": lambda: True,
            "GoLeft": lambda: self.go_to((self.position[0] + 30 * np.sin(deg2rad(self.dir_body - 90)),self.position[0] + 30 * np.cos(deg2rad(self.dir_body - 90))), "left"),
            "GoRight": lambda: self.go_to((self.position[0] + 30 * np.sin(deg2rad(self.dir_body + 90)),self.position[0] + 30 * np.cos(deg2rad(self.dir_body + 90))), "right"),
        }
        return actions
    
    def draw_helper_lines(self):
        #fov
        end_pos_left = (self.position[0] + 500 * np.sin(deg2rad(self.dir_head + self.dir_body - self.fov/2)), self.position[1] + 500 * np.cos(deg2rad(self.dir_head + self.dir_body - self.fov/2)))
        end_pos_right = (self.position[0] + 500 * np.sin(deg2rad(self.dir_head + self.dir_body + self.fov/2)), self.position[1] + 500 * np.cos(deg2rad(self.dir_head + self.dir_body + self.fov/2)))
        pygame.draw.line(self.display, (255, 0, 0), vec2tuple(self.position), end_pos_left)
        pygame.draw.line(self.display, (0, 0, 255), vec2tuple(self.position), end_pos_right)

        #body dir
        end_pos = (self.position[0] + 100 * np.sin(deg2rad(self.dir_body)), self.position[1] + 100 * np.cos(deg2rad(self.dir_body)))
        pygame.draw.line(self.display, (192, 0, 135), vec2tuple(self.position), end_pos)

        #line to opponents goal
        pygame.draw.line(self.display, (102, 0, 102), vec2tuple(self.position), vec2tuple(self.opponent_goal))
        
    def set_speed(self, speed):
        self.speed = speed

    def turn_for_ball(self, amt):
        self.dir_head = 0
        self.current_head_speed = 0
        self.dir_body += amt
        self.can_see_ball()
        self.finish_current_goal()

    def turn_for_goal(self):
        vec_goal_ball = self.ball.pos - self.opponent_goal
        vec_goal_ball = normalize(vec_goal_ball)
        dir_goal_ball = np.arctan2(vec_goal_ball[0], vec_goal_ball[1])
        self.position[0] = self.ball.pos[0] + 30 * np.sin(dir_goal_ball)
        self.position[1] = self.ball.pos[1] + 30 * np.cos(dir_goal_ball)
        #self.dir_body = rad2deg(dir_goal_ball + np.pi)
        self.dir_body = deg2rad(np.arctan2(self.position[0] - self.ball.pos[0], self.position[1] - self.ball.pos[1])) + 180
        self.go_to((self.position[0] - 0.01,self.position[1]), "forward")
        

    def get_position(self):
        return vec2tuple(self.position)

    def calc_opponent_goal_threshold(self, team):
        threshold = -1
        offset_from_edge = int(self.display.get_width() * 1/5)
        if team == "red":
            threshold = self.display.get_width() - offset_from_edge
        else:
            threshold = offset_from_edge
        return threshold

    def calc_opponent_goal_pos(self, team):
        if team == "red":
            return np.array([self.display.get_width(), self.display.get_height()/2])
        else:
            return np.array([0, self.display.get_height()/2])


    def calc_near_ball_pos(self):
        near_pos = np.zeros(2)
        ball_dir = self.ball.pos - self.position
        ball_dir = normalize(ball_dir)
        angle_to_ball = np.arctan2(ball_dir[0], ball_dir[1])
        near_pos[0] = self.ball.pos[0] + 25 * np.sin(angle_to_ball + np.pi)
        near_pos[1] = self.ball.pos[1] + 25 * np.cos(angle_to_ball + np.pi)
        return near_pos

    def turn_for_opponent_goal(self):
        ball_dist = 25
        self.dir_body = rad2deg(np.arctan2(normalize(self.position - self.opponent_goal)))
        self.dir_head = 0
        self.ball.set_pos(self.position[0] + ball_dist * np.sin(deg2rad(self.dir_body)), self.position[1] + ball_dist * np.cos(deg2rad(self.dir_body)))
        self.ball.update()
        

    def finish_current_goal(self):
        out = "no report"
        dist = self.ball.pos - self.position
        angle = rad2deg(np.arctan2(dist[0], dist[1]))
        dist = np.linalg.norm(dist)
        if self.current_goal == "TurnForOpponentGoal":
            if (self.team == "red" and self.position[0] >= self.opponent_goal_threshold) or (self.team == "blue" and self.position[0] >= self.opponent_goal_threshold):
                dist = self.ball.pos - self.position
                angle = rad2deg(np.arctan2(dist[0], dist[1]))
                dist = np.linalg.norm(dist)
                if dist < 40:
                    out = "ready to shoot"
                elif dist >= 40:
                    out = "too far from ball"
            else:
                out = "facing opponents goal"
        elif self.current_goal == "Dribble":
            out = "done dribbling"
        elif self.current_goal == "Shoot":
            if not self.can_see_ball():
                out = "lost ball"
            elif dist > 40:
                out = "too far from ball"
        elif self.current_goal[:4] == "Look" and self.current_head_speed == 0:
            if self.can_see_ball():
                out = "found ball"
                self.move_head(0, False)
            else:
                out = "cant find ball"
        elif self.current_goal == "GoToBall":
            if not self.can_see_ball():
                out = "lost ball"
            elif dist < 40 and np.isclose(angle, self.dir_body, atol=30):
                out = "close to ball"
            else:
                self.go_to(self.calc_near_ball_pos(), "forward")
        elif self.current_goal == "TurnForBall":
            out = "done turning"

        return out

    def update(self):
        #update movement
        report = "no report"
        if np.isclose(self.target[0], self.position[0], atol= 0.5) and np.isclose(self.target[1], self.position[1], atol= 0.5):
            self.current_speed[0] = 0
            self.current_speed[1] = 0
            report = self.finish_current_goal()
        else:
            self.position = self.position + self.current_speed
        #update looking direction
        if not np.isclose(self.target_head_angle, self.dir_head, atol= 0.5):
            self.dir_head += self.current_head_speed
        else:
            self.current_head_speed = 0
        if self.searching and self.current_head_speed == 0:
            report = self.finish_current_goal()
        sprite_offset = np.array([16, 22.5])
        self.draw_helper_lines()
        #self.display.blit(pygame.transform.rotate(self.sprite, (self.dir_body - 90 + self.dir_head)), vec2tuple(self.position - sprite_offset))
        return report

    def move_head(self, target_dir, is_searching):
        self.searching = is_searching
        if target_dir > 119.5:
            self.debug_print("Angle too great!")
            target_dir = 119.5
        elif target_dir < -119.5:
            self.debug_print("Angle too small!")
            target_dir = -119.5
        self.target_head_angle = target_dir
        if self.target_head_angle < self.dir_head:
            self.current_head_speed = -self.head_yaw_speed
        elif self.target_head_angle > self.dir_head:
            self.current_head_speed = self.head_yaw_speed

    def can_see_ball(self):
        ball_dir = normalize(self.ball.pos - self.position)
        ball_dir = np.rad2deg(np.arctan2(ball_dir[0], ball_dir[1]))
        if np.isclose(ball_dir, (self.dir_body + self.dir_head), atol=self.fov):
            self.debug_print("can see the ball at {}".format(self.ball.pos))
            return True
        else:
            self.debug_print("can't see the ball")
            return False

    def look_direction(self, direction):
        factor = -1 if direction == "right" else 1
        starting_dir = self.dir_head
        if not np.isclose(factor * self.fov, self.dir_head):
            starting_dir = 0
        self.move_head(factor * self.fov + starting_dir, True)

    def kick(self):
        dist = self.ball.pos - self.position
        angle = rad2deg(np.arctan2(dist[0], dist[1]))
        dist = np.linalg.norm(dist)
        if dist < 40 and np.isclose(angle, self.dir_body, atol=30):
            self.ball.kick(self.dir_body)
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