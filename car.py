import pygame
import random
from config import *

class Car:
    """Represents a car in the toll queue"""
    
    def __init__(self, lane_y):
        self.fee = random.choice(TOLL_FEES)
        self.payment = random.choice(PAYMENTS)
        self.x = -CAR_WIDTH
        self.y = lane_y
        self.color = random.choice(CAR_COLORS)
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)

    def move(self):
        """Move the car forward"""
        self.x += CAR_SPEED
        self.rect.x = self.x

    def draw(self, screen):
        """Draw the car with windows and payment display"""
        # Car body
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        
        # Windows
        window_color = (200, 230, 255)
        pygame.draw.rect(screen, window_color, (self.x + 15, self.y + 8, 12, 10), border_radius=2)
        pygame.draw.rect(screen, window_color, (self.x + 33, self.y + 8, 12, 10), border_radius=2)
        
        # Payment display
        font = pygame.font.SysFont("Arial", FONT_SIZE)
        text = font.render(f"${self.payment}", True, WHITE)
        text_bg = pygame.Surface((text.get_width() + 4, text.get_height() + 2))
        text_bg.fill(BLACK)
        text_bg.set_alpha(150)
        screen.blit(text_bg, (self.x + 8, self.y + 22))
        screen.blit(text, (self.x + 10, self.y + 23))

    def at_toll(self, toll_x):
        """Check if car has reached the toll booth"""
        return self.x + CAR_WIDTH >= toll_x

