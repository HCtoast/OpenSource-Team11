# garlic_aura.py
import pygame
from .weapon import Weapon

class Garlic(Weapon):
    def __init__(self, player, image):
        super().__init__(name="Garlic", base_damage=1, cooldown=0)
        self.player = player
        self.radius = 200
        self.slow_factor = 0.5
        self.acquired = False

        # 전달받은 image로 스케일 조정
        scale_factor = self.radius / image.get_width()
        size = int(image.get_width() * scale_factor)
        scaled_image = pygame.transform.scale(image, (size, size))

        # 내부 aura 스프라이트
        self.aura = pygame.sprite.Sprite()
        self.aura.image = scaled_image
        self.aura.image.set_alpha(80)
        self.aura.rect = self.aura.image.get_rect(center=self.player.rect.center)
        self.aura.mask = pygame.mask.from_surface(self.aura.image)

        self.tick_timer = 0
        self.tick_interval = 200

        # upgrade 시 다시 사용할 원본 이미지 저장
        self.original_image = image

    def update(self, dt, npc_group):
        self.aura.rect.center = self.player.rect.center
        self.tick_timer += dt
        if self.tick_timer >= self.tick_interval:
            self.tick_timer = 0
            self.apply_effects(npc_group)

    def apply_effects(self, npc_group):
        for npc in npc_group:
            if self.aura.rect.colliderect(npc.rect):
                offset = (npc.rect.left - self.aura.rect.left, npc.rect.top - self.aura.rect.top)
                if self.aura.mask.overlap(pygame.mask.from_surface(npc.image), offset):
                    if hasattr(npc, "take_damage"):
                        npc.take_damage(self.base_damage, self.player)
                    if hasattr(npc, "apply_slow"):
                        npc.apply_slow(self.slow_factor)

    def upgradeweapon(self):
        self.radius += 30
        scale_factor = self.radius / self.original_image.get_width()
        new_size = int(self.original_image.get_width() * scale_factor)
        scaled_image = pygame.transform.scale(self.original_image, (new_size, new_size))

        self.aura.image = scaled_image
        self.aura.image.set_alpha(80)
        self.aura.rect = self.aura.image.get_rect(center=self.player.rect.center)
        self.aura.mask = pygame.mask.from_surface(self.aura.image)
