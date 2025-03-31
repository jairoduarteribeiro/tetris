import pygame


class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def is_cell_occupied(self, x, y):
        if x < 0 or x >= self.width or y >= self.height:
            return True
        if y < 0:
            return False
        return self.grid[y][x] is not None

    def collides(self, block):
        for x, y in block.get_cells():
            if self.is_cell_occupied(x, y):
                return True
        return False

    def fix_block(self, block):
        image = block.get_image()
        for x, y in block.get_cells():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = image

    def render(self, surface, origin, cell_size, scale=1.0):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell:
                    scaled = pygame.transform.scale(
                        cell, (int(cell_size * scale), int(cell_size * scale))
                    )
                    pixel_x = origin[0] + x * cell_size * scale
                    pixel_y = origin[1] + y * cell_size * scale
                    surface.blit(scaled, (pixel_x, pixel_y))
