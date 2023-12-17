import pygame

class Map_1:
    def __init__(self, screen):
        self.screen = screen

    def render(self):
        pass

    def create_board(self):
        self.width = 3
        self.height = 3
        self.board = [[0] * self.width for _ in range(self.height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 144
        for x in range(0, self.width):
            for y in range(0, self.height):
                pygame.draw.rect(self.screen, 'white', (x * self.cell_size, y * self.cell_size,
                                                        self.cell_size, self.cell_size), 1)