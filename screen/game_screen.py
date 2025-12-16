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
        self.world.load_tilemap_from_file('levels/level1.txt')

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
        is_moving = False
        if not self.is_paused:
            old_x = self.frog.x_pos
            old_y = self.frog.y_pos
            if self.key_states['left']:
                self.frog.x_pos -= self.frog.MOVE_SPEED * dt 
                self.frog.move_left()
                is_moving = True
            elif self.key_states['right']:
                self.frog.x_pos += self.frog.MOVE_SPEED * dt 
                self.frog.move_right()
                is_moving = True
                
            if not is_moving and self.frog.on_ground and self.frog.current_row != self.frog.ROW_ATTACK:
                self.frog.current_row = self.frog.ROW_IDLE
                
            self.frog.apply_gravity(dt)
            
            self.frog.rect.x = int(self.frog.x_pos)
            self.frog.rect.y = int(self.frog.y_pos)
            
            self.handle_collisions(old_x, old_y)
            
            if self.frog.rect.top > self.screen_height:
                self.frog.die()
                    
            if not self.frog.is_dead:
                self.score += dt * 10
                
            self.frog.update(dt)
            
            print("row:", self.frog.current_row, "moving:", is_moving)

            
    def handle_collisions(self, old_x, old_y):
        tiles = self.world.get_collisions(self.frog.rect)

        # === HORIZONTAL COLLISION ===
        self.frog.rect.x = int(self.frog.x_pos)
        for tile in tiles:
            if self.frog.rect.colliderect(tile.rect):
                self.frog.x_pos = old_x
                self.frog.rect.x = int(old_x)
                break

        # === VERTICAL COLLISION ===
        self.frog.rect.y = int(self.frog.y_pos)

        for tile in tiles:
            if self.frog.rect.colliderect(tile.rect):
                # JATUH KE ATAS TILE
                if self.frog.velocity_y > 0 and old_y + self.frog.rect.height <= tile.rect.top:
                    self.frog.rect.bottom = tile.rect.top
                    self.frog.y_pos = float(self.frog.rect.y)
                    self.frog.velocity_y = 0
                    self.frog.on_ground = True

                # BENTUR KEPALA
                elif self.frog.velocity_y < 0 and old_y >= tile.rect.bottom:
                    self.frog.rect.top = tile.rect.bottom
                    self.frog.y_pos = float(self.frog.rect.y)
                    self.frog.velocity_y = 0


    def draw(self, surface):
        surface.fill(self.background_color)
        self.world.draw(surface)
        self.frog.draw(surface)

        score_text = self.font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

        if self.is_paused:
            self.draw_pause_overlay(surface)
            
        pygame.draw.rect(surface, (255,0,0), self.frog.rect, 2)
        for tile in self.world.tiles:
            pygame.draw.rect(surface, (0,255,0), tile.rect, 1)


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