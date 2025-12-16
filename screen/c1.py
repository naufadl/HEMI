import pygame
from .base import ScreenBase
from ui.button import Button
from src.coin import Spinning_Coin, Coin

class C1(ScreenBase):
    def __init__(self, manager, screen_size, player_coin):
        super().__init__(manager, screen_size)
        self.screen_size = screen_size
        self.coins=player_coin
        
        self.cx=self.screen_size[0]//2
        self.cy=self.screen_size[1]//2

        

        #animasi coin
        self.coin_display = Spinning_Coin(10, 10, self.coins)

        #status chapter
        self.current_question = 0
        self.is_completed = False

        #background
        image_path = r"assets\images\background_soal\soal.jpg"
        bg_image=pygame.image.load(image_path).convert()
        self.bg=pygame.transform.scale(bg_image, screen_size)

        #font
        self.font_question=pygame.font.SysFont(None,48)
        self.font_button=pygame.font.SysFont(None,28)

        self.back_button = Button("Back to Menu",
                                  (self.cx, self.cy + 100),
                                  (200, 50),
                                  lambda: self.manager.go_to("Soal"),
                                  self.font_button)

        #soal
        self.questions = [
            {"question": "2 x 2 = ?", "options": ["3","4","5"], "answer":"4"},
            {"question": "5 x 3 = ?", "options": ["15","10","20"], "answer":"15"}
        ]

        #tombol jawaban
        self.buttons = []
        self.create_buttons(self.cx, self.cy)


    def create_buttons(self, cx,cy):
        self.buttons.clear()
        q = self.questions[self.current_question]
        for i, opt in enumerate(q["options"]):
            btn = Button(opt, (cx, cy + i*60), (200, 50), lambda o=opt: self.check_answer(o), self.font_button)
            self.buttons.append(btn)

    def check_answer(self, selected):
        q = self.questions[self.current_question]
        if selected == q["answer"]:
            self.coins.add_coin(10)
        


        self.current_question += 1
        if self.current_question >= len(self.questions):
            print("Chapter selesai. Total coins:", self.coins)
            self.is_completed = True
            self.manager.go_to('Soal')  # balik ke menu soal
        else:
            # update tombol untuk soal selanjutnya
            cx, cy = self.screen_width//2, self.screen_height//2
            self.create_buttons(cx, cy)

    def handle_event(self, event):
        if self.is_completed:
            self.back_button.handle_event(event)
            return
        for btn in self.buttons:
            btn.handle_event(event)
    
    def update(self, dt):
        pass
    
    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.coin_display.draw(surface, self.font_button)
        
        cx=self.screen_size[0]//2
        cy=self.screen_size[1]//2 

        if self.is_completed:
            msg = "Chapter ini sudah diselesaikan!"
            txt = self.font_question.render(msg, True, (255, 0, 0)) # Warna merah
            surface.blit(txt, (cx - txt.get_width()//2, cy - txt.get_height()//2))

            self.back_button.draw(surface)


        elif self.current_question < len(self.questions):
            # TAMPILKAN SOAL JIKA BELUM SELESAI
            q = self.questions[self.current_question]
            txt = self.font_question.render(q["question"], True, (0,0,0))
            surface.blit(txt, (cx - txt.get_width()//2, 150))
            
            # GAMBAR TOMBOL
            for btn in self.buttons:
                btn.draw(surface)   
       