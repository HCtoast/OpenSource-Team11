from sprites.projectile import Projectile
from .weapon import Weapon

class BulletGun(Weapon):
    def __init__(self, sprite_index):
        super().__init__("Bullet Gun", base_damage=10, cooldown=400)
        self.sprite_index = 6
        self.projectilespeed = 6
        self.pierce = 0
        self.acquired = False

    def fire(self, attacker, target, projectile_sprites):
        proj = Projectile(
            x=attacker.rect.centerx,
            y=attacker.rect.centery,
            target_x=target.rect.centerx,
            target_y=target.rect.centery,
            frames=projectile_sprites[self.sprite_index],
            speed=self.projectilespeed,
            damage=self.calculate_damage(),
            owner=attacker,
            pierce=self.pierce
        )
        return proj
    
    def upgradeweapon(self):
        self.level += 1
        self.base_damage += 1
        self.projectilespeed += 1
        self.cooldown = self.cooldown*0.92
        self.pierce = self.level - 1