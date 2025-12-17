class Tile:
    def __init__(self, image, x, y, tile_coords=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tile_coords = tile_coords  # Simpan koordinat tile (col, row)
        
        # Cek apakah ini death tile
        self.is_deadly = (tile_coords == (4, 11)) if tile_coords else False
        # Cek apakah ini goal tile
        self.is_goal = (tile_coords == (4, 8)) if tile_coords else False

    def draw(self, surface):
        surface.blit(self.image, self.rect)