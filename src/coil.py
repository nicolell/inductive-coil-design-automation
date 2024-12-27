from coil_util import *

class Coil:

    def __init__(self, diameter=5, spacing=1.27, size=1.27, turns=5, layers=['F.Cu', 'B.Cu'], drill=0.5, adhere_strictly=True, x=100, y=100) -> None:
        self.text = initialize_file()
        self.diameter = diameter
        self.spacing = spacing
        self.size = size
        self.turns = turns
        self.layers = layers
        self.lines = []
        self.drill = drill
        self.adhere_strictly = adhere_strictly
        self.x = x
        self.y = y

    def make_full_turns(self, start_x, start_y):
        pass

    def make_partial_turns(self):
        pass

    def create_coil(self):
        pass
