from .weapon import Weapon
import pygame
import math

class LaserGun(Weapon):
    def __init__(self):
        super().__init__("Laser Gun", base_damage=8, cooldown=300)
        self.timer = 0
        self.range = 250  # 기본 사거리
        self.max_targets = 2  # 타겟 수 (레벨 1)
        self.targets = set()  # 현재 타겟팅된 적
        self.acquired = False

    def update(self, dt, npc_group, attacker):
        self.timer += dt

        # 현재 타겟 중 사거리 밖으로 나간 적 제거
        to_remove = set()
        for npc in self.targets:
            if not npc.alive() or not self._within_range(attacker, npc):
                to_remove.add(npc)
        self.targets -= to_remove

        # 타겟 부족 시 새로 추가
        available_targets = [
            npc for npc in npc_group
            if npc not in self.targets and self._within_range(attacker, npc)
        ]
        available_targets.sort(key=lambda n: self._distance(attacker, n))

        while len(self.targets) < self.max_targets and available_targets:
            self.targets.add(available_targets.pop(0))

        # 타겟에 지속 피해 적용
        if self.timer >= self.cooldown:
            for npc in self.targets:
                if hasattr(npc, "take_damage"):
                    npc.take_damage(self.calculate_damage())
            self.timer = 0

    def _within_range(self, attacker, npc):
        return self._distance(attacker, npc) <= self.range

    def _distance(self, a, b):
        dx = a.rect.centerx - b.rect.centerx
        dy = a.rect.centery - b.rect.centery
        return math.hypot(dx, dy)

    def upgradeweapon(self):
        self.max_targets += 1
        self.range += 20

    def draw(self, screen, attacker):
        # 반투명 서피스 생성
        laser_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        laser_color = (255, 200, 0, 153)  # 알파 153 ≈ 60% 투명도

        for npc in self.targets:
            if npc.alive():
                start_pos = attacker.rect.center
                end_pos = npc.rect.center
                pygame.draw.line(laser_surface, laser_color, start_pos, end_pos, 3)

        # 화면 위에 덧씌움
        screen.blit(laser_surface, (0, 0))