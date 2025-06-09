import pygame
from .spritesheet import SpriteSheet
from weapon.bullet_gun import BulletGun
from weapon.laser_gun import LaserGun
from weapon.cross_gun import CrossGun
from weapon.garlic_aura import Garlic
from weapon.bomb_gun import BombGun

class Player(pygame.sprite.Sprite):
    """
    플레이어 캐릭터 클래스
    - x: 초기 X 좌표
    - y: 초기 Y 좌표
    """
    def __init__(self, x, y, garlic_image):
        super().__init__()

        self.hp = 100      # 플레이어 체력
        self.exp = 0       # 경험치
        self.level = 1     # 레벨
        
        # 128x384 크기의 스프라이트시트 초기화
        self.sprite_sheet = SpriteSheet("assets/images/player.png", 32, 32)
        
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

        # 충돌 판정을 위한 mask 정의
        self.mask = pygame.mask.from_surface(self.image)

        # 이동 관련 변수
        self.speed = 3
        self.direction = 'down'  # 현재 바라보는 방향
        self.is_moving = False   # 이동 중인지 여부
        
        # 애니메이션 타이밍 설정
        self.animation_speed = 150  # 밀리초 단위
        self.last_update = pygame.time.get_ticks()
        
        print("플레이어 생성 완료")

        # 플레이어 무기 목록
        self.weapons = []

    def update(self, keys):
        """
        프레임 업데이트, 이동 처리 및 애니메이션 처리
        - keys: 키보드 입력 상태
        """
        # 이전 위치 저장
        prev_x, prev_y = self.rect.x, self.rect.y
        
        # 키 입력에 따른 이동 처리
        self.is_moving = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = 'left'
            self.is_moving = True
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = 'right'
            self.is_moving = True
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = 'up'
            self.is_moving = True
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = 'down'
            self.is_moving = True
        
        # 화면 경계 처리
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:  # 화면 너비
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:  # 화면 높이
            self.rect.bottom = 600
            
        # 애니메이션 상태 결정
        if self.is_moving:
            self.current_state = f'walk_{self.direction}'
        else:
            self.current_state = f'idle_{self.direction}'
        
        # 애니메이션 프레임 업데이트
        self._update_animation()

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
            self.hp -= amount
            if self.hp <= 0:
                self.kill()