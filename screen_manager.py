from screen.main_menu import MainMenuScreen
from screen.game_screen import GameScreen
from screen.soal import Soal
from src.coin import Coin


class ScreenManager:
    def __init__(self, screen_size):
        self.screen_size=screen_size
        self.screens={}
        self.current_screen=None
        self.player_coin=Coin(0)
        self._register_screen()

    def _register_screen(self):
        self.screens["Main_menu"]=MainMenuScreen(self, self.screen_size,self.player_coin) 
        self.screens["game"]=GameScreen(self, self.screen_size)
        #self.screens["Soal"]=Soal

        self.screens["Main_menu"]=MainMenuScreen(self, self.screen_size,self.player_coin)
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