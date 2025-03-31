import pygame
import random
from abc import ABC, abstractmethod


class Block(ABC):
    def __init__(self, rotation=0):
        self.rotation = rotation % 360
        self.position = (4, 0)

    @abstractmethod
    def shape(self):
        pass

    @abstractmethod
    def get_asset_path(self):
        pass

    def get_cells(self):
        rel_cells = self.shape()[self.rotation]
        px, py = self.position
        return [(px + x, py + y) for (x, y) in rel_cells]

    def get_image(self):
        return pygame.image.load(self.get_asset_path()).convert_alpha()

    def set_position(self, x, y):
        self.position = (x, y)

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360

    def move_left(self):
        x, y = self.position
        self.position = (x - 1, y)

    def move_right(self):
        x, y = self.position
        self.position = (x + 1, y)

    def move_down(self):
        x, y = self.position
        self.position = (x, y + 1)


class BlockI(Block):
    def shape(self):
        return {
            0: [(0, -1), (0, 0), (0, 1), (0, 2)],
            90: [(-1, 0), (0, 0), (1, 0), (2, 0)],
            180: [(0, -1), (0, 0), (0, 1), (0, 2)],
            270: [(-1, 0), (0, 0), (1, 0), (2, 0)],
        }

    def get_asset_path(self):
        return "assets/blocks/I.png"


class BlockJ(Block):
    def shape(self):
        return {
            0: [(-1, -1), (-1, 0), (0, 0), (1, 0)],
            90: [(1, -1), (0, -1), (0, 0), (0, 1)],
            180: [(-1, 0), (0, 0), (1, 0), (1, 1)],
            270: [(0, -1), (0, 0), (0, 1), (-1, 1)],
        }

    def get_asset_path(self):
        return "assets/blocks/J.png"


class BlockL(Block):
    def shape(self):
        return {
            0: [(1, -1), (-1, 0), (0, 0), (1, 0)],
            90: [(0, -1), (0, 0), (0, 1), (1, 1)],
            180: [(-1, 0), (0, 0), (1, 0), (-1, 1)],
            270: [(-1, -1), (0, -1), (0, 0), (0, 1)],
        }

    def get_asset_path(self):
        return "assets/blocks/L.png"


class BlockO(Block):
    def shape(self):
        return {
            0: [(0, 0), (1, 0), (0, 1), (1, 1)],
            90: [(0, 0), (1, 0), (0, 1), (1, 1)],
            180: [(0, 0), (1, 0), (0, 1), (1, 1)],
            270: [(0, 0), (1, 0), (0, 1), (1, 1)],
        }

    def get_asset_path(self):
        return "assets/blocks/O.png"


class BlockS(Block):
    def shape(self):
        return {
            0: [(1, 0), (0, 0), (0, 1), (-1, 1)],
            90: [(-1, -1), (-1, 0), (0, 0), (0, 1)],
            180: [(1, 0), (0, 0), (0, 1), (-1, 1)],
            270: [(-1, -1), (-1, 0), (0, 0), (0, 1)],
        }

    def get_asset_path(self):
        return "assets/blocks/S.png"


class BlockT(Block):
    def shape(self):
        return {
            0: [(-1, 0), (0, 0), (1, 0), (0, -1)],
            90: [(0, -1), (0, 0), (0, 1), (1, 0)],
            180: [(-1, 0), (0, 0), (1, 0), (0, 1)],
            270: [(0, -1), (0, 0), (0, 1), (-1, 0)],
        }

    def get_asset_path(self):
        return "assets/blocks/T.png"


class BlockZ(Block):
    def shape(self):
        return {
            0: [(-1, 0), (0, 0), (0, 1), (1, 1)],
            90: [(0, -1), (-1, 0), (0, 0), (-1, 1)],
            180: [(-1, 0), (0, 0), (0, 1), (1, 1)],
            270: [(0, -1), (-1, 0), (0, 0), (-1, 1)],
        }

    def get_asset_path(self):
        return "assets/blocks/Z.png"


class BlockFactory:
    BLOCK_TYPES = [BlockI, BlockJ, BlockL, BlockO, BlockS, BlockT, BlockZ]

    @staticmethod
    def create_random_block():
        block_class = random.choice(BlockFactory.BLOCK_TYPES)
        rotation = random.choice([0, 90, 180, 270])
        return block_class(rotation)
