import pygame
from .base import ScreenBase
from ui.button import Button
from src.frog import Frog
from src.coin import Spinning_Coin, Coin

class MainMenuScreen(ScreenBase):
    def __init__(self, manager, screen_size, player_coin):
        super().__init__(manager, screen_size)
        self.screen_size=screen_size
        self.player_coin=player_coin
        self.error_text = None

        
        image_path = "assets/images/background_main_menu/HEMI.png"

        #background
        bg_image=pygame.image.load(image_path).convert()
        self.bg=pygame.transform.scale(bg_image, screen_size)

        #title+button
        self.font_title=pygame.font.SysFont(None,48)
        #self.font_button=pygame.font.SysFont(None, 35)

        self.font_button=pygame.font.Font("assets/font/PixelOperator8-Bold.ttf", 21)

        #gambar coin
        coin_pos_x = 20
        coin_pos_y = 20
        self.coin_display = Spinning_Coin(coin_pos_x, coin_pos_y, player_coin)

        #titik acuan tengah layar
        cx=screen_size[0]//2
        cy=screen_size[1]//2

        self.frog = Frog(500, 500, scale=15.0)
        self.frog.current_row = self.frog.ROW_IDLE
        self.frog.current_frame = 0.0
        
        self.buttons=[
            Button("Game", (cx+150,cy), (180,80), self.game, self.font_button),
            Button('Soal', (cx+150,cy+100), (180,80), self.soal, self.font_button),
            Button('Exit',(cx+150,cy+200), (180,80), self.exit, self.font_button)
        ]

    def game(self):
        if self.player_coin.use_coin(10):
            self.manager.go_to('game')
        else:
            self.error_text="coin tidak cukup"
            self.error_timer=pygame.time.get_ticks()

    def soal(self):
        self.manager.go_to('Soal')

    def exit(self):
        pygame.quit()
        raise SystemExit
        
    def handle_event(self, event):
        for i in self.buttons:
            i.handle_event(event)

    def update(self, dt):
        self.frog.update(dt)
        self.coin_display.update()
        pass

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.frog.draw(surface)

        self.coin_display.draw(surface, self.font_button)

        if self.error_text:
            text = self.font_button.render(self.error_text, True, (255, 0, 0))
            rect = text.get_rect(center=(self.screen_size[0]//2-230, self.screen_size[1]//2))
            surface.blit(text, rect)

        for i in self.buttons:
            i.draw(surface)