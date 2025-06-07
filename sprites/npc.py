import pygame
import random
from .spritesheet import SpriteSheet

class NPC(pygame.sprite.Sprite):
    """
    NPC 캐릭터 클래스
    - x: 초기 X 좌표
    - y: 초기 Y 좌표
    """
    def __init__(self, x, y):
        super().__init__()
        
        # 128x384 크기의 스프라이트시트 초기화
        self.sprite_sheet = SpriteSheet("assets/images/npc_red.png", 32, 32)
        
        # 애니메이션 프레임 로드 (각 행별로 다른 애니메이션)
        self.frames = {
            'idle_down': self.sprite_sheet.get_animation_frames(0),   # 1행: 아래쪽 보기
            'walk_down': self.sprite_sheet.get_animation_frames(1),   # 2행: 아래쪽 걷기
            'idle_left': self.sprite_sheet.get_animation_frames(2),   # 3행: 왼쪽 보기
            'walk_left': self.sprite_sheet.get_animation_frames(3),   # 4행: 왼쪽 걷기
            'idle_right': self.sprite_sheet.get_animation_frames(4),  # 5행: 오른쪽 보기
            'walk_right': self.sprite_sheet.get_animation_frames(5),  # 6행: 오른쪽 걷기
            'idle_up': self.sprite_sheet.get_animation_frames(6),     # 7행: 위쪽 보기
            'walk_up': self.sprite_sheet.get_animation_frames(7),     # 8행: 위쪽 걷기
        }
        
        # 초기 상태 설정
        self.current_state = 'idle_down'
        self.current_frame = 0
        self.image = self.frames[self.current_state][self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        
        # AI 관련 변수
        self.speed = 1
        self.direction = random.choice(['down', 'left', 'right', 'up'])
        self.is_moving = False
        self.move_timer = 0
        self.move_duration = random.randint(60, 180)  # 1-3초 (60fps 기준)
        self.idle_duration = random.randint(30, 120)  # 0.5-2초 정지
        
        # 애니메이션 타이밍 설정
        self.animation_speed = 200  # NPC는 더 느린 애니메이션
        self.last_update = pygame.time.get_ticks()

        self.projectile_timer = 0
        self.projectile_cooldown = 800  # Projectile_type 에서 가져오는게 아닌, 임시로 800 할당.
        
        print(f"NPC 생성 완료 - 위치: ({x}, {y})")

    def update(self):
        """NPC 자동 이동 및 애니메이션 업데이트"""
        # AI 이동 로직
        self._update_ai()
        
        # 애니메이션 상태 결정
        if self.is_moving:
            self.current_state = f'walk_{self.direction}'
        else:
            self.current_state = f'idle_{self.direction}'
            
        # 애니메이션 프레임 업데이트
        self._update_animation()

    def _update_ai(self):
        """NPC AI 이동 로직 (내부 메서드)"""
        self.move_timer += 1
        
        if self.is_moving:
            # 이동 중일 때
            if self.direction == 'left':
                self.rect.x -= self.speed
            elif self.direction == 'right':
                self.rect.x += self.speed
            elif self.direction == 'up':
                self.rect.y -= self.speed
            elif self.direction == 'down':
                self.rect.y += self.speed
                
            # 화면 경계 처리
            if self.rect.left <= 0 or self.rect.right >= 800:
                self.direction = random.choice(['up', 'down'])
            if self.rect.top <= 0 or self.rect.bottom >= 600:
                self.direction = random.choice(['left', 'right'])
                
            # 이동 시간이 끝나면 정지
            if self.move_timer >= self.move_duration:
                self.is_moving = False
                self.move_timer = 0
                self.move_duration = random.randint(30, 120)  # 정지 시간
        else:
            # 정지 중일 때
            if self.move_timer >= self.move_duration:
                self.is_moving = True
                self.direction = random.choice(['down', 'left', 'right', 'up'])
                self.move_timer = 0
                self.move_duration = random.randint(60, 180)  # 이동 시간

    def _update_animation(self):
        """애니메이션 프레임 업데이트 (내부 메서드)"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            
            # 현재 상태의 프레임 리스트가 존재하는지 확인
            if self.current_state in self.frames and self.frames[self.current_state]:
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.current_state])
                self.image = self.frames[self.current_state][self.current_frame]
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False