import pygame
from .base import ScreenBase
from ui.button import Button
from src.coin import Spinning_Coin, Coin

class MainMenuScreen(ScreenBase):
    def __init__(self, manager, screen_size, player_coin):
        super().__init__(manager, screen_size)
        self.screen_size=screen_size

        
        image_path = r"C:\Users\tutii\Downloads\FP PBO\HEMI\assets\images\background_main_menu\Summer2.png"

        #background
        bg_image=pygame.image.load(image_path).convert()
        self.bg=pygame.transform.scale(bg_image, screen_size)

        #title+button
        self.font_title=pygame.font.SysFont(None,48)
        self.font_button=pygame.font.SysFont(None,28)

        #gambar coin
        coin_pos_x = 20
        coin_pos_y = 20
        self.coin_display = Spinning_Coin(coin_pos_x, coin_pos_y, player_coin)

        #titik acuan tengah layar
        cx=screen_size[0]//2
        cy=screen_size[1]//2

        self.buttons=[
            Button("Game", (cx+250,cy), (180,40), self.game, self.font_button),
            Button('Soal', (cx+250,cy+100), (180,40), self.soal, self.font_button),
            Button('Exit',(cx+250,cy+200), (180,40), self.exit, self.font_button)
        ]

    def game(self):
        self.manager.go_to('game')

    def soal(self):
        self.manager.go_to('Soal')

    def exit(self):
        pygame.quit()
        raise SystemExit
        
        
    def handle_event(self, event):
        for i in self.buttons:
            i.handle_event(event)

    def update(self, dt):
        self.coin_display.update()

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        title=self.font_title.render("HEMI", True, (255,255,255))
        surface.blit(title, (self.screen_width//2-45, 120))

        self.coin_display.draw(surface, self.font_button)

        for i in self.buttons:
            i.draw(surface)