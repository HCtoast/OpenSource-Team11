import pygame
import sys
from start_screen import StartScreen
from ui import GameUI
from sprites.player import Player
from sprites.npc import NPC
from sprites.projectile import Projectile, load_projectile_sprites
from sprites.projectile_types import PROJECTILE_TYPES
from sprites.bomb_projectile import BombProjectile
from weapon.bullet_gun import BulletGun
from weapon.laser_gun import LaserGun
from weapon.cross_gun import CrossGun
from weapon.bomb_gun import BombGun

# 충돌 처리를 위한 group 분리
npc_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

BombProjectile.set_npc_group(npc_group)

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
    player_group.add(player)

    npc = NPC(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2)
    npc_group.add(npc)
    for i in range(3):  # 3마리 추가 생성
        npc = NPC(200 + i * 200, 200)
        npc_group.add(npc)
    
    # 투사체 생성
    projectile_sprites = load_projectile_sprites("assets/images/projectiles.png")

    # 투사체 그룹 생성
    projectiles = pygame.sprite.Group()
    
    # (임시) 기본 투사체 설정(projectile_types 참조)
    projectile_type = PROJECTILE_TYPES["yellow"] # 투사체 색(특성) 가져오기
    # projectile_timer = 0
    # projectile_cooldown = projectile_type["cooldown"] # 투사체 발사간격 가져오기

    # (임시) Player 투사체 설정
    player_projectile_type = PROJECTILE_TYPES["blue"]
    player_projectile_timer = 0
    player_projectile_cooldown = projectile_type["cooldown"]

    
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
        
        
        # 플레이어 경험치 
        if player.exp >= 100: 
            for weapon in player.weapons:
                weapon.upgradeweapon()
            player.exp = 0    
            player.level +=1
        
        
        
        for npc in npc_group:
            npc.update()

            # npc 마다 개별적용.
            # 투사체 쿨다운 타이머 증가
            npc.projectile_timer += clock.get_time()
            
            # 쿨타임을 넘어서면 0으로 타이머 리셋시킴
            if npc.projectile_timer >= npc.projectile_cooldown:
                npc.projectile_timer = 0  # 타이머 리셋

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
                    damage=damage,
                    owner=npc
                )
                # 투사체 group에 추가(화면 벗어나면 삭제됨)
                projectiles.add(proj)
        
        # 무기
        for weapon in player.weapons:
            if weapon.acquired:
                weapon.update_timer(clock.get_time())
                if weapon.can_fire():
                    if isinstance(weapon, BulletGun):
                        proj = weapon.fire(player, npc, projectile_sprites)
                        projectiles.add(proj)
                    elif isinstance(weapon, CrossGun):
                        proj = weapon.fire(player, npc, projectile_sprites)
                        projectiles.add(proj)
                    elif isinstance(weapon, LaserGun):
                        weapon.fire(player, npc_group)
                    elif isinstance(weapon, BombGun):
                        proj = weapon.fire(player, npc, projectile_sprites)
                        projectiles.add(proj)
                        

        # 투사체 위치 업뎃
        projectiles.update(clock.get_time())

        # NPC 충돌 처리
        collisions = pygame.sprite.groupcollide(npc_group, projectiles, False, False)
        for target, hit_projectiles in collisions.items():
            for proj in hit_projectiles:
                if proj.owner != target:
                    if hasattr(target, 'take_damage'):
                        dead = target.take_damage(proj.damage)
                        if dead:
                            player.exp += 50
                        proj.pierce -= 1  # 관통 수 감소
                        if proj.pierce < 0:
                            proj.kill()

        # 플레이어 충돌 처리
        player_collisions = pygame.sprite.spritecollide(player, projectiles, False, pygame.sprite.collide_mask)
        for proj in player_collisions:
            if proj.owner != player:
                player.take_damage(proj.damage)
                proj.kill()
        
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
        # npc가 kill 당해서 npc_group에서 빠지면 그리지 않음.
        for npc in npc_group:
            screen.blit(npc.image, npc.rect)
        
        projectiles.draw(screen)
        
        # UI 그리기
        game_ui.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

# 디버깅용 try 처리
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()  # 오류 전체 출력
        input("오류가 발생했습니다. Enter를 눌러 종료합니다...")
