import pygame
import random                     # <<– ekle

CELL = 20              # kare boyutu
BG1 = (30, 30, 30)     # zemin renkleri
BG2 = (50, 50, 50)

class Game:
    def __init__(self, width=640, height=480):
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.width = width
        self.height = height

        self.snake = [
            (width // 2, height // 2),
            (width // 2 - CELL, height // 2),
            (width // 2 - 2 * CELL, height // 2),
        ]
        self.direction = (1, 0)

        self.food = self._place_food()

    def _place_food(self):
        """Ekranın hücrelerinden rastgele bir yer seç.
           Yılanın içine yerleşmemesine dikkat et."""
        cols = self.width // CELL
        rows = self.height // CELL
        while True:
            x = random.randrange(cols) * CELL
            y = random.randrange(rows) * CELL
            if (x, y) not in self.snake:
                return (x, y)

    def reset(self):
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.snake = [
            (self.width // 2, self.height // 2),
            (self.width // 2 - CELL, self.height // 2),
            (self.width // 2 - 2 * CELL, self.height // 2),
        ]
        self.direction = (1, 0)
        self.food = self._place_food()

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        # sınırları mod alarak sarma (wrap‑around) işlemi
        new_x = (head_x + dx * CELL) % self.width
        new_y = (head_y + dy * CELL) % self.height
        new_head = (new_x, new_y)

        self.snake.insert(0, new_head)

        if new_head == self.food:          # yem yenirse
            self.score += 1
            self.food = self._place_food() # yeni yem üret
            # kuyruğu çıkarmıyoruz → yılan uzar
        else:
            self.snake.pop()

    def check_game_over(self):
        """Kafa yılanın geri kalanıyla çakıştı mı diye bak."""
        head = self.snake[0]
        if head in self.snake[1:]:
            self.game_over = True

    def draw(self, screen):
        # basit bir kareli/uzay-salonu tarzı zemin
        for gx in range(0, self.width, CELL):
            for gy in range(0, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))

        # eğer resim kullanacaksanız üstteki döngüyü kaldırıp
        # screen.blit(self.background, (0, 0))

        # yılan
        for i, segment in enumerate(self.snake):
            # kafayı farklı renkle de boyayabilirsiniz
            col = (0, 255, 0) if i else (0, 200, 0)
            rect = pygame.Rect(segment[0], segment[1], CELL, CELL)
            pygame.draw.rect(screen, col, rect)

        # yem
        fx, fy = self.food
        pygame.draw.rect(screen, (255, 60, 60),
                         pygame.Rect(fx, fy, CELL, CELL))

        # skor
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (240, 240, 240))
        screen.blit(text, (5, 5))


    def draw_start_screen(self, screen):
        screen.fill((20, 20, 30))
        
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("SNAKE", True, (0, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 60))
        screen.blit(title, title_rect)
        
        subtitle_font = pygame.font.Font(None, 36)
        subtitle = subtitle_font.render("Press SPACE to Start", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.height // 2 + 20))
        screen.blit(subtitle, subtitle_rect)
        
        controls_font = pygame.font.Font(None, 24)
        controls = controls_font.render("Use Arrow Keys to Move", True, (120, 120, 120))
        controls_rect = controls.get_rect(center=(self.width // 2, self.height // 2 + 80))
        screen.blit(controls, controls_rect)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()

        while self.start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_screen = False
            
            self.draw_start_screen(screen)
            pygame.display.flip()
            clock.tick(30)

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)

            self.update()
            self.check_game_over()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()