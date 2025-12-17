import pygame
from src.world.tileset import Tileset
from src.world.tilemap import Tilemap
from .tile import Tile

class World:
    def __init__(self):
        self.tiles = []
        self.tilemap = None

    def load_tilemap_from_file(self, filepath):
        """Load level dari file"""
        TILE_SIZE = 16
        SCALE = 2
        
        self.tilemap = Tilemap(
            "assets/images/tiles/world_tileset.png",
            TILE_SIZE,
            SCALE
        )
        
        self.tilemap.load_from_file(filepath)
        self.tiles = self.tilemap.tiles


    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)

    def get_collisions(self, rect):
        return [tile for tile in self.tiles if tile.rect.colliderect(rect)]
