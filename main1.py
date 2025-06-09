import os
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
from weapon_select_screen import WeaponSelectScreen
from weapon.garlic_aura import Garlic
from map1_view import View_Map
from GameOverScreen import GameOverScreen
from weapon.bomb_gun import BombGun
from sprites.npc_spawner import NPCSpawner



def main():
    # 충돌 처리를 위한 group 분리
    npc_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    BombProjectile.set_npc_group(npc_group)
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
    
    
    # 무기 선택 화면 호출
    weapon_selector = WeaponSelectScreen(screen, font)
    selected_weapon_names = weapon_selector.select()
    
    # 게임 UI 인스턴스 생성
    game_ui = GameUI(font)
    
    # 마늘 무기 이미지 생성
    base_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_path, "assets", "images", "garlic_aura.png")
    garlic_image = pygame.image.load(image_path).convert_alpha()

    # 플레이어 및 NPC 생성
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, garlic_image=garlic_image)
    player_group.add(player)

    

    # 선택된 무기 장착
    for name in selected_weapon_names:
        if name == "Bullet Gun":
            bullet_gun = BulletGun(sprite_index=6)
            bullet_gun.acquired = True
            player.weapons.append(bullet_gun)
        elif name == "Laser":
            laser_gun = LaserGun(player)
            laser_gun.acquired = True
            player.weapons.append(laser_gun)
        elif name == "Cross Gun":
            cross = CrossGun(sprite_index=7)
            cross.acquired = True
            player.weapons.append(cross)
        elif name == "Garlic":
            garlic_aura = Garlic(player=player, image=garlic_image)
            garlic_aura.acquired = True
            player.weapons.append(garlic_aura)
        elif name == "Bomb":
            Bomb = BombGun(sprite_index=8)
            Bomb.acquired = True
            player.weapons.append(Bomb)
    
    
    
    
    
    
    
    
    

    npc = NPC(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2)
    npc_group.add(npc)
    for i in range(3):  # 3마리 추가 생성
        npc = NPC(200 + i * 200, 200)
        npc_group.add(npc)

    
    # 투사체 생성
    projectile_sprites = load_projectile_sprites("assets/images/projectiles.png")

    # 투사체 그룹 생성
    projectiles = pygame.sprite.Group()

    # npc spawner 생성
    spawner = NPCSpawner(player, npc_group, projectile_sprites)
    
    # (임시) 기본 투사체 설정(projectile_types 참조)
    projectile_type = PROJECTILE_TYPES["yellow"] # 투사체 색(특성) 가져오기
    # projectile_timer = 0
    # projectile_cooldown = projectile_type["cooldown"] # 투사체 발사간격 가져오기

    # (임시) Player 투사체 설정
    player_projectile_type = PROJECTILE_TYPES["blue"]
    player_projectile_timer = 0
    player_projectile_cooldown = projectile_type["cooldown"]
    #맵 객체생성
    view_Map = View_Map("assets/map/map1.tmx")
    # TMX 맵 초기화

    
    # 게임 루프
    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  # 생존 시간 측정용
    while running:
                
        # 화면 그리기
        view_Map.draw_stretched_to_screen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
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
        
        spawner.update(clock.get_time())
        
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

                if hasattr(weapon, 'aura'):
                    weapon.update(clock.get_time(), npc_group)

                if weapon.can_fire():

                    # 가장 가까운 npc 찾기
                    if len(npc_group) > 0:
                        closest_npc = min(
                            npc_group,
                            key=lambda n: (player.rect.centerx - n.rect.centerx)**2 + (player.rect.centery - n.rect.centery)**2)
                        if isinstance(weapon, BulletGun):
                            proj = weapon.fire(player, closest_npc, projectile_sprites)
                            projectiles.add(proj)
                        if isinstance(weapon, CrossGun):
                            proj = weapon.fire(player, closest_npc, projectile_sprites)
                            projectiles.add(proj)
                        if isinstance(weapon, BombGun):
                            proj = weapon.fire(player, closest_npc, projectile_sprites)
                            projectiles.add(proj)
                    else:
                        closest_npc = None
                    if isinstance(weapon, LaserGun):
                        weapon.update(clock.get_time(), npc_group, player)
                        #weapon.fire(player, npc_group,projectile_sprites)

        # 투사체 위치 업뎃
        projectiles.update(clock.get_time())

        # NPC 충돌 처리
        collisions = pygame.sprite.groupcollide(npc_group, projectiles, False, False)
        for target, hit_projectiles in collisions.items():
            for proj in hit_projectiles:
                if proj.owner != target:
                    if hasattr(target, 'take_damage'):
                        dead = target.take_damage(proj.damage,player)
                        #if dead:
                            #player.exp += 50
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

        # 마늘 및 레이저 무기 그리기
        for weapon in player.weapons:
            if weapon.acquired and hasattr(weapon, 'aura'):
                screen.blit(weapon.aura.image, weapon.aura.rect)
            if weapon.acquired and isinstance(weapon, LaserGun):
                weapon.draw(screen, player)

        # 플레이어 그리기
        screen.blit(player.image, player.rect)

        # npc가 kill 당해서 npc_group에서 빠지면 그리지 않음.
        for npc in npc_group:
            screen.blit(npc.image, npc.rect)
        
        # 투사체
        projectiles.draw(screen)
        
        # UI 그리기
        game_ui.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
                # 게임 오버 조건 확인
        if player.hp <= 0:
            survival_time = (pygame.time.get_ticks() - start_time) / 1000  # ms → sec
            gameover_screen = GameOverScreen(screen, "assets/images/Ending_Screen.png")
            result = gameover_screen.show(survival_time)

            if result == "reset":
                main()  # 게임 재시작
            else:
                running = False
    
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
