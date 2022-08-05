from panda3d.core import DirectionalLight
from ursina import Entity

class SunLight(Entity):
    def __init__(self, direction, resolution, car):
        super().__init__()

        self.car = car

        dlight = DirectionalLight("sun")
        dlight.setShadowCaster(True, resolution, resolution)

        lens = dlight.getLens()
        lens.setNearFar(-80, 200)
        lens.setFilmSize((100, 100))

        self.dlnp = render.attachNewNode(dlight)
        self.dlnp.lookAt(direction)
        render.setLight(self.dlnp)

    def update(self):
        self.dlnp.setPos(self.car.world_position)