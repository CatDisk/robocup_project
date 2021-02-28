import pygame
from pygame import display
from pygame.locals import *
import json
import threading
import queue
import numpy as np
import sys

from TeamViewer.utils import *
from TeamViewer.field import Field
from TeamViewer.player import Player
from TeamViewer.ball import Ball
from TeamViewer.message import Message
from TeamViewer.clock import Clock
from game_controller import GameController

HEIGHT = 64 * 10 #has to be even number of tiles
WIDTH = 64 * 18
FPS = 60

class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', 23)
        self.FramePerSec = pygame.time.Clock()
        self.game_speed = 1
        pygame.display.set_caption("2D Robocup")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player_speed = 1
        self.running = True
        self.players = []
        self.player_metadata = []
        self.score = np.array([0, 0])
        self.field = Field(self.display)
        self.field.update()
        self.player_spites = {
            "red": pygame.image.load( "./TeamViewer/assets/player_red.png"),
            "blue": pygame.image.load("./TeamViewer/assets/player_blue.png"),
        }
        self.key_map = {
            49: 1,
            50: 2,
            51: 3,
            52: 10,
            114: 'r',
        }
        #self.ball = Ball((WIDTH / 2, HEIGHT / 2), self.display)
        self.ball = Ball((WIDTH/2, HEIGHT/2 - 50), self.display)
        self.clock = Clock(FPS)
        self.inbox = queue.Queue()
        self.controller_inbox = queue.Queue()
        self.message_event = threading.Event()

    def set_controller_inbox(self, inbox: queue.Queue):
        self.controller_inbox = inbox
        print("set controller inbox at {}".format(self.controller_inbox))

    def add_player(self,pos, dir, team, role, def_pos = None, atk_pos = None):
        #player id corresponds to index in players list
        id = len(self.players)
        if role == "defender":
            self.players.append(Player(id, pos, dir, self.player_speed, team, self.player_spites[team], self.display, self.ball, def_pos=def_pos, atk_pos=atk_pos))
        else:
            self.players.append(Player(id, pos, dir, self.player_speed, team, self.player_spites[team], self.display, self.ball))
        self.player_metadata.append({
            "reset position": (np.array([pos[0], pos[1]]), dir),
            "role": role,
            "team": team
        })


    def reset_all(self):
        iter_starting_pos = iter(self.player_metadata)
        for player in self.players:
            player_pos = next(iter_starting_pos)["reset position"]
            np.copyto(player.position, player_pos[0])
            player.dir_body = player_pos[1]
            player.current_speed *= 0
        self.ball.pos = np.array([WIDTH / 2, HEIGHT / 2])
        self.ball.current_speed = np.array([0, 0])

    def check_goal(self):
        from_sides, from_center = self.field.goals_pos()
        if self.ball.pos[0] < from_sides and np.isclose(self.ball.pos[1], HEIGHT/2, atol = from_center):
            #goal for blue
            self.score[1] += 1
            return True
        elif self.ball.pos[0] > WIDTH - from_sides and np.isclose(self.ball.pos[1], HEIGHT/2, atol = from_center):
            #goal for red
            self.score[0] += 1
            return True
        else:
            return False

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
                    if self.players[i].report_collision(pos2):
                        self.send_data(i, "collision")
                        self.message_event.set()

            #player-ball collisions
            dist = np.linalg.norm(pos1 - pos_ball)
            if dist < 20:
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
    
    def game_speed_text(self):
        out = "{}x ".format(self.game_speed)
        for _ in range(self.game_speed):
            out = out + ">"
        return out

    def display_game_info(self):
        texts = []
        texts.append(" Time: {}".format(self.clock.time))
        texts.append("Speed: {}".format(self.game_speed_text()))
        texts.append("Score: {}-{}".format(self.score[0], self.score[1]))
        for index, text in enumerate(texts):
            surf = self.font.render(text, False, (255, 255, 255))
            self.display.blit(surf, (40, 40 + int(surf.get_height()) * index))

    def draw_helper_lines(self):
        factor = 1/4
        offset_from_edge = int(WIDTH * factor)
        #red goal area
        pygame.draw.line(self.display, (255, 0, 0), (offset_from_edge,0), (offset_from_edge,HEIGHT), 2)
        #blue goal area
        pygame.draw.line(self.display, (0, 0, 255), (WIDTH - offset_from_edge,0), (WIDTH - offset_from_edge,HEIGHT), 2)

    def msg_handler(self, mode='in', body = None):
        if mode == 'in':
            while not self.inbox.empty():
                msg = self.inbox.get()
                if msg.msg_type == "order":
                    payload = json.loads(msg.payload)
                    self.players[payload["target"]].current_goal = payload["action"]
                    print("Player {} current goal: {}".format(payload["target"], payload["action"]))
                    self.players[payload["target"]].actions[payload["action"]]()
                elif msg.msg_type == "quit":
                    self.running = False
                elif msg.msg_type == "reset":
                    self.reset_all()
        elif mode == "out":
            message = Message("data", body) 
            self.controller_inbox.put(message)
            self.message_event.set()

    def send_data(self, player_id, report):
        data = {
            "target": player_id,
            "report": report,
        }
        self.msg_handler("out", json.dumps(data))

    def start(self):
        pygame.display.flip()
        #main game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.message_event.set()
                    if controller != None:
                        controller.inbox.put(Message("quit", None))
                        controller_thread.join()
                    self.running = False
                elif event.type == pygame.KEYUP:
                    try:
                        if event.key != 114:
                            self.game_speed = self.key_map[event.key]
                        elif event.key == 114:
                            self.reset_all()
                            controller.inbox.put(Message("reset", None))
                            self.message_event.set()
                        else:
                            raise NotImplementedError
                    except:
                        print("unmapped key: {}".format(event.key))
            self.msg_handler()
            self.check_collisions()
            self.field.update()
            self.ball.update()
            self.draw_helper_lines()
            self.display_game_info()
            for index, entity in enumerate(self.players):
                msg = entity.update()
                if msg != "no report":
                    print("Player {} reports: {}".format(index, msg))
                    self.send_data(index, msg)
            if self.check_goal():
                self.reset_all()
                controller.inbox.put(Message("reset", None))
                self.message_event.set()
            pygame.display.flip()
            self.clock.tick()
            self.FramePerSec.tick(FPS * self.game_speed)

def print_help():
    print("usage: game.py <showcase number>")
    print("-----------------------------------------------")
    print("1: Goalkeeper defends a striker's goal attempt")
    print("2: Ball is out of line of sight of striker\n")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '1':
            game = Game()
            #Blue Team
            game.add_player((WIDTH - 40, HEIGHT /2), -90, "blue", "keeper")
            #Red Team
            game.add_player((WIDTH/2 -200,200), 90, "red", "striker")
            controller = GameController(game.inbox, list(map(lambda elem : [elem["role"], elem["team"]], game.player_metadata)))
            game.set_controller_inbox(controller.inbox)
            controller_thread = threading.Thread(target = controller.run, args=(game.message_event, ))
            controller_thread.start()
            game.start()
        elif sys.argv[1] == '2':
            game = Game()
            #Blue Team
            game.add_player((WIDTH - 100, HEIGHT /2), 0, "blue", "striker")
            #Red Team
            controller = GameController(game.inbox, list(map(lambda elem : [elem["role"], elem["team"]], game.player_metadata)))
            game.set_controller_inbox(controller.inbox)
            controller_thread = threading.Thread(target = controller.run, args=(game.message_event, ))
            controller_thread.start()
            game.start()
        elif sys.argv[1] == 'debug':
            game = Game()
            #Blue Team
            game.add_player((WIDTH/2 + 280, HEIGHT /2 - 200), -90, "blue", "defender", (WIDTH/2 + 280, HEIGHT /2 - 200), (WIDTH/2 - 100, HEIGHT /2 - 200))
            game.add_player((WIDTH/2 + 280, HEIGHT /2 + 200), -90, "blue", "defender", (WIDTH/2 + 280, HEIGHT /2 + 200), (WIDTH/2 - 100, HEIGHT /2 + 200))
            #Red Team
            controller = GameController(game.inbox, list(map(lambda elem : [elem["role"], elem["team"]], game.player_metadata)))
            game.set_controller_inbox(controller.inbox)
            controller_thread = threading.Thread(target = controller.run, args=(game.message_event, ))
            controller_thread.start()
            game.start()
        else:
            print_help()
    else:
        print_help()