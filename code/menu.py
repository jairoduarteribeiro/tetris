import pygame

from code.constants import MENU_WIDTH, MENU_HEIGHT, COLOR_YELLOW, COLOR_WHITE
from code.gamestate import GameState


class Menu:
    def __init__(self, app):
        self.app = app
        self.options = [
            ("Start Game", GameState.PLAYING),
            ("Scoreboard", GameState.SCOREBOARD),
            ("Quit Game", GameState.QUIT)
        ]
        self.selected = 0
        self.font = pygame.font.Font(None, 48)

    @staticmethod
    def scale_title(image, max_height):
        width, height = image.get_size()
        scale = max_height / height
        new_size = (int(width * scale), int(height * scale))
        return pygame.transform.scale(image, new_size)

    def render_options(self):
        option_spacing = 60
        total_height = len(self.options) * option_spacing
        start_y = (MENU_HEIGHT // 2) - (total_height // 2)
        for i, (text, _) in enumerate(self.options):
            color = COLOR_YELLOW if i == self.selected else COLOR_WHITE
            rendered = self.font.render(text, True, color)
            rect = rendered.get_rect(center=(MENU_WIDTH // 2, start_y + i * option_spacing))
            self.app.screen.blit(rendered, rect)

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

            self.render_options()

            pygame.display.flip()
            self.app.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.change_state(GameState.QUIT)
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.app.change_state(self.options[self.selected][1])
                        running = False
