
# === main.py ===
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'  # 창을 화면 중앙에 띄우기 위한 설정

import pygame
from map1_view import View_Map  

pygame.init()  # pygame 초기화

# 화면 크기 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


view_Map = View_Map("assets//map//map1.tmx")  #객체 생성
  #########################################################################################(확인용)
zoom = 1.0  # 확대 비율 설정
camera_x = (view_Map.map_width - SCREEN_WIDTH / zoom) / 2
camera_y = (view_Map.map_height - SCREEN_HEIGHT / zoom) / 2  # 카메라 초기 위치
  #########################################################################################(확인용용)
clock = pygame.time.Clock()  # 프레임 조절용 시계 객체
running = True  # 게임 루프 상태

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 창 닫으면 종료

    ######################################################################################### 방향키 입력 처리하여 카메라 이동(확인용)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: camera_x -= 10
    if keys[pygame.K_RIGHT]: camera_x += 10
    if keys[pygame.K_UP]: camera_y -= 10
    if keys[pygame.K_DOWN]: camera_y += 10
    ########################################################################################
    # 카메라가 맵 범위를 벗어나지 않도록 제한
    camera_x = max(0, min(camera_x, view_Map.map_width - SCREEN_WIDTH / zoom))
    camera_y = max(0, min(camera_y, view_Map.map_height - SCREEN_HEIGHT / zoom))
    
    screen.fill((0, 0, 0))  # 화면 초기화 (검정 배경)
    view_Map.draw_zoomed(screen, camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT, zoom)  # 확대된 맵 그리기
    pygame.display.flip()  # 화면 갱신
    clock.tick(60)  # FPS 제한 (60프레임)

pygame.quit()  # pygame 종료
