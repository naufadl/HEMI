from screen.main_menu import MainMenuScreen
from screen.game_screen import GameScreen
#buat game dan soal
from screen.soal import Soal


class ScreenManager:
    def __init__(self, screen_size):
        self.screen_size=screen_size
        self.screens={}
        self.current_screen=None
        self._register_screen()

    def _register_screen(self):
        self.screens["Main_menu"]=MainMenuScreen(self, self.screen_size) 
        self.screens["game"]=GameScreen(self, self.screen_size)
        #self.screens["Soal"]=Soal

        self.screens["Main_menu"]=MainMenuScreen(self, self.screen_size)
        self.screens["Soal"]=Soal(self,self.screen_size)
        
        self.go_to("Main_menu")

    def go_to(self, name):
        self.current_screen=self.screens[name]

    def handle_event(self, event):
        self.current_screen.handle_event(event)

    def update(self, dt):
        self.current_screen.update(dt)

    def draw(self,surface):
        self.current_screen.draw(surface)