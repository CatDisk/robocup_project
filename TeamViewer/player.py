import pygame
import random
import numpy as np
from .utils import *
from .ball import Ball

class Player():
    def __init__(self, id, pos, direction, speed, team, sprite, display, ball, def_pos = None, atk_pos = None):
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
            "LookForBall": lambda: self.can_see_ball(),
            "LookLeft": lambda: self.look_direction("left"),
            "LookFarLeft": lambda: self.look_direction("left"),
            "LookRight": lambda: self.look_direction("right"),
            "LookFarRight": lambda: self.look_direction("right"),
            "GoToBall": lambda: self.go_to_ball(),
            "GoToAttackPosition": lambda: self.go_to(self.attack_pos, "forward"),
            "GoToDefendPosition": lambda: self.go_to(self.defend_pos, "back"),
            "Pass":lambda: self.kick(random.randint(-30, 30)),
            "StepBack": lambda: self.go_to((self.position[0] + 5 * np.sin(deg2rad(self.dir_body + 180)),self.position[1] + 5 * np.cos(deg2rad(self.dir_body + 180))), "back"),
            "StayPut": lambda: True,
            "GoRight": lambda: self.go_to((self.position[0] + 30 * np.sin(deg2rad(self.dir_body - 90)),self.position[1] + 30 * np.cos(deg2rad(self.dir_body - 90))), "left"),
            "GoLeft": lambda: self.go_to((self.position[0] + 30 * np.sin(deg2rad(self.dir_body + 90)),self.position[1] + 30 * np.cos(deg2rad(self.dir_body + 90))), "right"),
        }
        return actions
    
    def draw_helper_lines(self):
        #fov
        end_pos_left = (self.position[0] + 500 * np.sin(deg2rad(self.dir_head + self.dir_body - self.fov/2)), self.position[1] + 500 * np.cos(deg2rad(self.dir_head + self.dir_body - self.fov/2)))
        end_pos_right = (self.position[0] + 500 * np.sin(deg2rad(self.dir_head + self.dir_body + self.fov/2)), self.position[1] + 500 * np.cos(deg2rad(self.dir_head + self.dir_body + self.fov/2)))
        pygame.draw.line(self.display, (255, 0, 0), vec2tuple(self.position), end_pos_left)
        pygame.draw.line(self.display, (0, 0, 255), vec2tuple(self.position), end_pos_right)

        #line to opponents goal
        pygame.draw.line(self.display, (0, 255, 0), vec2tuple(self.position), vec2tuple(self.opponent_goal))
        
        #body dir
        end_pos = (self.position[0] + 50 * np.sin(deg2rad(self.dir_body)), self.position[1] + 50 * np.cos(deg2rad(self.dir_body)))
        pygame.draw.line(self.display, (192, 0, 135), vec2tuple(self.position), end_pos, 2)

    def set_speed(self, speed):
        self.speed = speed

    def turn_for_ball(self, amt):
        self.dir_head = 0
        self.current_head_speed = 0
        self.dir_body += amt
        self.can_see_ball()

    def go_to_ball(self):
        self.move_head(0,False)
        self.go_to(self.calc_near_ball_pos(), "forward")

    def turn_for_goal(self):
        self.opponent_goal = self.calc_opponent_goal_pos(self.team)
        vec_goal_ball = self.ball.pos - self.opponent_goal
        vec_goal_ball = normalize(vec_goal_ball)
        dir_goal_ball = np.arctan2(vec_goal_ball[0], vec_goal_ball[1])
        self.position[0] = self.ball.pos[0] + 30 * np.sin(dir_goal_ball)
        self.position[1] = self.ball.pos[1] + 30 * np.cos(dir_goal_ball)
        self.dir_body = rad2deg(dir_goal_ball + np.pi)
        #self.dir_body = deg2rad(np.arctan2(self.position[0] - self.ball.pos[0], self.position[1] - self.ball.pos[1]))
        #self.go_to((self.position[0] - 0.01,self.position[1]), "forward")
        

    def get_position(self):
        return vec2tuple(self.position)

    def calc_opponent_goal_threshold(self, team):
        threshold = -1
        offset_from_edge = int(self.display.get_width() * 1/4)
        if team == "red":
            threshold = self.display.get_width() - offset_from_edge
        else:
            threshold = offset_from_edge
        return threshold
    
    def calc_distance_to_goal(self):
        goal_pos: np.array
        if self.team == "blue":
            goal_pos =  np.array([self.display.get_width(), self.display.get_height()/2])
        else:
            goal_pos =  np.array([0, self.display.get_height()/2])

        dist = goal_pos - self.position
        dist = np.linalg.norm(dist)
        return dist

    def calc_opponent_goal_pos(self, team):
        random_offset = random.randint(-64 * 2, 64 * 2)
        if team == "red":
            return np.array([self.display.get_width(), self.display.get_height()/2 + random_offset])
        else:
            return np.array([0, self.display.get_height()/2 + random_offset])


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
        distance_to_ball = self.ball.pos - self.position
        angle_to_ball = rad2deg(np.arctan2(distance_to_ball[0], distance_to_ball[1]))
        distance_to_ball = np.linalg.norm(distance_to_ball)
        if self.current_goal == "TurnForOpponentGoal":
            if (self.team == "red" and self.position[0] >= self.opponent_goal_threshold) or (self.team == "blue" and self.position[0] <= self.opponent_goal_threshold):
                distance_to_ball = self.ball.pos - self.position
                angle_to_ball = rad2deg(np.arctan2(distance_to_ball[0], distance_to_ball[1]))
                distance_to_ball = np.linalg.norm(distance_to_ball)
                if distance_to_ball < 40:
                    out = "ready to shoot"
                elif distance_to_ball >= 40:
                    out = "too far from ball"
            else:
                out = "facing opponents goal"
        elif self.current_goal == "Dribble":
            out = "done dribbling"
        elif self.current_goal == "Shoot":
            out = "lost ball"
        elif self.current_goal == "LookForBall":
            if self.can_see_ball():
                out = "found ball"
            else:
                out = "cant find ball"
        elif self.current_goal[:4] == "Look" and self.current_head_speed == 0:
            if self.can_see_ball():
                out = "found ball"
            else:
                out = "cant find ball"
        elif self.current_goal == "GoToBall":
            ball_is_on_my_half = self.ball.pos[0] <= self.display.get_width()/2 if self.team == "red" else self.ball.pos[0] > self.display.get_width()/2
            if not self.can_see_ball():
                out = "lost ball"
            elif distance_to_ball < 40 and np.isclose(angle_to_ball, self.dir_body, atol=30):
                out = "close to ball"
            elif self.attack_pos != None and not ball_is_on_my_half:
                out = "Ball is on opponents half"
            else:
                self.go_to(self.calc_near_ball_pos(), "forward")
        elif self.current_goal == "TurnForBall":
            out = "done turning"
        elif self.current_goal == "StepBack":
            out = "done stepping back"
        elif self.current_goal == "StayPut":
            if self.attack_pos == None: #Keeper
                if distance_to_ball < 40:
                    out = "has ball"
                elif self.calc_distance_to_goal() < 30:
                    out = "far from goal" 
                elif distance_to_ball < 2 * (self.display.get_width() * 1/6):
                    if self.team == "blue":
                        if angle_to_ball < -90:
                            out = "Ball is approaching on the right side"
                        else:
                            out = "Ball is approaching on the left side"
                    else:
                        if angle_to_ball > 90:
                            out = "Ball is approaching on the left side"
                        else:
                            out = "Ball is approaching on the right side"
                else: 
                    out = "staying put"
            else: #Defender
                ball_is_on_my_half = self.ball.pos[0] <= self.display.get_width()/2 if self.team == "red" else self.ball.pos[0] > self.display.get_width()/2
                if not self.can_see_ball():
                    out = "lost ball"
                elif ball_is_on_my_half:
                    out = "Ball is on your half"
                else:
                    out = "Ball is on opponents half"
        elif self.current_goal == "GoRight" or self.current_goal == "GoLeft":
            out = "done stepping"
        elif self.current_goal == "Pass":
            out = "ball kicked away"
        elif self.current_goal == "GoToAttackPosition":
            ball_is_on_my_half = self.ball.pos[0] <= self.display.get_width()/2 if self.team == "red" else self.ball.pos[0] > self.display.get_width()/2
            if not self.can_see_ball():
                out = "lost ball"
            elif distance_to_ball < 40 and np.isclose(angle_to_ball, self.dir_body, atol=30):
                out = "has ball"
            elif ball_is_on_my_half:
                out = "Ball is on your half"
        elif self.current_goal == "GoToDefendPosition":
            ball_is_on_my_half = self.ball.pos[0] <= self.display.get_width()/2 if self.team == "red" else self.ball.pos[0] > self.display.get_width()/2
            approaching_goal = self.ball.pos[0] <= (self.display.get_width() * 1/5) if self.team == "red" else self.ball.pos[0] >= self.display.get_width() - (self.display.get_width() * 1/5)
            if not self.can_see_ball():
                out = "lost ball"
            elif distance_to_ball < 40 and np.isclose(angle_to_ball, self.dir_body, atol=30):
                out = "has ball"
            elif not ball_is_on_my_half:
                out = "Ball is on opponents half"
            elif approaching_goal:
                out = "Ball approaches goal"

        return out

    def update(self):
        #update movement
        report = "no report"
        if self.current_goal == "TurnForOpponentGoal" or self.current_goal == "LookForBall" or self.current_goal == "StayPut" or self.current_goal == "Pass" or self.current_goal == "Shoot" or self.current_goal == "TurnForBall":
            report = self.finish_current_goal()
        if np.isclose(self.target[0], self.position[0], atol= 0.5) and np.isclose(self.target[1], self.position[1], atol= 0.5):
            self.current_speed[0] = 0
            self.current_speed[1] = 0
            if report == "no report" :report = self.finish_current_goal()
        else:
            self.position = self.position + self.current_speed
        #update looking direction
        if not np.isclose(self.target_head_angle, self.dir_head, atol= 0.5):
            self.dir_head += self.current_head_speed
        else:
            self.current_head_speed = 0
        if self.searching:
            if self.current_head_speed == 0:
                report = self.finish_current_goal()
                
            elif self.can_see_ball():
                report = "found ball"
                self.searching = False
        sprite_offset = np.array([16, 22.5])
        self.draw_helper_lines()
        self.display.blit(pygame.transform.rotate(self.sprite, (self.dir_body - 90 + self.dir_head)), vec2tuple(self.position - sprite_offset))
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
        #self.debug_print(ball_dir, self.dir_head)
        if np.isclose(ball_dir, (self.dir_body + self.dir_head), atol=self.fov):
            #self.debug_print("can see the ball at {}".format(self.ball.pos))
            return True
        else:
            #self.debug_print("can't see the ball")
            return False

    def look_direction(self, direction):
        factor = -1 if direction == "right" else 1
        starting_dir = self.dir_head
        if not np.isclose(factor * self.fov, self.dir_head, atol = 10):
            starting_dir = 0
        self.move_head(factor * self.fov + starting_dir, True)

    def kick(self, dir = 0):
        dist = self.ball.pos - self.position
        dist = np.linalg.norm(dist)
        if dist < 40:
            self.debug_print("kick success")
            self.ball.kick(self.dir_body + dir)
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
            self.debug_print("bonk!")
            #'bounce' player out of colision retection range
            self.position -= 5 * self.current_speed
            return True
        else:
            return False
    
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

    def debug_print(self, *output):
        print("Player {}: {}".format(self.id, output))