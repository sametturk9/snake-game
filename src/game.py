import pygame
import random
from user_manager import UserManager

CELL = 20
BG1 = (30, 30, 30)
BG2 = (50, 50, 50)

class Game:
    def __init__(self, width=640, height=480):
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.width = width
        self.height = height
        self.user_manager = UserManager()
        self.screen_state = "menu"
        self.input_field = ""
        self.input_label = ""
        self.input_type = None
        self.message = ""
        self.message_timer = 0

        self.snake = [
            (width // 2, height // 2),
            (width // 2 - CELL, height // 2),
            (width // 2 - 2 * CELL, height // 2),
        ]
        self.direction = (1, 0)
        self.food = self._place_food()

    def _place_food(self):
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
        self.screen_state = "menu"
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
        new_x = (head_x + dx * CELL) % self.width
        new_y = (head_y + dy * CELL) % self.height
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

    def draw(self, screen):
        for gx in range(0, self.width, CELL):
            for gy in range(0, self.height, CELL):
                color = BG1 if ((gx//CELL + gy//CELL) % 2 == 0) else BG2
                screen.fill(color, pygame.Rect(gx, gy, CELL, CELL))

        for i, segment in enumerate(self.snake):
            col = (0, 255, 0) if i else (0, 200, 0)
            rect = pygame.Rect(segment[0], segment[1], CELL, CELL)
            pygame.draw.rect(screen, col, rect)

        fx, fy = self.food
        pygame.draw.rect(screen, (255, 60, 60),
                         pygame.Rect(fx, fy, CELL, CELL))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (240, 240, 240))
        screen.blit(score_text, (5, 5))

        if self.user_manager.current_user and self.user_manager.current_user in self.user_manager.users:
            user_data = self.user_manager.users[self.user_manager.current_user]
            user_text = font.render(f"Player: {user_data.get('username', 'Unknown')}", True, (100, 200, 255))
            screen.blit(user_text, (5, 40))

            high_score = self.user_manager.get_high_score()
            high_text = font.render(f"High Score: {high_score}", True, (255, 215, 0))
            screen.blit(high_text, (self.width - 180, 5))

    def draw_menu(self, screen):
        screen.fill((20, 20, 30))
        
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("SNAKE", True, (0, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)

        menu_y = 160
        font = pygame.font.Font(None, 36)
        
        if self.user_manager.current_user:
            user_data = self.user_manager.users[self.user_manager.current_user]
            user_text = font.render(f"Welcome, {user_data['username']}!", True, (100, 200, 255))
            user_rect = user_text.get_rect(center=(self.width // 2, menu_y))
            screen.blit(user_text, user_rect)
            
            menu_y += 50
            scores = self.user_manager.get_scores()
            if scores:
                score_label = font.render("Your Scores:", True, (200, 200, 200))
                screen.blit(score_label, (self.width // 2 - 80, menu_y))
                menu_y += 40
                for i, s in enumerate(scores[:5]):
                    score_text = font.render(f"{i+1}. {s}", True, (255, 255, 255))
                    screen.blit(score_text, (self.width // 2 - 40, menu_y))
                    menu_y += 30
            
            menu_y += 20
            start_text = font.render("Press SPACE to Play", True, (0, 255, 100))
            screen.blit(start_text, (self.width // 2 - 120, menu_y))
            
            logout_text = pygame.font.Font(None, 24).render("Press L to Logout", True, (150, 150, 150))
            screen.blit(logout_text, (self.width // 2 - 90, menu_y + 40))
        else:
            login_text = font.render("Press L to Login", True, (200, 200, 200))
            screen.blit(login_text, (self.width // 2 - 100, menu_y))
            
            register_text = font.render("Press R to Register", True, (200, 200, 200))
            screen.blit(register_text, (self.width // 2 - 120, menu_y + 50))

        global_scores = self.user_manager.get_global_high_scores()
        if global_scores:
            y_pos = 400
            label_font = pygame.font.Font(None, 28)
            label = label_font.render("Top Players:", True, (255, 215, 0))
            screen.blit(label, (self.width // 2 - 60, y_pos))
            y_pos += 30
            for i, entry in enumerate(global_scores[:5]):
                score_text = pygame.font.Font(None, 24).render(
                    f"{i+1}. {entry['username']}: {entry['high_score']}", True, (200, 200, 200)
                )
                screen.blit(score_text, (self.width // 2 - 80, y_pos))
                y_pos += 25

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
        screen.fill((20, 20, 30))
        
        font = pygame.font.Font(None, 48)
        title = font.render("LOGIN", True, (0, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, 80))
        screen.blit(title, title_rect)
        
        input_font = pygame.font.Font(None, 36)
        label = input_font.render(self.input_label, True, (200, 200, 200))
        label_rect = label.get_rect(center=(self.width // 2, 160))
        screen.blit(label, label_rect)
        
        input_text = input_font.render(self.input_field + "_", True, (255, 255, 255))
        input_rect = input_text.get_rect(center=(self.width // 2, 220))
        screen.blit(input_text, input_rect)
        
        prompt_font = pygame.font.Font(None, 24)
        prompt = prompt_font.render("Press ENTER to confirm", True, (150, 150, 150))
        prompt_rect = prompt.get_rect(center=(self.width // 2, 300))
        screen.blit(prompt, prompt_rect)
        
        back = prompt_font.render("Press ESC to go back", True, (120, 120, 120))
        back_rect = back.get_rect(center=(self.width // 2, 340))
        screen.blit(back, back_rect)

    def draw_register(self, screen):
        screen.fill((20, 20, 30))
        
        font = pygame.font.Font(None, 48)
        title = font.render("REGISTER", True, (0, 255, 100))
        title_rect = title.get_rect(center=(self.width // 2, 60))
        screen.blit(title, title_rect)
        
        input_font = pygame.font.Font(None, 32)
        
        y_pos = 130
        label = input_font.render(self.input_label, True, (200, 200, 200))
        screen.blit(label, (self.width // 2 - 150, y_pos))
        
        input_text = input_font.render(self.input_field + "_", True, (255, 255, 255))
        screen.blit(input_text, (self.width // 2 - 100, y_pos + 35))
        
        prompt_font = pygame.font.Font(None, 24)
        prompt = prompt_font.render("Press ENTER to continue", True, (150, 150, 150))
        screen.blit(prompt, (self.width // 2 - 130, 300))
        
        back = prompt_font.render("Press ESC to go back", True, (120, 120, 120))
        screen.blit(back, (self.width // 2 - 110, 340))

    def draw_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(None, 72)
        title = title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 60))
        screen.blit(title, title_rect)

        font = pygame.font.Font(None, 48)
        score_text = font.render(f"Score: {self.score}", True, (240, 240, 240))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 2))
        screen.blit(score_text, score_rect)

        if self.user_manager.current_user:
            high_score = self.user_manager.get_high_score()
            high_text = font.render(f"Best: {high_score}", True, (255, 215, 0))
            high_rect = high_text.get_rect(center=(self.width // 2, self.height // 2 + 45))
            screen.blit(high_text, high_rect)

        prompt_font = pygame.font.Font(None, 32)
        restart_text = prompt_font.render("Press SPACE to Play Again", True, (0, 255, 100))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 100))
        screen.blit(restart_text, restart_rect)

        menu_text = prompt_font.render("Press ESC for Menu", True, (200, 200, 200))
        menu_rect = menu_text.get_rect(center=(self.width // 2, self.height // 2 + 140))
        screen.blit(menu_text, menu_rect)

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
                    if event.key == pygame.K_ESCAPE:
                        if self.screen_state in ["login", "register"]:
                            self.screen_state = "menu"
                            self.input_field = ""
                            self.input_label = ""
                    elif event.key == pygame.K_SPACE:
                        if self.screen_state == "menu" and self.user_manager.current_user:
                            self.start_screen = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_field = self.input_field[:-1]
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
                    elif event.key == pygame.K_l:
                        if self.screen_state == "menu":
                            if not self.user_manager.current_user:
                                self.screen_state = "login"
                                self.input_label = "Enter Username:"
                                self.input_field = ""
                            elif self.user_manager.current_user:
                                self.user_manager.logout()
                    elif event.key == pygame.K_r:
                        if self.screen_state == "menu" and not self.user_manager.current_user:
                            self.screen_state = "register"
                            self.input_label = "Enter Username:"
                            self.input_field = ""
                    else:
                        if self.screen_state in ["login", "register"]:
                            if event.unicode.isprintable() and len(self.input_field) < 20:
                                if event.unicode.isalnum() or event.unicode in "_-":
                                    self.input_field += event.unicode

            if self.screen_state == "menu":
                self.draw_menu(screen)
            elif self.screen_state == "login":
                self.draw_login(screen)
            elif self.screen_state == "register":
                self.draw_register(screen)

            pygame.display.flip()
            clock.tick(30)

        while not self.game_over:
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
            clock.tick(10)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                        self.start_screen = False
                        self.game_over = False
                        break
                    elif event.key == pygame.K_ESCAPE:
                        self.reset()
                        self.start_screen = True
                        self.screen_state = "menu"
                        self.game_over = False
                        break
            
            if not self.game_over:
                break
                
            self.draw(screen)
            self.draw_game_over(screen)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()