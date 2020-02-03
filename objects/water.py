import pygame
from objects.slurry import Slurry
from objects.static import StaticHolder


class Water(Slurry):
    def __init__(self, *args):
        super().__init__(*args[:len(StaticHolder.slurry_order)])
        self.color = pygame.Color(StaticHolder.water_color)
        self.build(StaticHolder.water_order, args[len(StaticHolder.slurry_order):])

