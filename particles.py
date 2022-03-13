from ursina import *
import numpy

class ParticleSystem(Entity):
    def __init__(self, **kwargs):
        super().__init__(t = 0, duration = 1, **kwargs)

        self.number_of_particles = 1
        self.points = numpy.array([Vec3(0, 0, 0) for i in range(self.number_of_particles)])
        self.directions = numpy.array([Vec3(random.random(), random.random(), random.random()) * 0.05 for i in range(self.number_of_particles)])
        self.frames = []

        self.model = Mesh(vertices = self.points, mode = "point", static = False, render_points_in_3d = True, thickness = 0.1)

        for i in range(200 * 1):
            self.points += self.directions
            self.frames.append(copy(self.points))

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.t += time.dt
        if self.t >= self.duration:
            destroy(self)
            return

        self.model.vertices = self.frames[floor(self.t * 100)]
        self.model.generate()