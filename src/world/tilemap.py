import pygame
from .tile import Tile
from .tileset import Tileset

class Tilemap:
    def __init__(self, tileset_path, tile_size=16, scale=2):
        self.tileset = Tileset(tileset_path, tile_size)
        self.tile_size = tile_size
        self.scale = scale
        self.tiles = []
        
    def load_from_array(self, tile_array):
        self.tiles.clear()
        
        scaled_size = self.tile_size * self.scale
        
        for row_idx, row in enumerate(tile_array):
            for col_idx, tile_coords in enumerate(row):
                if tile_coords is None:
                    continue
                
                tile_col, tile_row = tile_coords
                
                # Dapatkan image tile dari tileset
                tile_image = self.tileset.get_tile(tile_col, tile_row, self.scale)
                
                # Hitung posisi tile di world
                x = col_idx * scaled_size
                y = row_idx * scaled_size
                
                # Buat tile object
                tile = Tile(tile_image, x, y)
                self.tiles.append(tile)
    
    def load_from_file(self, filepath):
        tile_array = []
        
        with open(filepath, 'r') as f:
            for line in f:
                row = []
                tiles_in_line = line.strip().split()
                
                for tile_str in tiles_in_line:
                    if tile_str == '-':
                        row.append(None)
                    else:
                        col, row_num = map(int, tile_str.split(','))
                        row.append((col, row_num))
                
                tile_array.append(row)
        
        self.load_from_array(tile_array)
    
    def draw(self, surface):
        """Menggambar semua tile"""
        for tile in self.tiles:
            tile.draw(surface)
    
    def get_collisions(self, rect):
        """Mendapatkan tile yang bersinggungan dengan rect"""
        return [tile for tile in self.tiles if tile.rect.colliderect(rect)]