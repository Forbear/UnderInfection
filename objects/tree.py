import pygame
import random
from objects.slurry import Slurry
from objects.static import StaticHolder


class Tree(Slurry):
    lifetime = StaticHolder.tree_lifetime
    max_lifetime = StaticHolder.tree_life_limit
    young = 'Young'
    middle = 'Middle'
    old = 'Old'

    def __init__(self, *args):
        super().__init__(*args[:len(StaticHolder.slurry_order)])
        self.color = pygame.Color(StaticHolder.young_tree_color)
        self.build(StaticHolder.tree_order, args[len(StaticHolder.slurry_order):])

    def get_lifetime(self):
        return self.components['lifespan']

    def get_plant(self):
        return [self.color, self.get_lifetime()]

    def get_area(self):
        return self.components['area']

    def get_age(self):
        return self.components['age']

    def grow(self):
        self.components['lifespan'] += 1
        if self.get_lifetime() == int(self.lifetime / 3):
            self.color = pygame.Color(StaticHolder.tree_color)
            self.components['age'] = Tree.middle
            return True
        elif self.get_lifetime() == 3 * int(self.lifetime / 3):
            self.color = pygame.Color(StaticHolder.old_tree_color)
            self.components['age'] = Tree.old
            return True
        return False

    def is_dying(self):
        if self.components['lifespan'] >= self.lifetime:
            if self.components['lifespan'] == self.max_lifetime:
                return True
            elif random.randint(0, self.max_lifetime - self.components['lifespan']) == 0:
                return True
        return False
