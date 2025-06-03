import math, heapq
from enum import IntEnum

class BLOCKTYPE(IntEnum):
    VOID = 0
    WALL = 1
    BEGIN = 2
    END = 3

'''
# 원래 일직선으로 다가오는 추격방식이랑 A* 추격방식 모두 사용할까 고민이 되어서 일단 주석 처리 했습니다.
class AGENTMODE(IntEnum):
    NONE = 0
    ASTAR = 1
'''

class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

class Cell: # 백트래킹을 위한 하나의 단위 노드
    def __init__(self):
        self.parent_x = -1
        self.parent_y = -1
        self.f = float('inf')
        self.g = float('inf')
        self.h = float('inf')

class NavMeshAgent:
    """
    적추격 알고리즘 클래스
    - x_cell_size: 픽셀 가로 크기
    - y_cell_size: 픽셀 세로 크기
    - map_size_width: 맵 전체 가로 길이(그냥 화면 크기랑 동일)
    - map_size_height: 맵 전체 세로 길이(그냥 화면 크기랑 동일)
    - x_cell_size: 픽셀 가로 크기
    - y_cell_size: 픽셀 세로 크기
    """
    dx1 = [0, 0, 1, -1]
    dy1 = [-1, 1, 0, 0]
    dx2 = [1, -1, -1, 1]
    dy2 = [-1, 1, -1, 1]

    def __init__(self, x_cell_size, y_cell_size, map_size_width, map_size_height):
        self.x_cell_size = x_cell_size
        self.y_cell_size = y_cell_size
        self.map_size_width = map_size_width
        self.map_size_height = map_size_height

        self.width = int(map_size_width / x_cell_size)
        self.height = int(map_size_height / y_cell_size)
        self.map = [[BLOCKTYPE.VOID for _ in range(self.width)] for _ in range(self.height)]

    # 기능 추가중...
    def SetOption(self, stp_distance, trc_velocity, agent_mode): # public
        """
        A* AI 기타 옵션
        - stp_distance: 타겟으로 부터 몇 블럭까지만을 계산할 것인지 (Unity에도 있는 기능이라서 넣을 생각입니다.)
        - trc_velocity: AI 추격 속력
        - agent_mode: Agent가 추격하는 방식
        """
        self.stp_distance = stp_distance
        self.trc_velocity = trc_velocity
        self.agent_mode = agent_mode

    def SetTargetPosition(self, x, y): # public
        """
        타겟 위치 설정 함수
        ####### 주의 사항(매우 중요함)#######
        -> 이때 xy값은 화면좌표계(절대좌표)가 아니라 블럭인덱스 번호입니다.
        -> 즉, (0, 1)인덱스 블럭, (15, 6) 이런식 입니다.
        """
        self.dst = Vector2D(x, y)

    def SetPosition(self, x, y): # public
        """
        시작 위치 설정 함수
        ####### 주의 사항(매우 중요함)#######
        -> 이때 xy값은 화면좌표계(절대좌표)가 아니라 블럭인덱스 번호입니다.
        -> 즉, (0, 1)인덱스 블럭, (15, 6) 이런식 입니다.
        """
        self.src = Vector2D(x, y)

    def SetBlockType(self, x, y, block_type): # public
        """
        블럭 타입 정하는 함수
        - block_type: 벽을 설치할 것인지, 도착지점, 출발지점을 설정할 것인지를 정한다.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map[y][x] = block_type

    def IsInRange(self, y, x): # private
        return 0 <= y < self.height and 0 <= x < self.width

    def IsUnBlocked(self, y, x): # private
        return self.map[y][x] == BLOCKTYPE.VOID

    def IsDestination(self, y, x): # private
        return y == self.dst.y and x == self.dst.x

    def Heuristic(self, y, x): # private
        return math.sqrt((y - self.dst.y) ** 2 + (x - self.dst.x) ** 2)

    def FindPath(self):  # public # 백트랙킹 알고리즘 ..
        """
        A* 알고리즘 함수
        """
        cell_details = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        closed_list = [[False for _ in range(self.width)] for _ in range(self.height)]

        sy, sx = self.src.y, self.src.x
        dy, dx = self.dst.y, self.dst.x

        cell_details[sy][sx].f = cell_details[sy][sx].g = cell_details[sy][sx].h = 0.0
        cell_details[sy][sx].parent_x = sx
        cell_details[sy][sx].parent_y = sy

        open_list = []
        heapq.heappush(open_list, (0.0, Vector2D(sx, sy)))

        while open_list:
            f_val, pos = heapq.heappop(open_list)
            x, y = pos.x, pos.y
            closed_list[y][x] = True

            for i in range(4):
                nx, ny = x + self.dx1[i], y + self.dy1[i]
                if self.IsInRange(ny, nx):
                    if self.IsDestination(ny, nx):
                        cell_details[ny][nx].parent_x = x
                        cell_details[ny][nx].parent_y = y
                        return self.TracePath(cell_details)

                    if not closed_list[ny][nx] and self.IsUnBlocked(ny, nx):
                        g_new = cell_details[y][x].g + 1.0
                        h_new = self.Heuristic(ny, nx)
                        f_new = g_new + h_new

                        if cell_details[ny][nx].f > f_new:
                            cell_details[ny][nx].f = f_new
                            cell_details[ny][nx].g = g_new
                            cell_details[ny][nx].h = h_new
                            cell_details[ny][nx].parent_x = x
                            cell_details[ny][nx].parent_y = y
                            heapq.heappush(open_list, (f_new, Vector2D(nx, ny)))
            '''
            for i in range(4):
                nx, ny = x + self.dx2[i], y + self.dy2[i]
                if self.IsInRange(ny, nx):
                    if self.IsDestination(ny, nx):
                        cell_details[ny][nx].parent_x = x
                        cell_details[ny][nx].parent_y = y
                        return self.TracePath(cell_details)

                    if not closed_list[ny][nx] and self.IsUnBlocked(ny, nx):
                        g_new = cell_details[y][x].g + 1.414
                        h_new = self.Heuristic(ny, nx)
                        f_new = g_new + h_new

                        if cell_details[ny][nx].f > f_new:
                            cell_details[ny][nx].f = f_new
                            cell_details[ny][nx].g = g_new
                            cell_details[ny][nx].h = h_new
                            cell_details[ny][nx].parent_x = x
                            cell_details[ny][nx].parent_y = y
                            heapq.heappush(open_list, (f_new, Vector2D(nx, ny)))
            '''
            
        return []

    def TracePath(self, cell_details): # public
        """
        최단 경로 계산 함수
        - cell_details: FindPath함수로 부터 계산된 최단경로 데이터셋을 기준으로 백트래킹기법을 사용하여 최단경로 역추적
        """
        path = []
        y, x = self.dst.y, self.dst.x
        while not (cell_details[y][x].parent_x == x and cell_details[y][x].parent_y == y):
            path.append((x, y))
            temp_x = cell_details[y][x].parent_x
            temp_y = cell_details[y][x].parent_y
            x, y = temp_x, temp_y
        path.append((x, y))
        path.reverse()
        
        return path
