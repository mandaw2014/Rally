from ursina import *

class ParticleSystem(Entity):
    def __init__(self, position, rotation_y, number_of_particles):
        super().__init__(
            model = "particles.obj", 
            scale = 0.1,
            position = position,
            rotation_y = rotation_y,
            t = 0,
            duration = 1
        )

        self.number_of_particles = number_of_particles
        if self.number_of_particles >= 0.1:
            self.number_of_particles = 0.1
        elif self.number_of_particles <= 0.05:
            self.number_of_particles = 0.05
        self.direction = Vec3(random.random(), random.random(), random.random()) * self.number_of_particles

    def update(self):
        self.t += time.dt
        if self.t >= self.duration:
            destroy(self)
            return

        self.position += self.direction * 120 * time.dt

        if self.number_of_particles >= 0.1:
            self.number_of_particles = 0.1
        elif self.number_of_particles <= 0.05:
            self.number_of_particles = 0.05

    def destroy(self):
        destroy(self)