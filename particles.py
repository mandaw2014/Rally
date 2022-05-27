from ursina import *

class ParticleSystem(Entity):
    def __init__(self, position, rotation_y):
        super().__init__(
            model = "particles.obj", 
            scale = 0.1,
            position = position,
            rotation_y = rotation_y,
            t = 0,
            duration = 1
        )

        self.direction = Vec3(random.random(), random.random(), random.random()) * 0.05

    def update(self):
        self.t += time.dt
        if self.t >= self.duration:
            destroy(self)
            return

        self.position += self.direction * 120 * time.dt