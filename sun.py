from ursina import *

class SunLight(DirectionalLight):
    def __init__(self, direction, resolution, car, **kwargs):
        super().__init__()

        self.look_at(direction)
        self.shadow_map_resolution = (resolution, resolution)
        self.car = car
        self.lens = self._light.get_lens()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.lens.set_near_far(-80, 20)
        self.lens.set_film_offset((0, 0))
        self.lens.set_film_size((40, 40))

        self.world_position = self.car.world_position 