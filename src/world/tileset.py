import pygame

class Tileset:
    def __init__(self, image_path, tile_size):
        # Load tileset image
        self.tileset = pygame.image.load('assets/images/tile/world_tileset.png').convert_alpha()
        self.tile_size = tile_size

    # Buat rectangle untuk crop area di tileset
    def get_tile(self, col, row, scale=1.0):
        rect = pygame.Rect(
            col * self.tile_size,
            row * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        # Crop tile dari tileset
        image = self.tileset.subsurface(rect)
        # Scale tile
        if scale != 1.0:
            image = pygame.transform.scale(
                image,
                (int(self.tile_size * scale), int(self.tile_size * scale))
            )

        return image