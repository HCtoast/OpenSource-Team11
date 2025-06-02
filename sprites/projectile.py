import pygame
import math

# 스프라이트 시트 불러오기(현재 projectile.png는 6종류의 투사체가 5프레임짜리로 들어가 있음)
def load_projectile_sprites(sheet_path):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    return load_projectile_frames(sheet, frame_width=16, frame_height=16, rows=6, cols=5)


# 투사체 애니메이션
def load_projectile_frames(sheet, frame_width, frame_height, rows, cols):
    sprites = []
    sheet_width, sheet_height = sheet.get_size()

    for row in range(rows):
        frames = []
        for col in range(cols):
            x = col * frame_width
            y = row * frame_height
            if x + frame_width > sheet_width or y + frame_height > sheet_height:
                continue 
            rect = pygame.Rect(x, y, frame_width, frame_height)
            frame = sheet.subsurface(rect).convert_alpha()
            frames.append(frame)
        sprites.append(frames)
    return sprites

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, frames, speed, damage):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_timer = 0
        
        # 투사체 애니메이션 프레임 간 간격 (40~60정도가 적당해보입니다)
        self.animation_speed = 40
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        # 투사체 위치 저장용
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

        # 속도
        dx = target_x - x
        dy = target_y - y
        angle = math.atan2(dy, dx)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.damage = damage


    def update(self, dt):
        # 💡 부동소수점으로 위치 이동
        self.pos_x += self.vx
        self.pos_y += self.vy
        self.rect.center = (round(self.pos_x), round(self.pos_y))

        # 애니메이션 처리 그대로
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # 화면 밖이면 제거
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.kill()
