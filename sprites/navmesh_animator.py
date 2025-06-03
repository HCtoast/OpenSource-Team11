from sprites.navmesh_agent import NavMeshAgent, BLOCKTYPE

class NavMeshAnimator:
    def __init__(self, cell_size, width, height):
        self.nav = NavMeshAgent(cell_size, cell_size, width, height)
        self.nav.SetOption(1, 1, 1)

        self.cell_size = cell_size
        self.cell_width = width // cell_size
        self.cell_height = height // cell_size
        self.absolute_pos = (0.0, 0.0)
        self.previous_target = None

        self.path = []
        self.current_idx = 0
        self.current_time = 0.0
        self.max_time = 0.3 ##### 적이 쫒아오는데 걸리는 시간
        self.is_stopped = True

        self.start = (0, 0)
        self.end = (0, 0)

    def Lerp(self, a, b, t):
        return (1.0 - t) * a + t * b

    def update(self, dt):
        if self.is_stopped or self.current_idx >= len(self.path) - 1:
            return self.absolute_pos

        self.current_time += dt

        current_cell = self.path[self.current_idx]
        next_cell = self.path[self.current_idx + 1]
        t = min(self.current_time / self.max_time, 1.0)

        c2 = self.cell_size * 0.5
        ax, ay = current_cell[0] * self.cell_size + c2, current_cell[1] * self.cell_size + c2
        bx, by = next_cell[0] * self.cell_size + c2, next_cell[1] * self.cell_size + c2

        x = self.Lerp(ax, bx, t)
        y = self.Lerp(ay, by, t)
        self.absolute_pos = (x, y)

        if t >= 1.0:
            self.current_idx += 1
            self.current_time = 0.0

            if self.current_idx >= len(self.path) - 1:
                self.is_stopped = True

        return self.absolute_pos

    def SetTargetPosition(self, target_x, target_y):
        my_x, my_y = self.absolute_pos

        self.nav.SetBlockType(*self.start, BLOCKTYPE.VOID)
        self.nav.SetBlockType(*self.end, BLOCKTYPE.VOID)
        
        self.start = (int(my_x // self.cell_size), int(my_y // self.cell_size))
        self.end = (int(target_x // self.cell_size), int(target_y // self.cell_size))

        if self.previous_target == self.end:
            return
        self.previous_target = self.end

        sx, sy = self.start
        ex, ey = self.end

        if not (0 <= sx < self.cell_width and 0 <= sy < self.cell_height):
            print("[오류] 시작 위치가 맵 범위를 벗어남")
            self.is_stopped = True
            return

        if not (0 <= ex < self.cell_width and 0 <= ey < self.cell_height):
            print("[오류] 도착 위치가 맵 범위를 벗어남")
            self.is_stopped = True
            return

        if self.nav.map[ey][ex] == BLOCKTYPE.WALL:
            print("[오류] 도착 위치는 벽입니다")
            self.is_stopped = True
            return

        self.nav.SetBlockType(*self.start, BLOCKTYPE.BEGIN)
        self.nav.SetBlockType(*self.end, BLOCKTYPE.END)

        self.nav.SetPosition(*self.start)
        self.nav.SetTargetPosition(*self.end)
        new_path = self.nav.FindPath()

        if new_path:
            self.path = new_path
            self.current_idx = 0
            self.current_time = 0.0
            self.is_stopped = False
        else:
            print("[경고] 경로를 찾을 수 없습니다")
            self.is_stopped = True

    def SetPosition(self, x: float, y: float):
        self.absolute_pos = (x, y)
