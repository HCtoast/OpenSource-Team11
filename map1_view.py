# === View_Map.py ===
import pygame
import pytmx

class View_Map:
    def __init__(self, map_file):
        # TMX 파일을 불러와 맵 데이터 초기화
        self.tmx_data = pytmx.load_pygame(map_file)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        self.map_width = self.tmx_data.width * self.tile_width
        self.map_height = self.tmx_data.height * self.tile_height

        # 전체 맵을 담을 surface 생성
        self.map_surface = pygame.Surface((self.map_width, self.map_height))
        self._draw_full_map()  # 전체 맵을 한 번에 그림

    def _draw_full_map(self):
        # 모든 레이어의 타일들을 map_surface에 그림
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.map_surface.blit(tile, (x * self.tile_width, y * self.tile_height))

    def draw_zoomed(self, screen, camera_x, camera_y, screen_width, screen_height, zoom):
        # 카메라 뷰 영역 정의 (줌 적용)
        view_rect = pygame.Rect(camera_x, camera_y, screen_width / zoom, screen_height / zoom)
        # 해당 영역만 잘라서 확대
        sub_surface = self.map_surface.subsurface(view_rect)
        scaled_surface = pygame.transform.scale(sub_surface, (screen_width, screen_height))
        # 화면에 출력
        screen.blit(scaled_surface, (0, 0))
    
        
