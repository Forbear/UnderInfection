import pygame
from objects.slurry import Slurry
from objects.static import StaticHolder


class Corrupted(Slurry):
    def __init__(self, *args):
        super().__init__(*args[:len(StaticHolder.slurry_order)])
        self.color = pygame.Color(StaticHolder.corrupted_color)
        self.build(StaticHolder.corrupted_order, args[len(StaticHolder.corrupted_order):])
