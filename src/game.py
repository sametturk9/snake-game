import pygame
import random
from user_manager import UserManager

CELL = 20
BG1 = (30, 30, 30)
BG2 = (50, 50, 50)
UI_HEIGHT = 50

class Game:
    def __init__(self, width=640, height=480):
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.width = width
        self.height = height + UI_HEIGHT
        self.user_manager = UserManager()
        self.screen_state = "menu"
        self.input_field = ""
        self.input_label = ""
        self.input_type = None
        self.message = ""
        self.message_timer = 0
        self.prev_high_score = 0
        self.confetti = []
        self.confetti_timer = 0
        self.sound_enabled = True
        self.game_speed = 1.0
        self.base_speed = 10

        pygame.font.init()
        try:
            self.font = pygame.font.Font("C:/Windows/Fonts/Algerian.ttf", 28)
        except:
            self.font = pygame.font.Font(None, 28)

        self.snake = [
            (width // 2, height // 2 + UI_HEIGHT),
            (width // 2 - CELL, height // 2 + UI_HEIGHT),
            (width // 2 - 2 * CELL, height // 2 + UI_HEIGHT),
        ]
        self.direction = (1, 0)
        self.food = self._place_food()

    def _place_food(self):
        cols = self.width // CELL
        rows = (self.height - UI_HEIGHT) // CELL
        while True:
            x = random.randrange(cols) * CELL
            y = random.randrange(rows) * CELL + UI_HEIGHT
            if (x, y) not in self.snake:
                return (x, y)

    def spawn_confetti(self):
        for _ in range(50):
            self.confetti.append({
                'x': random.randint(0, self.width),
                'y': random.randint(-100, UI_HEIGHT),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(2, 5),
                'color': (random.randint(200, 255), random.randint(100, 255), random.randint(100, 255)),
                'size': random.randint(3, 8)
            })

    def draw_confetti(self, screen):
        if self.confetti_timer > 0:
            for c in self.confetti:
                c['x'] += c['vx']
                c['y'] += c['vy']
                c['vy'] += 0.1
                pygame.draw.circle(screen, c['color'], (int(c['x']), int(c['y'])), c['size'])
            self.confetti_timer -= 1
            self.confetti = [c for c in self.confetti if c['y'] < self.height]

    def reset(self):
        self.score = 0
        self.game_over = False
        self.prev_high_score = self.user_manager.get_high_score() if self.user_manager.current_user else 0
        self.confetti = []
        self.confetti_timer = 0
        game_height = self.height - UI_HEIGHT
        self.snake = [
            (self.width // 2, game_height // 2 + UI_HEIGHT),
            (self.width // 2 - CELL, game_height // 2 + UI_HEIGHT),
            (self.width // 2 - 2 * CELL, game_height // 2 + UI_HEIGHT),
        ]
        self.direction = (1, 0)
        self.food = self._place_food()

    def update(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_x = (head_x + dx * CELL) % self.width
        new_y = (head_y + dy * CELL)
        
        if new_y < UI_HEIGHT:
            new_y = UI_HEIGHT
        if new_y >= self.height:
            new_y = self.height - CELL
        new_head = (new_x, new_y)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()

    def check_game_over(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            self.game_over = True
            if self.user_manager.current_user:
                self.user_manager.add_score(self.score)
        
        is_new_high = False
        if self.user_manager.current_user and self.score > self.prev_high_score:
            self.prev_high_score = self.score
            is_new_high = True
        
        if self.game_over and is_new_high:
            self.confetti_timer = 120
            self.spawn_confetti()

    def draw(self, screen):
        screen.fill((20, 20, 30), (0, 0, self.width, UI_HEIGHT))
        
        pygame.draw.line(screen, (100, 100, 100), (0, UI_HEIGHT), (self.width, UI_HEIGHT), 2)
        
        score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 12))
        
        if self.user_manager.current_user and self.user_manager.current_user in self.user_manager.users:
            user_data = self.user_manager.users[self.user_manager.current_user]
            user_text = self.font.render(f"PLAYER: {user_data.get('username', 'Unknown')}", True, (100, 200, 255))
            screen.blit(user_text, (200, 12))
            
            high_score = self.user_manager.get_high_score()
            high_text = self.font.render(f"BEST: {high_score}", True, (255, 215, 0))
            screen.blit(high_text, (450, 12))

        for gx in range(0, self.width, CELL):
            for gy in range(UI_HEIGHT, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))

        for i, segment in enumerate(self.snake):
            col = (0, 255, 0) if i else (0, 200, 0)
            rect = pygame.Rect(segment[0], segment[1], CELL, CELL)
            pygame.draw.rect(screen, col, rect)

        fx, fy = self.food
        pygame.draw.rect(screen, (255, 60, 60),
                         pygame.Rect(fx, fy, CELL, CELL))

    def draw_menu(self, screen):
        for gx in range(0, self.width, CELL):
            for gy in range(0, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pulse = (pygame.time.get_ticks() % 2000) / 2000
        glow_intensity = int(50 + pulse * 30)
        
        title_surf = self.font.render("SNAKE", True, (0, 255, 100))
        title_rect = title_surf.get_rect(center=(self.width // 2, 80))
        
        glow_surf = self.font.render("SNAKE", True, (0, glow_intensity, glow_intensity // 2))
        glow_rect = glow_surf.get_rect(center=(self.width // 2, 80))
        for _ in range(3):
            screen.blit(glow_surf, (glow_rect.x - 2, glow_rect.y))
            screen.blit(glow_surf, (glow_rect.x + 2, glow_rect.y))
            screen.blit(glow_surf, (glow_rect.x, glow_rect.y - 2))
            screen.blit(glow_surf, (glow_rect.x, glow_rect.y + 2))
        screen.blit(title_surf, title_rect)
        
        card_x = self.width // 2 - 150
        card_y = 130
        card_w = 300
        
        pygame.draw.rect(screen, (40, 40, 60), (card_x, card_y, card_w, 320), border_radius=15)
        pygame.draw.rect(screen, (0, 255, 150), (card_x, card_y, card_w, 320), 2, border_radius=15)
        
        menu_y = card_y + 30
        font = pygame.font.Font(None, 32)
        
        if self.user_manager.current_user:
            user_data = self.user_manager.users[self.user_manager.current_user]
            user_text = font.render(f"Welcome, {user_data['username']}!", True, (100, 220, 255))
            user_rect = user_text.get_rect(center=(self.width // 2, menu_y))
            screen.blit(user_text, user_rect)
            
            menu_y += 50
            high_score = self.user_manager.get_high_score()
            if high_score > 0:
                hs_text = font.render(f"Best Score: {high_score}", True, (255, 215, 0))
                hs_rect = hs_text.get_rect(center=(self.width // 2, menu_y))
                screen.blit(hs_text, hs_rect)
                menu_y += 40
            
            pygame.draw.line(screen, (100, 100, 120), (card_x + 20, menu_y), (card_x + card_w - 20, menu_y), 1)
            menu_y += 20
            
            play_text = font.render("[ SPACE ] PLAY", True, (0, 255, 120))
            play_rect = play_text.get_rect(center=(self.width // 2, menu_y))
            screen.blit(play_text, play_rect)
            
            logout_text = pygame.font.Font(None, 20).render("[ L ] Logout", True, (180, 180, 180))
            logout_rect = logout_text.get_rect(center=(self.width // 2, menu_y + 35))
            screen.blit(logout_text, logout_rect)
            
            settings_text = pygame.font.Font(None, 18).render("[ O ] Settings", True, (150, 150, 180))
            settings_rect = settings_text.get_rect(center=(self.width // 2, menu_y + 65))
            screen.blit(settings_text, settings_rect)
            
            exit_text = pygame.font.Font(None, 18).render("[ X ] Exit", True, (200, 100, 100))
            exit_rect = exit_text.get_rect(center=(self.width // 2, menu_y + 90))
            screen.blit(exit_text, exit_rect)
        else:
            login_text = font.render("[ L ] Login", True, (100, 200, 255))
            login_rect = login_text.get_rect(center=(self.width // 2, menu_y))
            screen.blit(login_text, login_rect)
            
            register_text = font.render("[ R ] Register", True, (255, 180, 100))
            register_rect = register_text.get_rect(center=(self.width // 2, menu_y + 45))
            screen.blit(register_text, register_rect)
            
            settings_text = pygame.font.Font(None, 18).render("[ O ] Settings", True, (150, 150, 180))
            settings_rect = settings_text.get_rect(center=(self.width // 2, menu_y + 85))
            screen.blit(settings_text, settings_rect)
            
            exit_text = pygame.font.Font(None, 18).render("[ X ] Exit", True, (200, 100, 100))
            exit_rect = exit_text.get_rect(center=(self.width // 2, menu_y + 110))
            screen.blit(exit_text, exit_rect)
        
        global_scores = self.user_manager.get_global_high_scores()
        if global_scores:
            leader_x = self.width // 2 - 120
            leader_y = 420
            
            pygame.draw.rect(screen, (30, 30, 50), (leader_x - 10, leader_y - 10, 240, 30 + len(global_scores[:5]) * 25 + 10), border_radius=10)
            
            label_font = pygame.font.Font(None, 26)
            label = label_font.render("LEADERBOARD", True, (255, 215, 0))
            screen.blit(label, (leader_x, leader_y))
            leader_y += 30
            
            for i, entry in enumerate(global_scores[:5]):
                color = (255, 255, 255) if i > 0 else (255, 215, 0)
                score_text = pygame.font.Font(None, 22).render(
                    f"{i+1}. {entry['username']:<10} {entry['high_score']}", True, color
                )
                screen.blit(score_text, (leader_x, leader_y))
                leader_y += 25
        
        controls_y = self.height - 40
        controls_font = pygame.font.Font(None, 18)
        controls = controls_font.render("[O] Settings  [X] Exit  |  Arrow Keys: Move  |  SPACE: Play", True, (120, 120, 120))
        controls_rect = controls.get_rect(center=(self.width // 2, controls_y))
        screen.blit(controls, controls_rect)

        if self.message:
            if self.message_timer > 0:
                msg_font = pygame.font.Font(None, 28)
                msg_text = msg_font.render(self.message, True, (255, 100, 100))
                msg_rect = msg_text.get_rect(center=(self.width // 2, self.height - 50))
                screen.blit(msg_text, msg_rect)
                self.message_timer -= 1
            else:
                self.message = ""

    def draw_login(self, screen):
        for gx in range(0, self.width, CELL):
            for gy in range(0, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        card_x = self.width // 2 - 160
        card_y = 120
        pygame.draw.rect(screen, (30, 40, 60), (card_x, card_y, 320, 250), border_radius=20)
        pygame.draw.rect(screen, (0, 200, 150), (card_x, card_y, 320, 250), 2, border_radius=20)
        
        font = pygame.font.Font(None, 52)
        title = font.render("LOGIN", True, (0, 255, 150))
        title_rect = title.get_rect(center=(self.width // 2, card_y + 40))
        screen.blit(title, title_rect)
        
        input_font = pygame.font.Font(None, 36)
        label = input_font.render(self.input_label, True, (180, 180, 200))
        label_rect = label.get_rect(center=(self.width // 2, card_y + 100))
        screen.blit(label, label_rect)
        
        pygame.draw.rect(screen, (50, 60, 80), (card_x + 30, card_y + 130, 260, 45), border_radius=10)
        pygame.draw.rect(screen, (100, 200, 150), (card_x + 30, card_y + 130, 260, 45), 2, border_radius=10)
        
        input_text = input_font.render(self.input_field + "_", True, (255, 255, 255))
        input_rect = input_text.get_rect(center=(self.width // 2, card_y + 155))
        screen.blit(input_text, input_rect)
        
        prompt_font = pygame.font.Font(None, 22)
        prompt = prompt_font.render("[ ENTER ] Confirm", True, (100, 255, 150))
        prompt_rect = prompt.get_rect(center=(self.width // 2, card_y + 210))
        screen.blit(prompt, prompt_rect)
        
        back = prompt_font.render("[ ESC ] Back to Menu", True, (150, 150, 180))
        back_rect = back.get_rect(center=(self.width // 2, card_y + 240))
        screen.blit(back, back_rect)

    def draw_register(self, screen):
        for gx in range(0, self.width, CELL):
            for gy in range(0, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        card_x = self.width // 2 - 160
        card_y = 120
        pygame.draw.rect(screen, (30, 40, 60), (card_x, card_y, 320, 250), border_radius=20)
        pygame.draw.rect(screen, (255, 180, 100), (card_x, card_y, 320, 250), 2, border_radius=20)
        
        font = pygame.font.Font(None, 52)
        title = font.render("REGISTER", True, (255, 200, 100))
        title_rect = title.get_rect(center=(self.width // 2, card_y + 40))
        screen.blit(title, title_rect)
        
        input_font = pygame.font.Font(None, 36)
        label = input_font.render(self.input_label, True, (180, 180, 200))
        label_rect = label.get_rect(center=(self.width // 2, card_y + 100))
        screen.blit(label, label_rect)
        
        pygame.draw.rect(screen, (50, 60, 80), (card_x + 30, card_y + 130, 260, 45), border_radius=10)
        pygame.draw.rect(screen, (255, 200, 100), (card_x + 30, card_y + 130, 260, 45), 2, border_radius=10)
        
        input_text = input_font.render(self.input_field + "_", True, (255, 255, 255))
        input_rect = input_text.get_rect(center=(self.width // 2, card_y + 155))
        screen.blit(input_text, input_rect)
        
        prompt_font = pygame.font.Font(None, 22)
        prompt = prompt_font.render("[ ENTER ] Confirm", True, (255, 200, 100))
        prompt_rect = prompt.get_rect(center=(self.width // 2, card_y + 210))
        screen.blit(prompt, prompt_rect)
        
        back = prompt_font.render("[ ESC ] Back to Menu", True, (150, 150, 180))
        back_rect = back.get_rect(center=(self.width // 2, card_y + 240))
        screen.blit(back, back_rect)

    def draw_settings(self, screen):
        for gx in range(0, self.width, CELL):
            for gy in range(0, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        card_x = self.width // 2 - 180
        card_y = 100
        card_w = 360
        card_h = 320
        pygame.draw.rect(screen, (30, 40, 60), (card_x, card_y, card_w, card_h), border_radius=20)
        pygame.draw.rect(screen, (100, 150, 200), (card_x, card_y, card_w, card_h), 2, border_radius=20)
        
        font = pygame.font.Font(None, 48)
        title = font.render("SETTINGS", True, (100, 180, 255))
        title_rect = title.get_rect(center=(self.width // 2, card_y + 40))
        screen.blit(title, title_rect)
        
        y_pos = card_y + 100
        item_font = pygame.font.Font(None, 28)
        
        self.settings_sound_btn = pygame.Rect(card_x + 180, y_pos - 5, 80, 35)
        pygame.draw.rect(screen, (60, 60, 80), self.settings_sound_btn, border_radius=8)
        pygame.draw.rect(screen, (100, 255, 100) if self.sound_enabled else (255, 100, 100), self.settings_sound_btn, 2, border_radius=8)
        
        sound_label = item_font.render("Sound:", True, (200, 200, 200))
        screen.blit(sound_label, (card_x + 30, y_pos))
        
        sound_status = "ON" if self.sound_enabled else "OFF"
        sound_color = (100, 255, 100) if self.sound_enabled else (255, 100, 100)
        sound_text = item_font.render(sound_status, True, sound_color)
        screen.blit(sound_text, (card_x + 200, y_pos))
        
        y_pos += 60
        speed_label = item_font.render("Game Speed:", True, (200, 200, 200))
        screen.blit(speed_label, (card_x + 30, y_pos))
        
        y_pos += 40
        self.speed_buttons = []
        speed_font = pygame.font.Font(None, 24)
        
        for i, (speed, label) in enumerate([(0.5, "0.5x"), (1.0, "1x"), (2.0, "2x")]):
            btn_rect = pygame.Rect(card_x + 50 + i * 100, y_pos, 80, 35)
            self.speed_buttons.append((btn_rect, speed))
            
            color = (0, 255, 150) if self.game_speed == speed else (80, 80, 100)
            border_color = (0, 255, 150) if self.game_speed == speed else (150, 150, 150)
            pygame.draw.rect(screen, color, btn_rect, border_radius=8)
            pygame.draw.rect(screen, border_color, btn_rect, 2, border_radius=8)
            
            btn_text = speed_font.render(label, True, (255, 255, 255))
            screen.blit(btn_text, (btn_rect.x + 20, btn_rect.y + 7))
        
        prompt_font = pygame.font.Font(None, 22)
        back = prompt_font.render("[ ESC ] Back to Menu", True, (150, 150, 180))
        back_rect = back.get_rect(center=(self.width // 2, card_y + card_h - 30))
        screen.blit(back, back_rect)

    def draw_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        card_x = self.width // 2 - 180
        card_y = self.height // 2 - 100
        pygame.draw.rect(screen, (30, 30, 50), (card_x, card_y, 360, 230), border_radius=20)
        pygame.draw.rect(screen, (255, 80, 80), (card_x, card_y, 360, 230), 3, border_radius=20)

        title_font = pygame.font.Font(None, 56)
        title = title_font.render("GAME OVER", True, (255, 80, 80))
        title_rect = title.get_rect(center=(self.width // 2, card_y + 40))
        screen.blit(title, title_rect)

        font = pygame.font.Font(None, 42)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 2, card_y + 95))
        screen.blit(score_text, score_rect)

        if self.user_manager.current_user:
            high_score = self.user_manager.get_high_score()
            hs_text = font.render(f"Best: {high_score}", True, (255, 215, 0))
            high_rect = hs_text.get_rect(center=(self.width // 2, card_y + 135))
            screen.blit(hs_text, high_rect)

        prompt_font = pygame.font.Font(None, 26)
        restart_text = prompt_font.render("[ SPACE ] Play Again", True, (0, 255, 120))
        restart_rect = restart_text.get_rect(center=(self.width // 2, card_y + 180))
        screen.blit(restart_text, restart_rect)

        menu_text = prompt_font.render("[ ESC ] Main Menu", True, (180, 180, 200))
        menu_rect = menu_text.get_rect(center=(self.width // 2, card_y + 210))
        screen.blit(menu_text, menu_rect)

        self.draw_confetti(screen)

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
                    if self.screen_state in ["login", "register"]:
                        if event.key == pygame.K_ESCAPE:
                            self.screen_state = "menu"
                            self.input_field = ""
                            self.input_label = ""
                        elif event.key == pygame.K_RETURN:
                            if self.screen_state == "login":
                                success, msg = self.user_manager.login(self.input_field)
                                if success:
                                    self.screen_state = "menu"
                                    self.message = f"Welcome {msg}!"
                                    self.message_timer = 120
                                else:
                                    self.message = msg
                                    self.message_timer = 120
                                self.input_field = ""
                            elif self.screen_state == "register":
                                success, msg = self.user_manager.register(self.input_field)
                                if success:
                                    self.user_manager.current_user = msg.lower()
                                    self.screen_state = "menu"
                                    self.message = f"Welcome {msg}!"
                                    self.message_timer = 120
                                else:
                                    self.message = msg
                                    self.message_timer = 120
                                self.input_field = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_field = self.input_field[:-1]
                        elif event.unicode.isprintable() and len(self.input_field) < 20:
                            if event.unicode.isalnum() or event.unicode in "_-":
                                self.input_field += event.unicode
                    elif self.screen_state == "settings":
                        if event.key == pygame.K_ESCAPE:
                            self.screen_state = "menu"
                        elif event.key == pygame.K_1:
                            self.game_speed = 0.5
                        elif event.key == pygame.K_2:
                            self.game_speed = 1.0
                        elif event.key == pygame.K_3:
                            self.game_speed = 2.0
                        elif event.key == pygame.K_s:
                            self.sound_enabled = not self.sound_enabled
                    elif self.screen_state == "menu":
                        if event.key == pygame.K_ESCAPE:
                            pass
                        elif event.key == pygame.K_SPACE:
                            if self.user_manager.current_user:
                                self.start_screen = False
                        elif event.key == pygame.K_l:
                            if not self.user_manager.current_user:
                                self.screen_state = "login"
                                self.input_label = "Enter Username:"
                                self.input_field = ""
                            else:
                                self.user_manager.logout()
                        elif event.key == pygame.K_r:
                            if not self.user_manager.current_user:
                                self.screen_state = "register"
                                self.input_label = "Enter Username:"
                                self.input_field = ""
                        elif event.key == pygame.K_o:
                            self.screen_state = "settings"
                        elif event.key == pygame.K_x:
                            pygame.quit()
                            return

            if self.screen_state == "menu":
                self.draw_menu(screen)
            elif self.screen_state == "login":
                self.draw_login(screen)
            elif self.screen_state == "register":
                self.draw_register(screen)
            elif self.screen_state == "settings":
                self.draw_settings(screen)

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.screen_state == "settings":
                        mouse_pos = event.pos
                        if hasattr(self, 'speed_buttons'):
                            for btn_rect, speed in self.speed_buttons:
                                if btn_rect.collidepoint(mouse_pos):
                                    self.game_speed = speed
                        if hasattr(self, 'settings_sound_btn'):
                            if self.settings_sound_btn.collidepoint(mouse_pos):
                                self.sound_enabled = not self.sound_enabled

            clock.tick(30)

        while not self.game_over:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
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
                actual_speed = int(self.base_speed * self.game_speed)
                clock.tick(actual_speed)
            except Exception as e:
                print(f"Hata: {e}")
                import traceback
                traceback.print_exc()
                break

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.score = 0
                        self.game_over = False
                        game_height = self.height - UI_HEIGHT
                        self.snake = [
                            (self.width // 2, game_height // 2 + UI_HEIGHT),
                            (self.width // 2 - CELL, game_height // 2 + UI_HEIGHT),
                            (self.width // 2 - 2 * CELL, game_height // 2 + UI_HEIGHT),
                        ]
                        self.direction = (1, 0)
                        self.food = self._place_food()
                        self.prev_high_score = self.user_manager.get_high_score() if self.user_manager.current_user else 0
                        self.confetti = []
                        self.confetti_timer = 0
                        break
                    elif event.key == pygame.K_ESCAPE:
                        self.score = 0
                        self.game_over = False
                        self.start_screen = True
                        self.screen_state = "menu"
                        game_height = self.height - UI_HEIGHT
                        self.snake = [
                            (self.width // 2, game_height // 2 + UI_HEIGHT),
                            (self.width // 2 - CELL, game_height // 2 + UI_HEIGHT),
                            (self.width // 2 - 2 * CELL, game_height // 2 + UI_HEIGHT),
                        ]
                        self.direction = (1, 0)
                        self.food = self._place_food()
                        break
            
            if not self.game_over:
                break
            
            self.draw(screen)
            self.draw_game_over(screen)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()