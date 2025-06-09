import pygame
import time

class GameUI:
    def __init__(self, font):
        self.font = font
        self.max_hp = 100
        self.current_hp = 100
        self.max_exp = 100
        self.current_exp = 0
        self.level = 1
        self.start_time = time.time()
        self.paused = False
        
    def update(self, hp, exp, level, paused):
        self.current_hp = hp
        self.current_exp = exp
        self.level = level
        self.paused = paused

    def draw_bar(self, surface, x, y, w, h, ratio, color_bg, color_fg):
        pygame.draw.rect(surface, color_bg, (x, y, w, h))
        pygame.draw.rect(surface, color_fg, (x, y, int(w * ratio), h))

    def draw(self, surface, paused_surface):
        # 체력 바
        self.draw_bar(surface, 20, 20, 200, 20, self.current_hp / self.max_hp, (100, 0, 0), (255, 0, 0))
        hp_text = self.font.render("HP", True, (255, 255, 255))
        surface.blit(hp_text, (230, 20))

        # 경험치 바
        self.draw_bar(surface, 20, 50, 200, 10, self.current_exp / self.max_exp, (50, 50, 50), (0, 200, 255))

        # 레벨 표시
        level_text = self.font.render(f"Lv. {self.level}", True, (255, 255, 0))
        surface.blit(level_text, (20, 70))

        # 생존 시간
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        time_text = self.font.render(f"Time: {mins:02}:{secs:02}", True, (255, 255, 255))
        surface.blit(time_text, (20, 100))
        
        if self.paused:
            paused_surface.fill((0, 0, 0, 150))

            p1 = self.font.render("PAUSED", True, (255, 255, 255))
            paused_surface.blit(p1, (280, 20))
            p1 = self.font.render("Press [Enter] key to escape !", True, (255, 30, 30))
            paused_surface.blit(p1, (170, 230))
            
            surface.blit(paused_surface, (80, 60))
