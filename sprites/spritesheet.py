import pygame

class SpriteSheet:
    """
    스프라이트시트 이미지를 처리하는 클래스
    - image_path: 스프라이트시트 파일 경로 (128x384 크기)
    - frame_width: 개별 프레임 너비 (32픽셀)
    - frame_height: 개별 프레임 높이 (32픽셀)
    """
    def __init__(self, image_path, frame_width=32, frame_height=32):
        # 투명도 처리를 위해 convert_alpha() 사용
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # 스프라이트시트 크기 정보
        self.sheet_width = self.sheet.get_width()   # 128
        self.sheet_height = self.sheet.get_height() # 384
        
        # 가로/세로 프레임 수 계산
        self.frames_per_row = self.sheet_width // frame_width    # 4개
        self.total_rows = self.sheet_height // frame_height      # 12행
        
        print(f"스프라이트시트 로드: {image_path}")
        print(f"전체 크기: {self.sheet_width}x{self.sheet_height}")
        print(f"프레임 크기: {frame_width}x{frame_height}")
        print(f"프레임 배치: {self.frames_per_row}열 x {self.total_rows}행")

    def get_frame(self, col, row):
        """
        특정 위치의 프레임 추출
        - col: 열 인덱스 (0-3)
        - row: 행 인덱스 (0-11)
        """
        # 범위 체크
        if col >= self.frames_per_row or row >= self.total_rows:
            print(f"경고: 프레임 인덱스가 범위를 벗어남 ({col}, {row})")
            return None
            
        frame_rect = pygame.Rect(
            col * self.frame_width,    # X 좌표
            row * self.frame_height,   # Y 좌표
            self.frame_width,
            self.frame_height
        )
        
        # 투명도 유지를 위한 SRCALPHA 표면 생성
        frame = pygame.Surface(frame_rect.size, pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), frame_rect)
        return frame
    
    def get_animation_frames(self, row, frame_count=4):
        """
        특정 행의 애니메이션 프레임들을 추출
        - row: 애니메이션이 있는 행 번호
        - frame_count: 추출할 프레임 수 (기본값: 4)
        """
        frames = []
        for col in range(min(frame_count, self.frames_per_row)):
            frame = self.get_frame(col, row)
            if frame:
                frames.append(frame)
        return frames
