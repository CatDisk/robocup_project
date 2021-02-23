import pygame
from pygame import display
from pygame.locals import *
import json
import threading
import numpy as np

from TeamViewer.utils import *
from TeamViewer.field import Field
from TeamViewer.player import Player
from TeamViewer.ball import Ball
from TeamViewer.message import Message
from game_controller import GameController

HEIGHT = 64 * 10 #has to be even number of tiles
WIDTH = 64 * 18
FPS = 60

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.FramePerSec = pygame.time.Clock()
        pygame.display.set_caption("2D Robocup")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player_speed = 1
        self.running = True
        self.players = []
        self.starting_pos = []
        self.field = Field(self.display)
        self.field.update()
        self.player_spites = {
            "red": pygame.image.load( "./TeamViewer/assets/player_red.png"),
            "blue": pygame.image.load("./TeamViewer/assets/player_blue.png"),
        }
        self.ball = Ball((WIDTH / 2, HEIGHT / 2), self.display)
        self.inbox = []

    def add_player(self,pos, dir, team = "red"):
        #player id corresponds to index in players list
        id = len(self.players)
        self.players.append(Player(id, pos, dir, self.player_speed, self.player_spites[team], self.display))
        self.starting_pos.append((np.array([pos[0], pos[1]]), dir))

    def reset_all(self):
        iter_starting_pos = iter(self.starting_pos)
        for player in self.players:
            player_pos = next(iter_starting_pos)
            np.copyto(player.position, player_pos[0])
            player.dir_body = player_pos[1]
            player.current_speed *= 0
        self.ball.pos = np.array([WIDTH / 2, HEIGHT / 2])
        self.ball.current_speed = np.array([0, 0])

    def check_collisions(self):
        pos_ball = self.ball.pos
        #player-player collisions
        for i in range(len(self.players)):
            pos1 = self.players[i].position
            for j in range(i+1, len(self.players)):
                pos2 = self.players[j].position
                dist = np.linalg.norm(pos1 - pos2)
                if dist < 45:
                    print("collision between {} and {} at  {}".format(i, j, pos1))
                    report1 = self.players[i].report_collision(pos2)
                    report2 = self.players[j].report_collision(pos1)

            #player-ball collisions
            dist = np.linalg.norm(pos1 - pos_ball)
            if dist < 30:
                less_speed = np.linalg.norm(self.players[i].current_speed) > np.linalg.norm(self.ball.current_speed)
                same_dir = np.isclose(self.players[i].dir_body, self.ball.dir, atol=45)
                no_ball_speed = np.allclose(self.ball.current_speed, np.zeros(2))
                if (less_speed and same_dir) or no_ball_speed:
                    self.ball.bump(self.players[i].dir_body)
                else:
                    normal = normalize(pos1 - pos_ball)
                    self.ball.bounce(normal)

        #ball-wall collision
        if self.ball.pos[0] < 10:
            self.ball.bounce(np.array([1, 0]))
        elif self.ball.pos[0] > WIDTH - 10:
            self.ball.bounce(np.array([-1, 0]))
        elif self.ball.pos[1] < 10:
            self.ball.bounce(np.array([0, 1]))
        elif self.ball.pos[1] > HEIGHT - 10:
            self.ball.bounce(np.array([0, -1]))

    def msg_handler(self, mode='in', body = None):
        if mode == 'in':
            while len(self.inbox) > 0:
                msg = self.inbox.pop()
                if msg.msg_type == "order":
                    payload = json.loads(msg.payload)
                    if payload["action"] == "move":
                        self.players[payload["target"]].go_to(payload["params"][0], payload["params"][1])
                    elif payload["action"] == "look":
                        self.players[payload["target"]].move_head(payload["params"][0])
                    elif payload["action"] == "kick":
                        if payload["target"] == "ball":
                            self.ball.kick(payload["params"][0])
                        else:
                            self.players[payload["target"]].kick(self.ball)
                    elif payload["action"] == "can see ball":
                        self.players[payload["target"]].can_see_ball(self.ball.pos)
                elif msg.msg_type == "quit":
                    self.running = False
                elif msg.msg_type == "reset":
                    self.reset_all()

    def start(self):
        pygame.display.flip()
        #main game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if controller != None:
                        controller.running = False
                        controller_thread.join()
                    self.running = False
            self.msg_handler()
            self.check_collisions()
            self.field.update()
            self.ball.update()
            for entity in self.players:
                entity.update()

            pygame.display.flip()
            self.FramePerSec.tick(FPS)

if __name__ == "__main__":
    game = Game()
    controller = GameController(game.inbox)
    game.add_player((WIDTH / 2 - 50, HEIGHT / 2), 90, "red")
    print((WIDTH / 2 + 50, HEIGHT / 2))
    game.add_player((100, 160), 180, "blue")
    controller_thread = threading.Thread(target = controller.run)
    controller_thread.start()
    game.start()