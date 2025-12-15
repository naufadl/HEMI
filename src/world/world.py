import pygame
from src.world.tileset import Tileset
from .tile import Tile

class World:
    def __init__(self):
        self.tiles = []

    def load_simple_level(self, screen_height):
        TILE_SIZE = 16
        SCALE = 2  

        tileset = Tileset(
            "assets/images/tiles/world_tileset.png",
            TILE_SIZE
        )

        TOP_TILE = tileset.get_tile(0, 0, SCALE)     
        BOTTOM_TILE = tileset.get_tile(0, 1, SCALE)  

        ground_y = screen_height - TILE_SIZE * SCALE

        for i in range(32):
            x = i * TILE_SIZE * SCALE

            self.tiles.append(
                Tile(BOTTOM_TILE, x, ground_y + TILE_SIZE * SCALE)
            )

            self.tiles.append(
                Tile(TOP_TILE, x, ground_y)
            )

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)

    def get_collisions(self, rect):
        return [tile for tile in self.tiles if tile.rect.colliderect(rect)]
