import pygame
import sys
from start_screen import StartScreen
from ui import GameUI
from sprites.player import Player
from sprites.npc import NPC

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
        
        # UI 그리기
        game_ui.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
