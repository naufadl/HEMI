import pygame
from .base import ScreenBase
from UI.button import Button

class MainMenuScreen(ScreenBase):
    def __init__(self, manager, screen_size):
        super().__init__(manager, screen_size)
        
        self.font_title=pygame.font.SysFont(None,48)
        self.font_button=pygame.font.SysFont(None,28)

        cx=screen_size[0]//2
        cy=screen_size[1]//2-40

        self.buttons=[
            Button("Game", (cx,cy+100), (180,40), self.game, self.font_button),
            Button('Soal', (cx+250,cy+100), (180,40), self.soal, self.font_button),
            Button('Exit',(cx-250,cy+100), (180,40), self.exit, self.font_button)
        ]

    def game(self):
        self.manager.go_to('game')

    def soal(self):
        self.manager.go_to('soal')

    def exit(self):
        pygame.quit()
        raise SystemExit
        
        
    def handle_event(self, event):
        for i in self.buttons:
            i.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill((255,255,255))
        title=self.font_title.render("HEMI", True, (0,0,0))
        surface.blit(title, (self.screen_width//2-45, 120))

        for i in self.buttons:
            i.draw(surface)