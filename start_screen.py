import pygame

class StartScreen:
    def __init__(self, screen, font):
        """
        시작화면 클래스
        :param screen: pygame 화면 Surface
        :param font: pygame Font 객체
        """
        self.screen = screen
        self.font = font
        # 제목 및 안내 텍스트 렌더링
        self.title_text = self.font.render("Survival game", True, (255, 255, 255))
        self.start_text = self.font.render("Press any key", True, (200, 200, 200))

    def draw(self):
        """
        시작화면을 그리는 함수
        """
        self.screen.fill((10, 10, 20))  # 어두운 배경
        screen_rect = self.screen.get_rect()
        # 제목 텍스트 중앙 위쪽에 표시
        self.screen.blit(
            self.title_text,
            self.title_text.get_rect(center=(screen_rect.centerx, screen_rect.centery - 50))
        )
        # 안내 텍스트 중앙 아래쪽에 표시
        self.screen.blit(
            self.start_text,
            self.start_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 30))
        )
        pygame.display.flip()  # 화면 갱신

    def wait_for_key(self):
        """
        아무 키나 누를 때까지 대기하는 함수
        창을 닫으면 False, 키나 마우스를 누르면 True 반환
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            pygame.time.delay(10)  # CPU 점유율 낮추기
        return True
