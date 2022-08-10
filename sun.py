from panda3d.core import DirectionalLight
from ursina import Entity

class SunLight(Entity):
    def __init__(self, direction, resolution, car):
        super().__init__()

        self.car = car
        self.resolution = resolution

        self.dlight = DirectionalLight("sun")
        self.dlight.setShadowCaster(True, self.resolution, self.resolution)

        lens = self.dlight.getLens()
        lens.setNearFar(-80, 200)
        lens.setFilmSize((100, 100))

        self.dlnp = render.attachNewNode(self.dlight)
        self.dlnp.lookAt(direction)
        render.setLight(self.dlnp)

    def update(self):
        self.dlnp.setPos(self.car.world_position)

    def update_resolution(self):
        self.dlight.setShadowCaster(True, self.resolution, self.resolution)