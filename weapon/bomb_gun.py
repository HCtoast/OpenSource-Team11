from sprites.bomb_projectile import BombProjectile
from .weapon import Weapon

class BombGun(Weapon):
    def __init__(self, sprite_index):
        super().__init__("Bomb Gun", base_damage=30, cooldown=2400)
        self.sprite_index = sprite_index
        self.projectilespeed = 3
        self.acquired = False  # 기본은 미획득

    def fire(self, attacker, target, projectile_sprites):
        radius = 100 + self.level * 20
        proj = BombProjectile(
            x=attacker.rect.centerx,
            y=attacker.rect.centery,
            target_x=target.rect.centerx,
            target_y=target.rect.centery,
            frames=projectile_sprites[self.sprite_index],
            speed=self.projectilespeed,
            damage=self.calculate_damage(),
            owner=attacker,
            radius=radius
        )
        return proj

    def upgradeweapon(self):
        pass