from ursina import *

class Particles(Entity):
    def __init__(self, position, rotation_y, number_of_particles):
        super().__init__(
            model = "particles.obj", 
            scale = 0.1,
            position = position,
            rotation_y = rotation_y,
        )

        self.number_of_particles = number_of_particles
        if self.number_of_particles >= 0.1:
            self.number_of_particles = 0.1
        elif self.number_of_particles <= 0.05:
            self.number_of_particles = 0.05
        self.direction = Vec3(random.random(), random.random(), random.random()) * self.number_of_particles

    def update(self):
        self.position += self.direction * 120 * time.dt

        if self.number_of_particles >= 0.1:
            self.number_of_particles = 0.1
        elif self.number_of_particles <= 0.05:
            self.number_of_particles = 0.05

# class Smoke(Entity):
#     def __init__(self, position, rotation_y, amount_of_smoke):
#         super().__init__(
#             model = "smoke.obj",
#             texture = "smoke.png", 
#             scale = 3,
#             position = position,
#             rotation_y = rotation_y,
#         )

#         self.amount_of_smoke = amount_of_smoke
#         if self.amount_of_smoke >= 0.1:
#             self.amount_of_smoke = 0.1
#         elif self.amount_of_smoke <= 0.05:
#             self.amount_of_smoke = 0.05
#         self.direction = Vec3(random.random(), random.random(), random.random()) * self.amount_of_smoke

#     def update(self):
#         self.position += self.direction * 120 * time.dt

#         if self.amount_of_smoke >= 0.1:
#             self.amount_of_smoke = 0.1
#         elif self.amount_of_smoke <= 0.05:
#             self.amount_of_smoke = 0.05

class TrailRenderer(Entity):
    def __init__(self, thickness = 10, length = 6, **kwargs):
        super().__init__(**kwargs)
        self.thickness = thickness
        self.length = length

        self.renderer = Entity(model = Mesh(
            vertices = [self.world_position for i in range(length)],
            mode = "line",
            thickness = thickness,
            static = False
        ), color = color.rgba(10, 10, 10, 90))

        self._t = 0
        self.update_step = 0.025

    def update(self):
        self._t += time.dt
        if self._t >= self.update_step:
            self._t = 0
            self.renderer.model.vertices.pop(0)
            self.renderer.model.vertices.append(self.world_position)
            self.renderer.model.generate()