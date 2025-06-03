import pygame
from navmesh_animator import NavMeshAnimator

SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680
CELL_SIZE = 32

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

animator = NavMeshAnimator(CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
start_px, start_py = 5 * CELL_SIZE, 5 * CELL_SIZE
animator.SetPosition(start_px, start_py)

# 루프
running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            animator.SetTargetPosition(mx, my)

    screen.fill((30, 30, 30))

    x, y = animator.update(dt)

    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), CELL_SIZE // 4)
    pygame.display.flip()

pygame.quit()
