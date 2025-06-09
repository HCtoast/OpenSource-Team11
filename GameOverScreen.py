import pygame
import sys

class GameOverScreen:
    def __init__(self, screen, bg_image_path, font_path=None):
        self.screen = screen
        self.bg_image = pygame.image.load("assets//images//Ending_Screen.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (800,600))
        self.font_small = pygame.font.Font(font_path, 36) if font_path else pygame.font.SysFont(None, 36)
        self.font_button = pygame.font.Font(font_path, 32) if font_path else pygame.font.SysFont(None, 32)

        self.reset_rect = pygame.Rect(0, 0, 200, 50)
        self.exit_rect = pygame.Rect(0, 0, 200, 50)
        self.reset_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 160)
        self.exit_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + 230)

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
        label = self.font_button.render(text, True, (255, 255, 255))
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def show(self, survival_time):
        running = True
        while running:
            self.screen.blit(self.bg_image, (0, 0))

            # 생존 시간 표시
            time_text = self.font_small.render(f"Survival Time: {int(survival_time)} seconds", True, (255, 0, 0))
            time_rect = time_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 +70))
            self.screen.blit(time_text, time_rect)

            # 버튼 그리기
            self.draw_button(self.reset_rect, "Reset")
            self.draw_button(self.exit_rect, "Exit")

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.reset_rect.collidepoint(event.pos):
                        return "reset"
                    elif self.exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            pygame.time.Clock().tick(60)
