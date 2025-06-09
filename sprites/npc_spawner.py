import pygame
import random
from .npc import NPC
from .projectile_types import PROJECTILE_TYPES

class NPCSpawner:
    def __init__(self, player, npc_group, projectile_sprites):
        self.player = player
        self.npc_group = npc_group
        self.projectile_sprites = projectile_sprites

        self.spawn_timer = 0
        self.spawn_interval = 3000  # 시작은 3초 간격
        self.elapsed_time = 0  # 게임 총 시간 

        self.base_hp = 100
        self.base_damage = 5

    def update(self, dt):
        self.elapsed_time += dt
        self.spawn_timer += dt

        # 시간이 지날수록 스폰 간격 감소
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_npc()

        # 난이도 증가 (10초마다)
        if self.elapsed_time % 10000 < dt:
            self.base_hp += 10
            self.base_damage += 1
            if self.spawn_interval > 400:
                self.spawn_interval -= 200  # 최소 0.4초까지 줄이기

    def spawn_npc(self):
        screen_w, screen_h = pygame.display.get_surface().get_size()
        px, py = self.player.rect.center
        margin = 400  # 플레이어로부터 이 거리 이내에는 스폰 금지

        while True:
            x = random.randint(0, screen_w)
            y = random.randint(0, screen_h)
            if abs(x - px) > margin or abs(y - py) > margin:
                break

        npc = NPC(x, y)
        npc.health = self.base_hp
        npc.projectile_damage = self.base_damage
        npc.projectile_sprites = self.projectile_sprites
        self.npc_group.add(npc)
