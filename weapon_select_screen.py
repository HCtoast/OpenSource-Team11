import pygame
import os

class WeaponSelectScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.title_font = pygame.font.Font(None, 60)  # 제목용 글씨
        self.sub_font = pygame.font.Font(None, 44)  # 소제목용 글씨
        self.weapon_names = ["Bullet Gun", "Laser", "Cross Gun", "Garlic", "Bomb"]
        self.selected = set()
        self.current_index = 0
        self.max_select = 3
        self.weapon_images = self.load_weapon_images()
        self.background = pygame.image.load("assets//images//Weapon_Select_Background.png").convert()
        self.background = pygame.transform.scale(self.background, (800,600))


    def load_weapon_images(self):
        images = {}
        base_path = os.path.join("assets", "images", "weapons")
        for name in self.weapon_names:
            path = os.path.join(base_path, f"{name}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                images[name] = pygame.transform.scale(img, (64, 64))  # 크기 조정
        return images

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        #self.screen.fill((10, 10, 10))
        title = self.title_font.render("Select 3 Weapons", True, (255, 230, 100))  # 노란 계열
        self.screen.blit(title, ((self.screen.get_width() - title.get_width()) // 2, 30))

        spacing = 75
        start_y = 100
        center_x = self.screen.get_width() // 2

        for i, name in enumerate(self.weapon_names):
            y = start_y + i * spacing

            # 배경 박스
            bg_color = (0, 150, 0) if name in self.selected else (80, 80, 80)
            if i == self.current_index:
                pygame.draw.rect(self.screen, (200, 200, 50), (center_x - 200, y - 10, 400, 80), 3)

            pygame.draw.rect(self.screen, bg_color, (center_x - 180, y, 360, 60))

            # 이미지
            if name in self.weapon_images:
                self.screen.blit(self.weapon_images[name], (center_x - 170, y))

            # 이름
            label = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(label, (center_x - 80, y + 15))

        # 선택 상태 표시
        info = self.sub_font.render(f"{len(self.selected)}/3 selected", True, (255, 100, 100))
        self.screen.blit(info, (center_x - info.get_width() // 2, 500))
        
        
        # 안내문 추가
        if len(self.selected) == self.max_select:
            prompt = self.sub_font.render("Press Enter to start!", True, (100, 255, 100))
            self.screen.blit(prompt, (center_x - prompt.get_width() // 2, 550))

        pygame.display.flip()

    def select(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_index = (self.current_index - 1) % len(self.weapon_names)
                    elif event.key == pygame.K_w:
                        self.current_index = (self.current_index - 1) % len(self.weapon_names)
                    elif event.key == pygame.K_DOWN:
                        self.current_index = (self.current_index + 1) % len(self.weapon_names)
                    elif event.key == pygame.K_s:
                        self.current_index = (self.current_index + 1) % len(self.weapon_names)
                    elif event.key == pygame.K_SPACE:
                        selected_name = self.weapon_names[self.current_index]
                        if selected_name in self.selected:
                            self.selected.remove(selected_name)
                        elif len(self.selected) < self.max_select:
                            self.selected.add(selected_name)
                    elif event.key == pygame.K_RETURN:
                        if len(self.selected) == self.max_select:
                            running = False

            clock.tick(60)

        return list(self.selected)
