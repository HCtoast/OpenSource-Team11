from sprites.projectile import Projectile
from .weapon import Weapon

class BulletGun(Weapon):
    def __init__(self, sprite_index):
        super().__init__("Bullet Gun", base_damage=10, cooldown=400)
        self.sprite_index = sprite_index

    def fire(self, attacker, target, projectile_sprites):
        proj = Projectile(
            x=attacker.rect.centerx,
            y=attacker.rect.centery,
            target_x=target.rect.centerx,
            target_y=target.rect.centery,
            frames=projectile_sprites[self.sprite_index],
            speed=6,
            damage=self.calculate_damage(),
            owner=attacker
        )
        return proj