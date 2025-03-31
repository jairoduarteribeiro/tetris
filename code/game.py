import time
import pygame

from code.block import BlockFactory
from code.board import Board
from code.constants import COLOR_BLACK, COLOR_YELLOW, COLOR_WHITE
from code.database import insert
from code.gamestate import GameState
from code.popup import Popup

ORIGINAL_BOARD_WIDTH = 768
ORIGINAL_BOARD_HEIGHT = 1408
SPACING = 20
BLOCK_SIZE = 64

MAIN_SCALE = 0.5
MINI_SCALE = 0.25


class Game:
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font(None, 36)
        self.start_time = None
        self.elapsed_time = None

    def update_time(self):
        self.elapsed_time = int(time.time() - self.start_time)

    def format_elapsed_time(self):
        h = self.elapsed_time // 3600
        m = (self.elapsed_time % 3600) // 60
        s = self.elapsed_time % 60
        return f"{h:02}:{m:02}:{s:02}"

    def run(self):
        self.start_time = time.time()
        self.last_speedup = self.start_time

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

        play_area_origin = (
            main_board_pos[0] + BLOCK_SIZE * MAIN_SCALE,
            main_board_pos[1] + BLOCK_SIZE * MAIN_SCALE,
        )

        mini_board_img = pygame.transform.scale(board_img, (mini_width, mini_height))
        mini_board_pos = (
            SPACING + main_width + SPACING,
            SPACING + ((main_height - mini_height) // 2),
        )

        preview_area_origin = (
            mini_board_pos[0] + BLOCK_SIZE * MINI_SCALE,
            mini_board_pos[1] + BLOCK_SIZE * MINI_SCALE,
        )

        title_img = pygame.image.load("assets/title.png").convert_alpha()
        title_scaled_height = int(128 * (mini_width / 371))
        title_img = pygame.transform.scale(title_img, (mini_width, title_scaled_height))

        title_pos = (SPACING + main_width + SPACING, SPACING)

        self.block_queue = [BlockFactory.create_random_block() for _ in range(5)]
        self.active_block = self.block_queue.pop(0)
        self.active_block.set_position(4, 0)

        self.board = Board()

        self.drop_time = time.time()
        self.drop_interval = 1

        running = True
        while running:
            current_time = time.time()
            if current_time - self.last_speedup >= 60:
                self.drop_interval = max(0.1, self.drop_interval - 0.1)
                self.last_speedup = current_time
            if current_time - self.drop_time > self.drop_interval:
                self.active_block.move_down()
                if not self.active_block.is_within_bounds() or self.board.collides(
                    self.active_block
                ):
                    self.active_block.move_up()
                    self.board.fix_block(self.active_block)
                    self.board.clear_lines()

                    self.active_block = self.block_queue.pop(0)
                    self.active_block.set_position(4, 0)
                    self.block_queue.append(BlockFactory.create_random_block())

                    if self.board.collides(self.active_block):
                        popup = Popup(self.app, time_text=self.format_elapsed_time())
                        name = popup.run()
                        insert(name, self.elapsed_time)
                        self.app.change_state(GameState.MENU)
                        break

                self.drop_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app.change_state(GameState.MENU)
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.active_block.rotate()
                        if (
                            not self.active_block.is_within_bounds()
                            or self.board.collides(self.active_block)
                        ):
                            self.active_block.rotate_back()
                    elif event.key == pygame.K_LEFT:
                        self.active_block.move_left()
                        if (
                            not self.active_block.is_within_bounds()
                            or self.board.collides(self.active_block)
                        ):
                            self.active_block.move_right()
                    elif event.key == pygame.K_RIGHT:
                        self.active_block.move_right()
                        if (
                            not self.active_block.is_within_bounds()
                            or self.board.collides(self.active_block)
                        ):
                            self.active_block.move_left()
                    elif event.key == pygame.K_DOWN:
                        self.active_block.move_down()
                        if (
                            not self.active_block.is_within_bounds()
                            or self.board.collides(self.active_block)
                        ):
                            self.active_block.move_up()

            self.app.screen.fill(COLOR_BLACK)
            self.app.screen.blit(main_board_img, main_board_pos)
            self.board.render(self.app.screen, play_area_origin, BLOCK_SIZE, MAIN_SCALE)
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

            self.update_time()
            time_text = self.font.render(self.format_elapsed_time(), True, COLOR_YELLOW)
            time_rect = time_text.get_rect(
                midtop=(
                    mini_board_pos[0] + mini_width // 2,
                    mini_board_pos[1] + mini_height + SPACING,
                )
            )
            self.app.screen.blit(time_text, time_rect)

            for x, y in self.active_block.get_cells():
                pixel_x = play_area_origin[0] + x * BLOCK_SIZE * MAIN_SCALE
                pixel_y = play_area_origin[1] + y * BLOCK_SIZE * MAIN_SCALE
                img = self.active_block.get_image()
                scaled = pygame.transform.scale(
                    img,
                    (
                        int(BLOCK_SIZE * MAIN_SCALE),
                        int(BLOCK_SIZE * MAIN_SCALE),
                    ),
                )
                self.app.screen.blit(scaled, (pixel_x, pixel_y))

            preview_positions = [(4, 2), (4, 7), (4, 12), (4, 17)]
            for i, block in enumerate(self.block_queue):
                block.set_position(*preview_positions[i])
                for x, y in block.get_cells():
                    pixel_x = preview_area_origin[0] + x * BLOCK_SIZE * MINI_SCALE
                    pixel_y = preview_area_origin[1] + y * BLOCK_SIZE * MINI_SCALE
                    img = block.get_image()
                    scaled = pygame.transform.scale(
                        img,
                        (
                            int(BLOCK_SIZE * MINI_SCALE),
                            int(BLOCK_SIZE * MINI_SCALE),
                        ),
                    )
                    self.app.screen.blit(scaled, (pixel_x, pixel_y))

            pygame.display.flip()
            self.app.clock.tick(60)
