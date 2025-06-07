import pygame
from sprites.projectile import Projectile

class BombProjectile(Projectile):
    npc_group = None  # 외부에서 set_npc_group으로 설정

    def __init__(self, x, y, target_x, target_y, frames, speed, damage, owner, radius):
        super().__init__(x, y, target_x, target_y, frames, speed, damage, owner)
        self.radius = radius
        self.animation_timer = 0
        self.animation_speed = 40

    def update(self, dt):
        super().update(dt)

        if BombProjectile.npc_group:
            for npc in BombProjectile.npc_group:
                if self.rect.colliderect(npc.rect):
                    self.explode()
                    self.kill()
                    break

    def explode(self):
        for npc in BombProjectile.npc_group:
            dist = pygame.math.Vector2(self.rect.center).distance_to(npc.rect.center)
            if dist <= self.radius and hasattr(npc, "take_damage"):
                npc.take_damage(self.damage)

    @classmethod
    def set_npc_group(cls, group):
        cls.npc_group = group
