import pygame


class Coin:
    def __init__(self, coin:int):
        if coin < 0:
            coin=0
        self.__coin=coin


    @property 
    def coin(self):
        return self.__coin
        

    def add_coin(self,c):
        if isinstance(c, int) and c>0:
            self.__coin+=c


    def use_coin(self,req_c:int)->bool:
        if self.__coin >= req_c:
            self.__coin -= req_c
            return True
        return False
        

    def check_coin(self,req_c:int)->bool:
        if self.__coin >= req_c:
            return True
        else:
            return False
        


class Spinning_Coin:
    def __init__(self, x,y, coin_value):
        path_asset_coin=r'assets\images\coin\coin.png'

        coin_width, coin_high, num_frames=16,16,12

        sheet=pygame.image.load(path_asset_coin).convert_alpha() 
        self.coin_data=coin_value

        self.x=x
        self.y=y

        self.frames=self._load_frames(sheet,coin_width, coin_high, num_frames)
        self.current_frame=0
        self.animation_speed=0.25

    def _load_frames(self, sheet,w,h,n):
        frames=[]
        for i in range(n):
            frame_rect= pygame.Rect(i * w, 0, w, h)
            image = pygame.Surface((w, h), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), frame_rect)
            frames.append(image)
        return frames


    def update(self):
        self.current_frame+= self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame= 0.0
            
    def draw(self, surface,font):
        coin_image = self.frames[int(self.current_frame)]
        surface.blit(coin_image, (self.x, self.y))
        coin_value = self.coin_data.coin

        coin_text = f"{coin_value}" # Hanya angkanya saja
        text_surface = font.render(coin_text, True, (0, 0, 0)) 

        text_x = self.x + coin_image.get_width() + 5 # 5 pixel spasi
        text_y = self.y + (coin_image.get_height() // 2) - (text_surface.get_height() // 2)
        
        surface.blit(text_surface, (text_x, text_y))


