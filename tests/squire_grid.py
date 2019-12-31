import random
import pygame
from objects.static import StaticHolder


class Squire:
    def __init__(self, count):
        self.squires = []
        self.color = pygame.Color(StaticHolder.grid_color)
        self._init_squires(count)

    def _init_squires(self, count):
        x = StaticHolder.squire_size
        for i in range(count):
            self.squires.append([])
            for j in range(count):
                self.squires[i].append([self.color, pygame.Rect((i * (x + 1) + 1, j * (x + 1) + 1), (x, x))])

    def pop_possible(self):
        if len(self.squires) > 0:
            return True
        else:
            return False

    def get_squires(self):
        return self.squires

    def pop_random_squire(self):
        if self.pop_possible():
            col = random.randint(0, len(self.squires) - 1)
            ret_value = self.squires[col].pop(random.randint(0, len(self.squires[col]) - 1))
            if len(self.squires[col]) == 0:
                self.squires.pop(col)
            return ret_value

    def pop_squire(self, col, row):
        if len(self.squires[col] > 0):
            return self.squires[col][row].pop()

    def get_place(self, col, row):
        if len(self.squires) - 1 >= col > 0:
            if len(self.squires[col]) - 1 >= row > 0:
                return self.squires[col][row][1]
            else:
                print('Row value is out of range.')
        else:
            print('Column value is out of range.')

    def disable_squires(self, row, col):
        for i in row:
            for j in col:
                self.squires[i][j][0] = pygame.Color("BLACK")

    def inject(self, item, col, row):
        if len(self.squires) - 1 >= col > 0:
            if len(self.squires[col]) - 1 >= row > 0:
                self.squires[col][row] = item
