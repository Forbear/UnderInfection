import pygame
import time
from objects.static import StaticHolder
from objects.tree import Tree
from objects.water import Water
from objects.divot import Divot
from objects.area import Area
from objects.corrupted import Corrupted
from numba import jit

SQUIRE_COUNT = 50


class App:
    def __init__(self):
        self.cycle_start_time = self.start_time = time.time()
        self.cycle_time = StaticHolder.cycle_time
        self.redraw_items = []
        self.field = []
        self.forest = []
        self.meadow = []
        self.pond = []
        self.ground = []
        self.fertile = []
        self.cell_size = StaticHolder.squire_size
        self.cycle_count = 0
        self._running = True
        self._display_surf = None
        self.clock = pygame.time.Clock()
        self.size = self.weight, self.height = SQUIRE_COUNT * (self.cell_size + 1) + 1, SQUIRE_COUNT * (self.cell_size + 1) + 1

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        for i in range(SQUIRE_COUNT):
            self.field.append([])
            for j in range(SQUIRE_COUNT):
                self.field[i].append(None)
                self.new_divot(i, j, 'Simple Divot.')

    def field_cell_fill(self, item, x, y):
        self.field[x][y] = item
        self.draw_squire(self.field[x][y].get_color(), x, y)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = [int(x / (self.cell_size + 1)) for x in list(pygame.mouse.get_pos())]
            if 0 <= x < SQUIRE_COUNT and 0 <= y < SQUIRE_COUNT:
                self.on_mouse_click(Water, x, y)
            else:
                print('Cell out of field range.')

    def on_loop(self):
        if time.time() - self.cycle_start_time > self.cycle_time:
            self.cycle_start_time = time.time()
            self.cycle_count += 1
            self.forest_update()
            self.pond_update()
        pass

    def draw_squire(self, color, x, y):
        updated_rect = self.get_rect_by_pos(x, y)
        pygame.draw.rect(self._display_surf, color, updated_rect)

    def on_render(self):
        pygame.display.update()
        self.clock.tick(60)
        pass

    def get_rect_by_pos(self, x, y):
        return pygame.Rect(x * (self.cell_size + 1) + 1, y * (self.cell_size + 1) + 1, self.cell_size, self.cell_size)

    def forest_update(self):
        for (x, y) in self.forest.copy():
            if self.field[x][y].get_age() != Tree.young:
                saturation_area = map(self.get_divots, self.field[x][y].get_surround())
                self.saturation(saturation_area, 'Forest', 1)
            if self.field[x][y].is_dying():
                self.new_divot(x, y, 'Tree wilting.')
            elif self.field[x][y].grow():
                self.draw_squire(self.field[x][y].get_color(), x, y)

    def pond_update(self):
        for (x, y) in self.pond.copy():
            saturation_area = map(self.get_divots, self.field[x][y].get_surround())
            self.saturation(saturation_area, 'Water', 2)

    def define_coast(self):
        pass

    def get_divots(self, items):
        (x, y) = items
        if type(self.field[x][y]) == Divot:
            return items
        else:
            return None

    def get_simple_surround(self, x, y, rad):
        ret_arr = []
        for i in range(-rad, rad + 1):
            if SQUIRE_COUNT > x + i >= 0:
                for j in range(-rad, rad + 1):
                    if SQUIRE_COUNT > y + j >= 0:
                        if i == j == 0:
                            pass
                        else:
                            ret_arr.append((x + i, y + j))
        return ret_arr

    def clear_dependencies(self, x, y):
        if type(self.field[x][y]) == Divot:
            self.ground.pop(self.ground.index((x, y)))
        elif type(self.field[x][y]) == Water:
            self.pond.pop(self.pond.index((x, y)))
        elif type(self.field[x][y]) == Tree:
            self.forest.pop(self.forest.index((x, y)))

    def new_divot(self, x, y, comment):
        self.clear_dependencies(x, y)
        self.field[x][y] = Divot(f'{comment}', 0)
        self.field[x][y].surround = self.get_simple_surround(x, y, StaticHolder.water_influence)
        self.ground.append((x, y))
        self.draw_squire(self.field[x][y].get_color(), x, y)

    def new_tree(self, x, y, comment):
        self.clear_dependencies(x, y)
        self.field[x][y] = Tree(f'{comment} upgrade.', 0, Area.forest, Tree.young)
        self.field[x][y].surround = self.get_simple_surround(x, y, StaticHolder.forest_influence)
        self.forest.append((x, y))
        self.draw_squire(self.field[x][y].get_color(), x, y)

    def new_water(self, x, y, comment):
        self.clear_dependencies(x, y)
        self.field[x][y] = Water(f'{comment}', 0)
        self.field[x][y].surround = self.get_simple_surround(x, y, StaticHolder.water_influence)
        self.pond.append((x, y))
        self.draw_squire(self.field[x][y].get_color(), x, y)

    def saturation(self, area, comment, rich_value):
        for item in area:
            if item is not None:
                (x, y) = item
                if self.field[x][y].is_rich():
                    self.new_tree(x, y, f'{comment} upgrade.')
                else:
                    self.field[x][y].get_rich(rich_value)

    def on_mouse_click(self, obj, x, y):
        if type(self.field[x][y]) == Divot:
            if obj == Tree:
                self.field_cell_fill(Tree("Mouse click.", 0, Area.meadow, Tree.young), x, y)
                self.forest.append((x, y))
            elif obj == Water:
                self.new_water(x, y, 'Mouse click.')
            elif obj == Divot:
                self.field_cell_fill(Divot("Mouse click.", 0), x, y)
                # self.meadow.append((x, y))
            # print(f'Inject {type(self.field[x][y])} at [{x, y}]')

    def on_cleanup(self):
        print(f'Application runtime {time.time() - self.start_time} seconds.')
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    myApp = App()
    myApp.on_execute()
