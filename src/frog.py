import pygame

class Frog:
    ROW_IDLE = 0
    ROW_WALK = 1
    ROW_DEAD = 2
    ROW_ATTACK = 3
    
    JUMP_FORCE = 15 
    GRAVITY = 0.8
    MOVE_SPEED = 4

    def __init__(self, x, y):
        try:
            self.sprite_sheet = pygame.image.load(
                'assets/images/player/frog_spritesheet.png'
            ).convert_alpha()
        except Exception as e:
            print("Warning: Failed to load spritesheet", e)
            self.sprite_sheet = None

        self.frame_height = 32

        self.frames_per_row = {
            self.ROW_IDLE: 4,
            self.ROW_WALK: 7,
            self.ROW_DEAD: 2,
            self.ROW_ATTACK: 4
        }

        self.frame_widths = {
            self.ROW_IDLE: 64,  
            self.ROW_WALK: 64,  
            self.ROW_DEAD: 64,
            self.ROW_ATTACK: 64
        }

        self.current_row = self.ROW_IDLE
        self.current_frame = 0.0
        self.animation_speed = 0.20

        self.facing_left = False
        self.is_dead = False
        
        # posisi
        self.rect = pygame.Rect(x, y, 64 * 2.5, 32 * 2.5)
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        
        self.x_pos = float(x)
        self.y_pos = float(y)
        self.ground_y = float(y)
        
        self.is_jumping = False
        self.velocity_y = 0.0

        self.update_sprite()


    # gerak
    
    def jump(self):
        if not self.is_dead:
            self.is_jumping = True
            self.velocity_y = -self.JUMP_FORCE
            self.current_row = self.ROW_WALK

    def move_right(self):
        if not self.is_dead:
            self.current_row = self.ROW_WALK
            self.facing_left = False

    def move_left(self):
        if not self.is_dead:
            self.current_row = self.ROW_WALK
            self.facing_left = True

    def idle(self):
        if not self.is_dead and not self.is_jumping and self.current_row != self.ROW_ATTACK:
            self.current_row = self.ROW_IDLE

    def attack(self):
        if not self.is_dead:
            self.current_row = self.ROW_ATTACK
            self.current_frame = 0.0

    def die(self):
        self.is_dead = True
        self.current_row = self.ROW_DEAD
        self.current_frame = 0.0

    # animasi

    def animate(self):
        total = self.frames_per_row[self.current_row]
        self.current_frame += self.animation_speed

        if self.current_frame >= total:
            if self.current_row == self.ROW_ATTACK:
                self.current_row = self.ROW_IDLE
                self.current_frame = 0.0
            elif self.current_row == self.ROW_DEAD:
                self.current_frame = total - 1.0  # freeze
                return
            else:
                self.current_frame = 0.0

        self.update_sprite()

    def update_sprite(self):
        frame_w = self.frame_widths[self.current_row]
        frame_h = self.frame_height
        idx = int(self.current_frame)

        src = pygame.Rect(
            idx * frame_w, 
            self.current_row * frame_h,
            frame_w,
            frame_h
        )

        img = self.sprite_sheet.subsurface(src)
        
        scale = 2.5
        img = pygame.transform.scale(
        img,
        (int(frame_w * scale), int(frame_h * scale))
        )
        
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        
        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect(midbottom=old_midbottom)
        
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)
        
        current_x = self.rect.x
        current_y = self.rect.y
        temp_rect = self.image.get_rect()
        self.rect.width = temp_rect.width
        self.rect.height = temp_rect.height
        self.rect.x = current_x 
        self.rect.y = current_y

    # update

    def update(self, dt):
        # 1. Update Jump/Gravity
        if self.is_jumping:
            self.velocity_y += self.GRAVITY * dt * 60 
            self.y_pos += self.velocity_y * dt * 60
            
            # Cek jika sudah mendarat
            if self.y_pos >= self.ground_y:
                self.y_pos = self.ground_y
                self.is_jumping = False
                self.velocity_y = 0.0
                self.idle()
        
        # 2. Update posisi Rect
        self.rect.x = int(self.x_pos)
        self.rect.y = int(self.y_pos)
        
        # 3. Update Animasi
        self.animate()

    def draw(self, surface):
        surface.blit(self.image, self.rect)