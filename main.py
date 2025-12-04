# main.py
import pygame
import sys
from config import *
from game_logic import TollSimulator
from ui_components import Button

def main():
    """Main game loop"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Toll Gate Queue Simulator")
    clock = pygame.time.Clock()
    
    # Initialize fonts
    title_font = pygame.font.SysFont("Arial", TITLE_FONT_SIZE, bold=True)
    subtitle_font = pygame.font.SysFont("Arial", SUBTITLE_FONT_SIZE)
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    
    # Game instances
    game = TollSimulator(WINDOW_WIDTH, WINDOW_HEIGHT)
    background_game = TollSimulator(WINDOW_WIDTH, WINDOW_HEIGHT)
    in_main_menu = True
    
    # Menu buttons
    start_button = Button(pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 25, 300, 60),
                         "START GAME", GREEN, (0, 200, 0))
    try_again_button = Button(pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, 300, 60),
                              "TRY AGAIN", YELLOW, (255, 220, 50))
    quit_button = Button(pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 125, 300, 60),
                        "QUIT", RED, (255, 100, 100))
    
    # Main game loop
    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                game.resize(event.w, event.h)
                background_game.resize(event.w, event.h)
                start_button.rect.center = (event.w // 2, event.h // 2)
                try_again_button.rect.center = (event.w // 2, event.h // 2 + 75)
                quit_button.rect.center = (event.w // 2, event.h // 2 + 150)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_main_menu:
                    if start_button.is_clicked(event.pos):
                        in_main_menu = False
                        game.reset_game()
                elif game.game_over:
                    if try_again_button.is_clicked(event.pos):
                        game.reset_game()
                    elif quit_button.is_clicked(event.pos):
                        in_main_menu = True
                        background_game.reset_game()
                else:
                    game.handle_click(event.pos)
        
        # Main Menu
        if in_main_menu:
            draw_main_menu(screen, background_game, start_button, game.high_score, 
                          mouse_pos, title_font, subtitle_font)
            pygame.display.flip()
            continue
        
        # Game Over Screen
        if game.game_over:
            draw_game_over(screen, game, try_again_button, quit_button, 
                          mouse_pos, title_font, subtitle_font, font)
            pygame.display.flip()
            continue
        
        # Gameplay
        game.spawn_car()
        game.update()
        
        # Update button hover states
        for btn in game.buttons:
            btn.update_hover(mouse_pos)
        game.submit_btn.update_hover(mouse_pos)
        game.reset_btn.update_hover(mouse_pos)
        
        game.draw(screen)
        pygame.display.flip()


def draw_main_menu(screen, background_game, start_button, high_score, 
                   mouse_pos, title_font, subtitle_font):
    """Draw the main menu with animated background"""
    # Animated background
    background_game.spawn_car()
    background_game.update()
    background_game.draw(screen)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))
    
    # Title with shadow
    title = title_font.render("TOLL GATE SIMULATOR", True, BLACK)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2 + 3, 
                       screen.get_height() // 2 - 153))
    title = title_font.render("TOLL GATE SIMULATOR", True, YELLOW)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 
                       screen.get_height() // 2 - 156))
    
    # Subtitle
    subtitle = subtitle_font.render("Calculate the correct change!", True, WHITE)
    screen.blit(subtitle, (screen.get_width() // 2 - subtitle.get_width() // 2, 
                          screen.get_height() // 2 - 100))
    
    # High score
    if high_score > 0:
        hs_text = subtitle_font.render(f"High Score: {high_score}", True, GREEN)
        screen.blit(hs_text, (screen.get_width() // 2 - hs_text.get_width() // 2, 
                             screen.get_height() // 2 - 60))
    
    # Start button
    start_button.update_hover(mouse_pos)
    start_button.draw(screen)


def draw_game_over(screen, game, try_again_button, quit_button, 
                   mouse_pos, title_font, subtitle_font, font):
    """Draw the game over screen"""
    screen.fill(BLACK)
    
    # Game over title
    over_text = title_font.render("GAME OVER!", True, RED)
    screen.blit(over_text, (screen.get_width() // 2 - over_text.get_width() // 2, 
                           screen.get_height() // 2 - 120))
    
    # Final score
    score_text = subtitle_font.render(f"Final Score: {game.score}", True, WHITE)
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 
                            screen.get_height() // 2 - 60))
    
    # New high score message
    if game.score == game.high_score and game.score > 0:
        new_hs = subtitle_font.render("NEW HIGH SCORE!", True, YELLOW)
        screen.blit(new_hs, (screen.get_width() // 2 - new_hs.get_width() // 2, 
                            screen.get_height() // 2 - 30))
    
    # Best streak
    streak_text = font.render(f"Best Streak: {game.best_streak}", True, GREEN)
    screen.blit(streak_text, (screen.get_width() // 2 - streak_text.get_width() // 2, 
                             screen.get_height() // 2 + 5))
    
    # Buttons
    try_again_button.update_hover(mouse_pos)
    quit_button.update_hover(mouse_pos)
    try_again_button.draw(screen)
    quit_button.draw(screen)


if __name__ == "__main__":
    main()