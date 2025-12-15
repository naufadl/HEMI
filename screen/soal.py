import pygame
from .base import ScreenBase
from ui.button import Button

class Soal(ScreenBase):
    def __init__(self,manager, screen_size):
        super().__init__(manager, screen_size)

        image_path = r"assets\images\background_soal\origbig.png"

        bg_image=pygame.image.load(image_path).convert()
        self.bg=pygame.transform.scale(bg_image, screen_size)

        self.font_title=pygame.font.SysFont(None,48)
        self.font_button=pygame.font.SysFont(None,28)

        cx=screen_size[0]//2
        cy=screen_size[1]//2-40

        self.buttons=[
            Button("Question 1", (cx,cy), (180,40), self.q1, self.font_button),
            Button('Question 2', (cx+250,cy+100), (180,40),  self.q2, self.font_button),
            Button('Question 3',(cx,cy+100), (180,40), self.q3, self.font_button),
            Button('Question 4',(cx-250,cy+100), (180,40),  self.q4, self.font_button),
            Button('Question 5',(cx,cy+200), (180,40), self.q1,  self.font_button),
            Button('Previous', (cx-390, cy+270), (100,40), self.prev_from_soal, self.font_button)
        ]


    def q1(self):
        self.manager.go_to('q1')

    def q2(self):
        self.manager.go_to('q2')

    def q3(self):
        self.manager.go_to('q3')

    def q4(self):
        self.manager.go_to('q4')

    def q5(self):
        self.manager.go_to('q5')

    def prev_from_soal(self):
        self.manager.go_to('Main_menu')

    def handle_event(self, event):
        for i in self.buttons:
            i.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        title=self.font_title.render("Oh noooo, i really like this course", True, (255,255,255))
        surface.blit(title, (self.screen_width//2-title.get_width()//2, 80))

        for i in self.buttons:
            i.draw(surface)

    



