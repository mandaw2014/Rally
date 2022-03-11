from ursina import *
import numpy

number_of_particles = 50
points = numpy.array([Vec3(0, 0, 0) for i in range(number_of_particles)])
directions = numpy.array([Vec3(random.random(), random.random(), random.random()) * 0.05 for i in range(number_of_particles)])
frames = []

for i in range(200 * 1):
    points += directions
    frames.append(copy(points))

class ParticleSystem(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = Mesh(vertices = points, mode = 'point', static = False, render_points_in_3d = True, thickness = 0.1), t = 0, duration = 1, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.t += time.dt
        if self.t >= self.duration:
            destroy(self)
            return

        self.model.vertices = frames[floor(self.t * 200)]
        self.model.generate()