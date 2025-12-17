import pygame

class Frog:
    ROW_IDLE = 0
    ROW_WALK = 1
    ROW_DEAD = 2
    ROW_ATTACK = 3
    
    JUMP_FORCE = 700 
    GRAVITY = 2000
    MOVE_SPEED = 300

    def __init__(self, x, y, scale=2.5):
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
        self.scale = scale
        
        self.collision_offset_y = int(8 * self.scale)
        self.foot_offset = int(9 * self.scale)
        
        hitbox_w = int(17 * scale)
        hitbox_h = int(14 * scale)
        
        self.rect = pygame.Rect(0, 0, hitbox_w, hitbox_h)
        
        self.hitbox_offset_x = int(-15 * self.scale)
        self.sprite_offset_x = int(9 * self.scale) 

        self.rect.midbottom = (x, y)
        self.rect.x += self.hitbox_offset_x

        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)


        self.ground_y = y
        
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)
        
        self.is_jumping = False
        self.is_moving = False
        self.velocity_y = 0.0
        self.on_ground = True  

        self.update_sprite()
        
        self.rect.bottom = self.ground_y
        self.y_pos = float(self.rect.y)


    # gerak
    
    def jump(self):
        if not self.is_dead and self.on_ground:
            self.is_jumping = True
            self.velocity_y = -self.JUMP_FORCE
            self.current_row = self.ROW_WALK
            self.on_ground = False

    def move_right(self):
        if not self.is_dead:
            self.current_row = self.ROW_WALK
            self.facing_left = False
            self.is_moving = True


    def move_left(self):
        if not self.is_dead:
            self.current_row = self.ROW_WALK
            self.facing_left = True
            self.is_moving = True


    def attack(self):
        if not self.is_dead:
            self.current_row = self.ROW_ATTACK
            self.current_frame = 0.0

    def die(self):
        self.is_dead = True
        self.current_row = self.ROW_DEAD
        self.current_frame = 0.0

    # animasi

    def animate(self, dt):
        total = self.frames_per_row[self.current_row]
        self.current_frame += self.animation_speed * dt * 50

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
        
        scale = self.scale
        img = pygame.transform.scale(
        img,
        (int(frame_w * scale), int(frame_h * scale))
        )
        
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        
        self.x_pos = float(self.rect.x)
        self.y_pos = float(self.rect.y)
        

    # update

    def update(self, dt):
        self.animate(dt)

    def draw(self, surface):
        if self.facing_left:
            draw_x = self.rect.x - int(39 * self.scale)
        else:
            draw_x = self.rect.x - self.sprite_offset_x 
        
        draw_y = self.rect.bottom - self.image.get_height() + self.foot_offset
        surface.blit(self.image, (draw_x, draw_y))

        
    def apply_gravity(self, dt):
        self.velocity_y += self.GRAVITY * dt 
        self.y_pos += self.velocity_y * dt 

    def land_on(self, tile_rect):
        self.rect.bottom = tile_rect.top - self.foot_offset
        self.y_pos = float(self.rect.y)
        self.velocity_y = 0
        self.is_jumping = False
        self.on_ground = True