from objects.slurry import Slurry
from objects.static import StaticHolder


class Item(Slurry):
    def __init__(self, *args):
        super().__init__(*args[:len(StaticHolder.slurry_order)])
        self.build(StaticHolder.item_order, args[len(StaticHolder.slurry_order):])


if __name__ == "__main__":
    test_item = Item(1, {}, 'Stick', "Mace", "Some state")
    print(test_item.get_params())
    print(test_item.get_definition())
    print(test_item.get_all())
