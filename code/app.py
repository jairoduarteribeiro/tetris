import pygame

from code.game import Game
from code.gamestate import GameState
from code.menu import Menu
from code.scoreboard import Scoreboard


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU

        self.menu = Menu(self)
        self.game = Game(self)
        self.scoreboard = Scoreboard(self)

    def run(self):
        while self.state != GameState.QUIT:
            if self.state == GameState.MENU:
                self.menu.run()
            elif self.state == GameState.PLAYING:
                self.game.run()
            elif self.state == GameState.SCOREBOARD:
                self.scoreboard.run()

        pygame.quit()

    def change_state(self, new_state: GameState):
        self.state = new_state

    def set_resolution(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
