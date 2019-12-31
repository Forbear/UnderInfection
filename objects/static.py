
class StaticHolder:
    cycle_time = 0.1
    slurry_color = "BISQUE"
    grid_color = "DARKSEAGREEN"
    young_tree_color = "LIGHTGREEN"
    tree_color = "FORESTGREEN"
    old_tree_color = "DARKOLIVEGREEN"
    divot_color = "TAN"
    divot_rich_color = "SADDLEBROWN"
    water_color = "STEELBLUE"
    corrupted_color = "DARKRED"
    tree_lifetime = 42
    tree_life_limit = 60
    slurry_order = ("definition",)
    item_order = ("type", "state")
    item_types = ("clothes", "weapon", "used")
    tree_order = ("lifespan", "area", "age")
    divot_order = ("fertility",)
    divot_good_fertility = 6
    water_order = ("deep",)
    corrupted_order = ("foo",)
    squire_size = 8
    water_influence = 2
    forest_influence = 1
