import pygame
import math
from .projectile import Projectile

class CrossProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, frames, speed, damage, owner, max_distance=800):
        super().__init__(x, y, target_x, target_y, frames, speed, damage, owner, pierce=999)
        self.origin = pygame.math.Vector2(x, y)
        self.pos = pygame.math.Vector2(x, y)
        self.distance_traveled = 0
        self.max_distance = max_distance

        self.max_distance = max_distance
        self.distance_traveled = 0
        self.returning = False  # 되돌아오는 중인지 여부

        dx, dy = target_x - x, target_y - y
        magnitude = (dx**2 + dy**2) ** 0.5 or 1
        self.speed = speed
        self.direction = pygame.math.Vector2(dx / magnitude, dy / magnitude)

        self.forward_dir = pygame.math.Vector2(dx, dy).normalize()
        self.return_dir = None  # 돌아올 때 계산 (한 번만)

    def update(self, dt):
        if self.returning:
            if self.return_dir is None:
                delta = self.origin - self.pos
                self.return_dir = delta.normalize() if delta.length_squared() > 0 else pygame.math.Vector2(1, 0)
            direction = self.return_dir
        else:
            direction = self.forward_dir

        movement = direction * self.speed
        self.pos += movement
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.pos_x = self.pos.x
        self.pos_y = self.pos.y

        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        # 누적 거리 계산
        self.distance_traveled += movement.length()

        # 되돌아오기 전 조건
        if not self.returning and self.distance_traveled >= self.max_distance:
            self.returning = True

        # 왕복 총 거리 초과 시 소멸
        if self.distance_traveled >= self.max_distance * 3:
            self.kill()