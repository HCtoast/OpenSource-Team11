# NavMeshAgent 클래스 멤버변수랑 메서드가 많아서 사용법 코드까지 짜봤습니다.
# 조작: 마우스 좌클릭으로 도착지점 갱신

import pygame
import random
from navmesh_agent import NavMeshAgent, BLOCKTYPE

pygame.init()

CELL_SIZE = 32
MAP_WIDTH = 640 # 32 x 20 (픽셀이미지 20장)
MAP_HEIGHT = 640
SCREEN = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
CLOCK = pygame.time.Clock()

COLS = MAP_WIDTH
ROWS = MAP_HEIGHT

agent = NavMeshAgent(CELL_SIZE, CELL_SIZE, MAP_WIDTH, MAP_HEIGHT)

# 벽 랜덤 생성
for _ in range(100):
    x = random.randint(0, agent.width - 1)
    y = random.randint(0, agent.height - 1)
    agent.SetBlockType(x, y, BLOCKTYPE.WALL)

# 시작지점 설정
start = (1, 1)
agent.SetBlockType(*start, BLOCKTYPE.BEGIN)
agent.SetPosition(*start)
agent.SetOption(1, 1, 1) # 임시값

# 경로 초기화
path = []

def draw_grid():
    for y in range(agent.height):
        for x in range(agent.width):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            block = agent.map[y][x]

            if block == BLOCKTYPE.VOID:
                pygame.draw.rect(SCREEN, (255, 255, 255), rect)
            elif block == BLOCKTYPE.WALL:
                pygame.draw.rect(SCREEN, (0, 0, 0), rect)
            elif block == BLOCKTYPE.BEGIN:
                pygame.draw.rect(SCREEN, (0, 255, 0), rect)
            elif block == BLOCKTYPE.END:
                pygame.draw.rect(SCREEN, (255, 0, 0), rect)

    if path:
        for (x, y) in path:
            pygame.draw.rect(SCREEN, (0, 0, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def main():
    global path
    running = True

    while running:
        CLOCK.tick(60)
        SCREEN.fill((200, 200, 200))
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                grid_x = mx // CELL_SIZE
                grid_y = my // CELL_SIZE

                if 0 <= grid_x < agent.width and 0 <= grid_y < agent.height:
                    if agent.map[grid_y][grid_x] != BLOCKTYPE.WALL:
                        # 이전 END 초기화
                            for y in range(agent.height):
                                for x in range(agent.width):
                                    if agent.map[y][x] == BLOCKTYPE.END:
                                        agent.SetBlockType(x, y, BLOCKTYPE.VOID)

                            agent.SetBlockType(grid_x, grid_y, BLOCKTYPE.END)
                            agent.SetTargetPosition(grid_x, grid_y)
                            path = agent.FindPath()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
