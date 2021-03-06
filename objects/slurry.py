import sys
import pygame
from objects.static import StaticHolder


class Slurry:
    def __init__(self, *args):
        self.components = {}
        self.color = pygame.Color(StaticHolder.slurry_color)
        self.build(StaticHolder.slurry_order, args)
        self.surround = []

    def build(self, order, pieces):
        if len(order) != len(pieces):
            print(str(self.__class__) + " params number exception.")
            sys.exit(1)
        for i, component in enumerate(order):
            self.components[component] = pieces[i]

    def get_field_by_id(self, index):
        if len(self.components) - 1 >= index:
            return self.components[index]

    def get_all(self):
        return self.components

    def get_color(self):
        return self.color

    def get_surround(self):
        return self.surround

    def less_surround(self, x, y):
        self.surround.pop(self.surround.index((x, y)))

    def more_surround(self, x, y):
        self.surround.append((x, y))


if __name__ == "__main__":
    test_slurry = Slurry("Slurry")
    # print(test_slurry.get_id())
    # print(test_slurry.get_definition())
    print(test_slurry.get_all())
    # wrongSlurry = Slurry()
