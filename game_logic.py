
# ====================
# game_logic.py
# ====================
import pygame
from collections import deque
from config import *
from car import Car
from ui_components import ParticleSystem, Button

class TollSimulator:
    """Main game logic for the toll simulator"""
    
    def __init__(self, width, height):
        self.window_width = width
        self.window_height = height
        self.queue = deque()
        self.last_spawn = pygame.time.get_ticks()
        
        # Game state
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
        self.user_input = 0
        self.high_score = 0
        self.streak = 0
        self.best_streak = 0
        
        # Game positions
        self.LANE_Y = height // 2
        self.TOLL_X = width - 250
        
        # Visual effects
        self.particles = ParticleSystem()
        
        # UI elements
        self.submit_btn = Button(pygame.Rect(0, 0, 180, 50), "Submit ✓", GREEN, (0, 200, 0))
        self.reset_btn = Button(pygame.Rect(0, 0, 180, 50), "Reset ✕", RED, (255, 100, 100))
        
        self.grid_start_x = 0
        self.grid_start_y = 0
        self.buttons = []
        self.update_button_positions()

    def reset_game(self):
        """Reset game state for new game"""
        if self.score > self.high_score:
            self.high_score = self.score
        if self.streak > self.best_streak:
            self.best_streak = self.streak
            
        self.queue.clear()
        self.score = 0
        self.lives = STARTING_LIVES
        self.user_input = 0
        self.game_over = False
        self.streak = 0
        self.particles.clear()
        self.last_spawn = pygame.time.get_ticks()

    def update_button_positions(self):
        """Update positions of all UI buttons"""
        grid_rows = (len(COINS) + GRID_COLS - 1) // GRID_COLS
        self.grid_start_x = self.window_width - (GRID_COLS * (BUTTON_WIDTH + BUTTON_MARGIN)) - 20
        self.grid_start_y = self.window_height - (grid_rows * (BUTTON_HEIGHT + BUTTON_MARGIN)) - 20

        # Create coin buttons
        self.buttons = []
        for i, coin in enumerate(COINS):
            row = i // GRID_COLS
            col = i % GRID_COLS
            x = self.grid_start_x + col * (BUTTON_WIDTH + BUTTON_MARGIN)
            y = self.grid_start_y + row * (BUTTON_HEIGHT + BUTTON_MARGIN)
            
            # Color gradient based on coin value
            reverse_i = len(COINS) - 1 - i
            btn_color = (100 + reverse_i * 20, 180, 100)
            hover_color = (120 + reverse_i * 20, 220, 120)
            self.buttons.append(Button(pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 
                                      f"${coin}", btn_color, hover_color))

        # Position submit and reset buttons
        self.reset_btn.rect.topleft = (self.grid_start_x, self.grid_start_y - 60)
        self.submit_btn.rect.topleft = (self.grid_start_x + 200, self.grid_start_y - 60)

    def resize(self, width, height):
        """Handle window resize"""
        self.window_width = width
        self.window_height = height
        self.LANE_Y = height // 2
        self.TOLL_X = width - 250
        self.update_button_positions()

    def spawn_car(self):
        """Spawn a new car if enough time has passed"""
        now = pygame.time.get_ticks()
        if now - self.last_spawn > SPAWN_INTERVAL:
            car = Car(self.LANE_Y)
            self.queue.append(car)
            self.last_spawn = now

    def handle_click(self, pos):
        """Handle mouse click on buttons"""
        # Coin buttons
        for btn in self.buttons:
            if btn.is_clicked(pos):
                try:
                    coin_val = int(btn.text.replace("$", ""))
                    self.user_input += min(coin_val, 1000)
                except:
                    pass
        
        # Submit button
        if self.submit_btn.is_clicked(pos):
            self.check_change()
        
        # Reset button
        if self.reset_btn.is_clicked(pos):
            self.user_input = 0

    def check_change(self):
        """Check if the user's change input is correct"""
        if not self.queue:
            self.user_input = 0
            return
            
        front_car = self.queue[0]
        correct_change = front_car.payment - front_car.fee
        
        if self.user_input == correct_change:
            self.score += 1
            self.streak += 1
            self.particles.add_particles(self.TOLL_X + TOLL_WIDTH // 2, self.LANE_Y, GREEN)
        else:
            self.lives -= 1
            self.streak = 0
            self.particles.add_particles(self.TOLL_X + TOLL_WIDTH // 2, self.LANE_Y, RED)
        
        self.queue.popleft()
        self.user_input = 0
        
        if self.lives <= 0:
            self.game_over = True

    def update(self):
        """Update game state"""
        # Update car movements
        for i, car in enumerate(self.queue):
            if i == 0:
                if not car.at_toll(self.TOLL_X):
                    car.move()
            else:
                front_car = self.queue[i - 1]
                distance = front_car.x - car.x - CAR_WIDTH
                if distance > CAR_GAP:
                    car.move()
        
        # Update particles
        self.particles.update()
        
        # Check for game over
        if len(self.queue) >= MAX_QUEUE_VISUAL:
            self.game_over = True

    def draw(self, screen):
        """Draw all game elements"""
        # Background
        screen.fill(SKY_BLUE)
        
        # Road
        road_y = self.LANE_Y - 50
        pygame.draw.rect(screen, DARK_GRAY, (0, road_y, self.window_width, 100))
        
        # Lane markings
        for x in range(0, self.window_width, 40):
            pygame.draw.rect(screen, YELLOW, (x, self.LANE_Y - 2, 25, 4))
        
        # Toll booth
        shadow_offset = 3
        pygame.draw.rect(screen, (0, 100, 0), 
                        (self.TOLL_X + shadow_offset, self.LANE_Y - 60 + shadow_offset, 
                         TOLL_WIDTH, CAR_HEIGHT + 20), border_radius=8)
        pygame.draw.rect(screen, GREEN, 
                        (self.TOLL_X, self.LANE_Y - 60, TOLL_WIDTH, CAR_HEIGHT + 20), 
                        border_radius=8)
        pygame.draw.rect(screen, BLACK, 
                        (self.TOLL_X, self.LANE_Y - 60, TOLL_WIDTH, CAR_HEIGHT + 20), 
                        3, border_radius=8)
        
        font = pygame.font.SysFont("Arial", FONT_SIZE)
        booth_text = font.render("TOLL", True, WHITE)
        screen.blit(booth_text, (self.TOLL_X + 20, self.LANE_Y - 50))
        
        # Cars
        for car in self.queue:
            car.draw(screen)
        
        # Particles
        self.particles.draw(screen)
        
        # Score display
        self._draw_score_panel(screen)
        
        # Control panel
        self._draw_control_panel(screen)

    def _draw_score_panel(self, screen):
        """Draw the score information panel"""
        info_bg = pygame.Surface((300, 80), pygame.SRCALPHA)
        pygame.draw.rect(info_bg, (*PANEL_BG, 200), (0, 0, 300, 80), border_radius=10)
        screen.blit(info_bg, (10, 10))
        
        font = pygame.font.SysFont("Arial", FONT_SIZE)
        subtitle_font = pygame.font.SysFont("Arial", SUBTITLE_FONT_SIZE)
        
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {'❤' * self.lives}", True, RED)
        streak_text = subtitle_font.render(f"Streak: {self.streak}", True, YELLOW)
        
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 45))
        screen.blit(streak_text, (160, 20))

    def _draw_control_panel(self, screen):
        """Draw the control panel with payment info and buttons"""
        panel_x = self.grid_start_x - 10
        panel_y = self.reset_btn.rect.y - 60
        panel_width = (BUTTON_WIDTH + BUTTON_MARGIN) * GRID_COLS + 20
        panel_height = (BUTTON_HEIGHT + BUTTON_MARGIN) * ((len(COINS) + GRID_COLS - 1) // GRID_COLS) + 130
        
        pygame.draw.rect(screen, PANEL_BG, (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (panel_x, panel_y, panel_width, panel_height), 3, border_radius=10)
        
        # Get current car info
        if self.queue:
            front_car = self.queue[0]
            cash = front_car.payment
            fee = front_car.fee
            required_change = cash - fee
        else:
            cash = fee = required_change = 0
        
        # Draw payment info boxes
        self._draw_info_boxes(screen, cash, fee, required_change)
        
        # Draw buttons
        for btn in self.buttons:
            btn.draw(screen)
        self.submit_btn.draw(screen)
        self.reset_btn.draw(screen)

    def _draw_info_boxes(self, screen, cash, fee, required_change):
        """Draw the payment, fee, and change info boxes"""
        info_y = self.reset_btn.rect.y - 45
        info_x = self.reset_btn.rect.x + 10
        
        box_width = 85
        box_height = 38
        box_spacing = 8
        
        value_font = pygame.font.SysFont("Arial", 22, bold=True)
        label_font = pygame.font.SysFont("Arial", 12)
        
        # Payment box
        payment_x = info_x
        pygame.draw.rect(screen, (40, 40, 80), (payment_x, info_y, box_width, box_height), border_radius=5)
        pygame.draw.rect(screen, WHITE, (payment_x, info_y, box_width, box_height), 2, border_radius=5)
        payment_label = label_font.render("Payment", True, WHITE)
        payment_value = value_font.render(f"${cash}", True, WHITE)
        screen.blit(payment_label, (payment_x + box_width // 2 - payment_label.get_width() // 2, info_y + 1))
        screen.blit(payment_value, (payment_x + box_width // 2 - payment_value.get_width() // 2, info_y + 13))
        
        # Fee box
        fee_x = payment_x + box_width + box_spacing
        pygame.draw.rect(screen, (80, 40, 40), (fee_x, info_y, box_width, box_height), border_radius=5)
        pygame.draw.rect(screen, RED, (fee_x, info_y, box_width, box_height), 3, border_radius=5)
        fee_label = label_font.render("Fee", True, WHITE)
        fee_value = value_font.render(f"${fee}", True, RED)
        screen.blit(fee_label, (fee_x + box_width // 2 - fee_label.get_width() // 2, info_y + 1))
        screen.blit(fee_value, (fee_x + box_width // 2 - fee_value.get_width() // 2, info_y + 13))
        
        # Change box
        change_x = fee_x + box_width + box_spacing
        pygame.draw.rect(screen, (40, 40, 40), (change_x, info_y, box_width, box_height), border_radius=5)
        pygame.draw.rect(screen, YELLOW, (change_x, info_y, box_width, box_height), 3, border_radius=5)
        change_label = label_font.render("Change", True, WHITE)
        change_value = value_font.render(f"${self.user_input}", True, YELLOW)
        screen.blit(change_label, (change_x + box_width // 2 - change_label.get_width() // 2, info_y + 1))
        screen.blit(change_value, (change_x + box_width // 2 - change_value.get_width() // 2, info_y + 13))
        
        # Required change hint
        font = pygame.font.SysFont("Arial", FONT_SIZE)
        required_text = font.render(f"(Need: ${required_change})", True, (150, 255, 150))
        screen.blit(required_text, (info_x + 10, info_y + box_height + 5))

