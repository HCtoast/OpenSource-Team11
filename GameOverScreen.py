import pygame
import sys

class GameOverScreen:
    def __init__(self, screen, bg_image_path, font_path=None):
        self.screen = screen
        self.bg_image = pygame.image.load(bg_image_path).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        self.font_button = pygame.font.Font(font_path, 32) if font_path else pygame.font.SysFont(None, 32)

        self.reset_rect = pygame.Rect(0, 0, 200, 50)
        self.exit_rect = pygame.Rect(0, 0, 200, 50)
        self.reset_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 160)
        self.exit_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 230)

        self.selected_index = 0  # 0: reset, 1: exit

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        for idx, rect in enumerate([self.reset_rect, self.exit_rect]):
            is_selected = self.selected_index == idx
            color = (255, 255, 255) if is_selected else (180, 180, 180)
            border_color = (255, 255, 0) if is_selected else (100, 100, 100)

            pygame.draw.rect(self.screen, (0, 0, 0), rect)
            pygame.draw.rect(self.screen, border_color, rect, 3)

            label = "Restart" if idx == 0 else "Exit"
            text = self.font_button.render(label, True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def wait_for_choice(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.selected_index = (self.selected_index - 1) % 2
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.selected_index = (self.selected_index + 1) % 2
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        return "reset" if self.selected_index == 0 else "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.reset_rect.collidepoint(event.pos):
                        return "reset"
                    elif self.exit_rect.collidepoint(event.pos):
                        return "exit"
            clock.tick(30)