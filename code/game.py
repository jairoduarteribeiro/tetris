import time

import pygame

from code.constants import COLOR_BLACK, COLOR_YELLOW, COLOR_WHITE
from code.gamestate import GameState

ORIGINAL_BOARD_WIDTH = 768
ORIGINAL_BOARD_HEIGHT = 1408
SPACING = 20

MAIN_SCALE = 0.5
MINI_SCALE = 0.25


class Game:
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font(None, 36)
        self.start_time = None

    def format_elapsed_time(self):
        elapsed = int(time.time() - self.start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        return f"{h:02}:{m:02}:{s:02}"

    def run(self):
        self.start_time = time.time()

        main_width = int(ORIGINAL_BOARD_WIDTH * MAIN_SCALE)
        main_height = int(ORIGINAL_BOARD_HEIGHT * MAIN_SCALE)

        mini_width = int(ORIGINAL_BOARD_WIDTH * MINI_SCALE)
        mini_height = int(ORIGINAL_BOARD_HEIGHT * MINI_SCALE)

        screen_width = SPACING + main_width + SPACING + mini_width + SPACING
        screen_height = SPACING + main_height + SPACING

        self.app.set_resolution(screen_width, screen_height)

        board_img = pygame.image.load("assets/board.png").convert_alpha()

        main_board_img = pygame.transform.scale(board_img, (main_width, main_height))
        main_board_pos = (SPACING, SPACING)

        mini_board_img = pygame.transform.scale(board_img, (mini_width, mini_height))
        mini_board_pos = (
            SPACING + main_width + SPACING,
            SPACING + ((main_height - mini_height) // 2),
        )

        title_img = pygame.image.load("assets/title.png").convert_alpha()
        title_scaled_height = int(128 * (mini_width / 371))
        title_img = pygame.transform.scale(title_img, (mini_width, title_scaled_height))

        title_pos = (SPACING + main_width + SPACING, SPACING)

        running = True
        while running:
            self.app.screen.fill(COLOR_BLACK)

            self.app.screen.blit(main_board_img, main_board_pos)

            self.app.screen.blit(title_img, title_pos)

            next_blocks_text = self.font.render("Next Blocks", True, COLOR_WHITE)
            next_blocks_rect = next_blocks_text.get_rect(
                midbottom=(
                    mini_board_pos[0] + mini_width // 2,
                    mini_board_pos[1] - SPACING,
                )
            )
            self.app.screen.blit(next_blocks_text, next_blocks_rect)

            self.app.screen.blit(mini_board_img, mini_board_pos)

            time_text = self.font.render(self.format_elapsed_time(), True, COLOR_YELLOW)
            time_rect = time_text.get_rect(
                midtop=(
                    mini_board_pos[0] + mini_width // 2,
                    mini_board_pos[1] + mini_height + SPACING,
                )
            )

            self.app.screen.blit(time_text, time_rect)

            pygame.display.flip()
            self.app.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.change_state(GameState.MENU)
                    running = False
