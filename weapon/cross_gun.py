from .weapon import Weapon
from sprites.cross_projectile import CrossProjectile

class CrossGun(Weapon):
    def __init__(self, sprite_index):
        super().__init__("Cross Gun", base_damage=5, cooldown=600)
        self.sprite_index = sprite_index
        self.acquired = False

    def fire(self, attacker, target, projectile_sprites):
        return CrossProjectile(
            x=attacker.rect.centerx,
            y=attacker.rect.centery,
            target_x=target.rect.centerx,
            target_y=target.rect.centery,
            frames=projectile_sprites[self.sprite_index],
            speed=4,
            damage=self.calculate_damage(),
            owner=attacker,
            max_distance=100 + self.level * 20  # 업그레이드에 따른 이동 거리 증가
        )
    
    def upgradeweapon(self):
        self.level += 1
        # 업그레이드 로직 여기에 작성
