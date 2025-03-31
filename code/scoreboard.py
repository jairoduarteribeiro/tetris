import pygame
from code.constants import SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT
from code.gamestate import GameState


class Scoreboard:
    def __init__(self, app):
        self.app = app
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 28)

    def run(self):
        self.app.set_resolution(SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)

        running = True
        while running:
            self.app.screen.fill((0, 0, 0))

            title = self.title_font.render("Scoreboard", True, (255, 255, 255))
            title_rect = title.get_rect(center=(SCOREBOARD_WIDTH // 2, 80))
            self.app.screen.blit(title, title_rect)

            message = self.info_font.render("Not implemented", True, (255, 0, 0))
            message_rect = message.get_rect(center=(SCOREBOARD_WIDTH // 2, 160))
            self.app.screen.blit(message, message_rect)

            return_msg = self.info_font.render(
                "Press ENTER to return to Menu", True, (200, 200, 200)
            )
            return_rect = return_msg.get_rect(
                center=(SCOREBOARD_WIDTH // 2, SCOREBOARD_HEIGHT - 60)
            )
            self.app.screen.blit(return_msg, return_rect)

            pygame.display.flip()
            self.app.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                ):
                    self.app.change_state(GameState.MENU)
                    running = False
