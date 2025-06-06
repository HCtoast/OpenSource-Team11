from .weapon import Weapon
import pygame

class LaserGun(Weapon):
    def __init__(self):
        super().__init__("Laser Gun", base_damage=8, cooldown=300)
        self.acquired = False  # 기본은 미획득
        self.timer = 0

    def fire(self, attacker, target_group, context=None):
        # (임시) 가장 가까운 적 하나에게 데미지 입힘
        closest_target = None
        min_dist = float('inf')

        for target in target_group:
            if not hasattr(target, 'take_damage'):
                continue
            dx = target.rect.centerx - attacker.rect.centerx
            dy = target.rect.centery - attacker.rect.centery
            dist = dx * dx + dy * dy
            if dist < min_dist:
                min_dist = dist
                closest_target = target

        if closest_target:
            closest_target.take_damage(self.calculate_damage())