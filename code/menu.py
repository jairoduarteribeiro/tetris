import pygame

from code.constants import MENU_WIDTH, MENU_HEIGHT
from code.gamestate import GameState


class Menu:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def scale_title(image, max_height):
        width, height = image.get_size()
        scale = max_height / height
        new_size = (int(width * scale), int(height * scale))
        return pygame.transform.scale(image, new_size)

    def run(self):
        self.app.set_resolution(MENU_WIDTH, MENU_HEIGHT)

        background = pygame.image.load('assets/menu.png').convert()
        background = pygame.transform.scale(background, (MENU_WIDTH, MENU_HEIGHT))

        title_img = pygame.image.load('assets/title.png').convert_alpha()
        title_img = self.scale_title(title_img, max_height=60)

        running = True
        while running:
            self.app.screen.blit(background, (0, 0))

            title_rect = title_img.get_rect(center=(MENU_WIDTH // 2, 30))
            self.app.screen.blit(title_img, title_rect)

            pygame.display.flip()
            self.app.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.change_state(GameState.QUIT)
                    running = False
