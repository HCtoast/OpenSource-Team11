class Weapon:
    def __init__(self, name, base_damage, cooldown):
        self.name = name
        self.base_damage = base_damage
        self.cooldown = cooldown
        self.level = 1
        self.timer = 0
        self.acquired = False

    def calculate_damage(self):
        # (임시) 데미지 계산 공식
        return self.base_damage + self.level * 2

    def update_timer(self, dt):
        self.timer += dt

    def can_fire(self):
        if self.timer >= self.cooldown:
            self.timer = 0
            return True
        return False

    def fire(self, attacker, target, context):
        raise NotImplementedError  # 자식 클래스에서 override
