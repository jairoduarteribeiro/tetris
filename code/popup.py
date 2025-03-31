import pygame
from code.constants import COLOR_BLACK, COLOR_YELLOW, COLOR_WHITE, COLOR_RED


class Popup:
    def __init__(
        self,
        app,
        time_text="",
        title="Game Over!",
        prompt="Enter your name:",
        max_length=20,
    ):
        self.app = app
        self.time_text = time_text
        self.screen = app.screen
        self.clock = app.clock
        self.font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 28)
        self.input_text = ""
        self.title = title
        self.prompt = prompt
        self.max_length = max_length

        # Tamanho da área central do popup
        self.popup_width = 400
        self.popup_height = 300
        self.popup_rect = pygame.Rect(
            (self.screen.get_width() - self.popup_width) // 2,
            (self.screen.get_height() - self.popup_height) // 2,
            self.popup_width,
            self.popup_height,
        )

    def run(self):
        active = True

        while active:
            self.screen.fill(COLOR_BLACK)

            # Caixa principal do popup
            pygame.draw.rect(self.screen, (30, 30, 30), self.popup_rect)
            pygame.draw.rect(self.screen, COLOR_WHITE, self.popup_rect, 2)

            center_x = self.popup_rect.centerx

            # Título
            title_surf = self.font.render(self.title, True, COLOR_RED)
            title_rect = title_surf.get_rect(
                center=(center_x, self.popup_rect.top + 40)
            )
            self.screen.blit(title_surf, title_rect)

            time_surf = self.info_font.render(
                f"Your time: {self.time_text}", True, COLOR_WHITE
            )
            time_rect = time_surf.get_rect(center=(center_x, self.popup_rect.top + 75))
            self.screen.blit(time_surf, time_rect)

            # Prompt
            prompt_surf = self.font.render(self.prompt, True, COLOR_WHITE)
            prompt_rect = prompt_surf.get_rect(
                center=(center_x, self.popup_rect.top + 100)
            )
            self.screen.blit(prompt_surf, prompt_rect)

            # Campo de texto (borda + texto)
            input_box = pygame.Rect(center_x - 150, self.popup_rect.top + 150, 300, 50)
            pygame.draw.rect(self.screen, COLOR_WHITE, input_box, 2)

            input_surf = self.font.render(self.input_text, True, COLOR_YELLOW)
            input_rect = input_surf.get_rect(center=input_box.center)
            self.screen.blit(input_surf, input_rect)

            # Instrução final
            info_surf = self.info_font.render(
                "Press ENTER to confirm", True, (200, 200, 200)
            )
            info_rect = info_surf.get_rect(
                center=(center_x, self.popup_rect.bottom - 40)
            )
            self.screen.blit(info_surf, info_rect)

            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < self.max_length:
                            self.input_text += event.unicode
