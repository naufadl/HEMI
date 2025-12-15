import pygame
from .base import ScreenBase
from ui.button import Button
from .c1 import C1
from src.coin import Spinning_Coin, Coin

class Soal(ScreenBase):
    def __init__(self,manager, screen_size, player_coin):
        super().__init__(manager, screen_size)
        self.coins=player_coin

        image_path = r"C:\Users\tutii\Downloads\FP PBO\HEMI\assets\images\background_soal\origbig.png"

        bg_image=pygame.image.load(image_path).convert()
        self.bg=pygame.transform.scale(bg_image, screen_size)

        self.font_title=pygame.font.SysFont(None,48)
        self.font_button=pygame.font.SysFont(None,28)

        self.coin_display = Spinning_Coin(10, 10, self.coins)

        cx=screen_size[0]//2
        cy=screen_size[1]//2-40

        self.buttons=[
            Button("Chapter 1", (cx,cy), (180,40), self.c1, self.font_button),
            Button('Chapter 2', (cx+250,cy+100), (180,40),  self.c2, self.font_button),
            Button('Chapter 3',(cx,cy+100), (180,40), self.c3, self.font_button),
            Button('Chapter 4',(cx-250,cy+100), (180,40),  self.c4, self.font_button),
            Button('Chapter 5',(cx,cy+200), (180,40), self.c5,  self.font_button),
            Button('Previous', (cx-390, cy+270), (100,40), self.prev_from_soal, self.font_button)
        ]


    def c1(self):
        self.manager.go_to('c1')

    def c2(self):
        self.manager.go_to('c2')

    def c3(self):
        self.manager.go_to('c3')

    def c4(self):
        self.manager.go_to('c4')

    def c5(self):
        self.manager.go_to('c5')

    def prev_from_soal(self):
        self.manager.go_to('Main_menu')

    def handle_event(self, event):
        for i in self.buttons:
            i.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        title=self.font_title.render("Oh noooo, i really like this course", True, (0,0,180))
        surface.blit(title, (self.screen_width//2-(title.get_width()//2), 80))

        self.coin_display.draw(surface, self.font_button)

        for i in self.buttons:
            i.draw(surface)

    



