import pygame
import sys
from start_screen import StartScreen
from ui import GameUI
from sprites.player import Player
from sprites.npc import NPC
from sprites.projectile import Projectile, load_projectile_sprites
from sprites.projectile_types import PROJECTILE_TYPES

def main():
    
    """메인 게임 함수"""
    # Pygame 초기화
    pygame.init()
    
    # 화면 설정
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Title")
    
    # 폰트 초기화
    font = pygame.font.Font(None, 36)
    
    # 시작화면 객체 생성 및 표시
    start_screen = StartScreen(screen, font)
    start_screen.draw()  # 시작화면 그리기

    # wait_for_key()가 False를 반환하면 프로그램 종료
    if not start_screen.wait_for_key():
        pygame.quit()
        sys.exit()
    
    # 게임 UI 인스턴스 생성
    game_ui = GameUI(font)
    
    # 플레이어 및 NPC 생성
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    npc = NPC(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2)
    
    
    # 투사체 생성
    projectile_sprites = load_projectile_sprites("assets/images/projectiles.png")

    # 투사체 그룹 생성
    projectiles = pygame.sprite.Group()
    
    # (임시) 기본 투사체 설정(projectile_types 참조)
    projectile_type = PROJECTILE_TYPES["yellow"] # 투사체 색(특성) 가져오기
    projectile_timer = 0
    projectile_cooldown = projectile_type["cooldown"] # 투사체 발사간격 가져오기
    
    
    # 게임 루프
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 게임 상태 업데이트
        keys = pygame.key.get_pressed()
        player.update(keys)
        npc.update()
        
        # 투사체 쿨다운 타이머 증가
        projectile_timer += clock.get_time()
        
        # 쿨타임을 넘어서면 0으로 타이머 리셋시킴
        if projectile_timer >= projectile_cooldown:
            projectile_timer = 0  # 타이머 리셋

       # 현재 projectile_type에서 속성 추출
            index = projectile_type["index"]
            speed = projectile_type["speed"]
            damage = projectile_type["damage"]

            # type에 맞는 속성 적용한 투사체 만들기
            proj = Projectile( 
                # 플레이어 위치와 NPC 위치를 참조(둘 다 중앙에서 시작)하여 속도를 정함
                npc.rect.centerx, npc.rect.centery,
                player.rect.centerx, player.rect.centery,
                projectile_sprites[index],
                speed=speed,
                damage=damage
        )
            # 투사체 group에 추가(화면 벗어나면 삭제됨)
            projectiles.add(proj)

        # 투사체 위치 업뎃
        projectiles.update(clock.get_time())

        
        
        
        
        # UI 업데이트 (예시 값 사용)
        game_ui.update(
            hp=player.hp,  # 실제 HP 값 연결
            exp=player.exp,  # 실제 경험치 값 연결
            level=player.level  # 실제 레벨 값 연결
        )
        
        # 화면 그리기
        screen.fill((30, 30, 30))
    
        
        # 스프라이트 그리기
        screen.blit(player.image, player.rect)
        screen.blit(npc.image, npc.rect)
        
        projectiles.draw(screen)
        
        # UI 그리기
        game_ui.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
