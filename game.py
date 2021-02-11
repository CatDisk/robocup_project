import pygame
from pygame import display
from pygame.locals import *

from field import Field
from player import Player

HEIGHT = 64 * 7
WIDTH = 64 * 12
FPS = 60

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.FramePerSec = pygame.time.Clock()
        pygame.display.set_caption("2D Robocup")
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.player_speed = 1.5
        self.running = True
        self.players = []
        self.field = Field(self.display)
        self.field.update()
        self.player_spites = {
            "red": pygame.image.load("./assets/player_red.png"),
            "blue": pygame.image.load("./assets/player_blue.png"),
        }

    def add_player(self, pos, dir, team = "red"):
        self.players.append(Player(pos, dir, self.player_speed, self.player_spites[team], self.display))

    def start(self):
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.field.update()
            for entity in self.players:
                entity.update()

            pygame.display.flip()
            self.FramePerSec.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.add_player((100, 100), 0)
    game.add_player((100, 300), 180, "blue")
    game.players[0].go_to((500, 200))
    game.players[1].go_to((500, 200))
    game.start()