import pygame
from config import *
import random

class Button:
    """Represents a clickable button with hover effect"""
    
    def __init__(self, rect, text, color=GRAY, hover_color=(200, 200, 200)):
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        """Draw the button with hover effect"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=8)
        
        font = pygame.font.SysFont("Arial", FONT_SIZE)
        txt = font.render(str(self.text), True, BLACK)
        txt_rect = txt.get_rect(center=self.rect.center)
        screen.blit(txt, txt_rect)

    def update_hover(self, pos):
        """Update hover state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(pos)


class ParticleSystem:
    """Manages particle effects for visual feedback"""
    
    def __init__(self):
        self.particles = []

    def add_particles(self, x, y, color, count=20):
        """Add burst of particles at position"""
        for _ in range(count):
            vel_x = random.uniform(-3, 3)
            vel_y = random.uniform(-5, -1)
            self.particles.append({
                'x': x, 'y': y,
                'vx': vel_x, 'vy': vel_y,
                'color': color,
                'life': 60
            })

    def update(self):
        """Update all particles"""
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.2  # gravity
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        """Draw all particles"""
        for p in self.particles:
            alpha = int(255 * (p['life'] / 60))
            color = (*p['color'], alpha)
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (3, 3), 3)
            screen.blit(s, (int(p['x']), int(p['y'])))

    def clear(self):
        """Clear all particles"""
        self.particles.clear()
