import pygame
from objects.slurry import Slurry
from objects.static import StaticHolder


class Divot(Slurry):
    rich = StaticHolder.divot_good_fertility

    def __init__(self, *args):
        super().__init__(*args[:len(StaticHolder.slurry_order)])
        self.color = pygame.Color(StaticHolder.divot_color)
        self.build(StaticHolder.divot_order, args[len(StaticHolder.slurry_order):])

    def get_rich(self, value=1):
        self.components['fertility'] += value

    def is_rich(self):
        if self.components['fertility'] >= self.rich:
            return True
        else:
            return False
