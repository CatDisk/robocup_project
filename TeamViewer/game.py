import pygame
from pygame import display
from pygame.locals import *
import json
import threading
import numpy as np

from field import Field
from player import Player
from ball import Ball
from message import Message
from game_controller import GameController

HEIGHT = 64 * 10
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
        self.field = Field(self.display)
        self.field.update()
        self.player_spites = {
            "red": pygame.image.load("./assets/player_red.png"),
            "blue": pygame.image.load("./assets/player_blue.png"),
        }
        self.ball = Ball((WIDTH / 2, HEIGHT / 2), self.display)
        self.inbox = []

    def add_player(self,pos, dir, team = "red"):
        #player id corresponds to index in players list
        id = len(self.players)
        self.players.append(Player(id, pos, dir, self.player_speed, self.player_spites[team], self.display))

    def check_collisions(self):
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

        
        #TODO player-ball collisions

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
                        self.ball.kick(payload["params"][0])
                elif msg.msg_type == "quit":
                    self.running = False

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
    game.add_player((120, 100), 0)
    game.add_player((100, 300), 180, "blue")
    controller_thread = threading.Thread(target = controller.run)
    controller_thread.start()
    game.start()