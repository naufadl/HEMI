import pygame

class Tileset:
    def __init__(self, image_path, tile_size):
        self.tileset = pygame.image.load('assets/images/tile/world_tileset.png').convert_alpha()
        self.tile_size = tile_size

    def get_tile(self, col, row, scale=1.0):
        rect = pygame.Rect(
            col * self.tile_size,
            row * self.tile_size,
            self.tile_size,
            self.tile_size
        )

        image = self.tileset.subsurface(rect)

        if scale != 1.0:
            image = pygame.transform.scale(
                image,
                (int(self.tile_size * scale), int(self.tile_size * scale))
            )

        return image