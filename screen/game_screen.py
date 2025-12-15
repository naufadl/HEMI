import pygame
import os
from .base import ScreenBase 
from src.frog import Frog
from src.world.world import World

BASE_DIR = os.path.dirname(__file__)  
ASSET_DIR = os.path.join(BASE_DIR, "..", "assets", "images", "player")
ASSET_DIR = os.path.abspath(ASSET_DIR)

class GameScreen(ScreenBase):
    def __init__(self, manager, screen_size):
        super().__init__(manager, screen_size)

        self.screen_width, self.screen_height = screen_size
        self.background_color = (171, 214, 236)

        frog_start_x = self.screen_width // 2 - 40
        frog_start_y = self.screen_height - 80
        self.frog = Frog(frog_start_x, frog_start_y) 

        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.is_paused = False
        
        self.key_states = {'left': False, 'right': False}
        
        self.world = World()
        self.world.load_simple_level(self.screen_height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                self.frog.jump()
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self.key_states['left'] = True
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.key_states['right'] = True
            elif event.key == pygame.K_w:
                 self.frog.attack()
            elif event.key == pygame.K_ESCAPE:
                self.is_paused = not self.is_paused
            elif event.key == pygame.K_m and self.is_paused:
                self.manager.go_to("Main_menu")
                self.reset_game()
                
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                self.key_states['left'] = False
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self.key_states['right'] = False

        if event.type == pygame.MOUSEBUTTONDOWN and not self.is_paused:
            self.frog.jump()

    def update(self, dt):
        if not self.is_paused:
            if self.key_states['left']:
                self.frog.x_pos -= self.frog.MOVE_SPEED * dt * 60
                self.frog.move_left()
            elif self.key_states['right']:
                self.frog.x_pos += self.frog.MOVE_SPEED * dt * 60
                self.frog.move_right()
            elif not self.frog.is_jumping: # Jika tidak bergerak dan tidak lompat, idle
                self.frog.idle()
                
            self.frog.apply_gravity(dt)
            
            self.frog.rect.x = int(self.frog.x_pos)
            self.frog.rect.y = int(self.frog.y_pos)
            
            for tile in self.world.get_collisions(self.frog.rect):
                if self.frog.velocity_y > 0 and \
                    self.frog.rect.bottom <= tile.rect.bottom:  # jatuh
                    self.frog.land_on(tile.rect)
                    
            if not self.frog.is_dead:
                self.score += dt * 10
                
            self.frog.update(dt)

    def draw(self, surface):
        surface.fill(self.background_color)
        self.world.draw(surface)
        self.frog.draw(surface)

        score_text = self.font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

        if self.is_paused:
            self.draw_pause_overlay(surface)

    def draw_pause_overlay(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        pause_font = pygame.font.SysFont(None, 72)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        menu_text = self.font.render("Press M to return to menu", True, (255, 255, 255))

        surface.blit(
            pause_text,
            (self.screen_width // 2 - pause_text.get_width() // 2, self.screen_height // 2 - 50),
        )
        surface.blit(
            menu_text,
            (self.screen_width // 2 - menu_text.get_width() // 2, self.screen_height // 2 + 50),
        )

    def reset_game(self):
        self.score = 0
        self.is_paused = False
        start_x = self.screen_width // 2 - 40
        start_y = self.screen_height - 80
        self.frog = Frog(start_x, start_y)
        self.key_states = {'left': False, 'right': False}