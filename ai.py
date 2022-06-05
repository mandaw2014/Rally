from ursina import *
from ursina import curve
from particles import ParticleSystem

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class AICar(Entity):
    def __init__(self, car, sand_track, grass_track, snow_track, plains_track):
        super().__init__(
            model = "car.obj",
            position = (0, 0, 0),
            rotation = (0, 0, 0),
            collider = "box",
            scale = (1, 1, 1)
        )

        i = random.randint(0, 5)
        if i == 0:
            self.texture = "car-red.png"
        elif i == 1:
            self.texture = "car-blue.png"
        elif i == 2:
            self.texture = "car-orange.png"
        elif i == 3:
            self.texture = "car-green.png"
        elif i == 4:
            self.texture = "car-white.png"
        elif i == 5:
            self.texture = "car-black.png"

        self.car = car

        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.topspeed = 30
        self.acceleration = 0.35
        self.friction = 0.6
        self.drift_speed = 35
        self.pivot_rotation_distance = 1

        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        self.number_of_particles = 0.05
        self.particle_pivot = Entity()
        self.particle_pivot.parent = self
        self.particle_pivot.position = self.position - (0, 1, 2)

        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.plains_track = plains_track

        self.slope = 100

    def update(self):
        self.pivot.position = self.position

        if self.pivot.rotation_y != self.rotation_y:
            if self.pivot.rotation_y > self.rotation_y:
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
                self.speed += self.pivot_rotation_distance / 4.5 * time.dt
                self.rotation_speed -= 0.1 * time.dt
            if self.pivot.rotation_y < self.rotation_y:
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
                self.speed -= self.pivot_rotation_distance / 4.5 * time.dt
                self.rotation_speed += 2 * time.dt

        if self.pivot.rotation_y - self.rotation_y < -20 or self.pivot.rotation_y - self.rotation_y > 20:
            self.number_of_particles += 1 * time.dt
        else:
            self.number_of_particles -= 2 * time.dt

        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        self.rotation_y += self.rotation_speed * 50 * time.dt

        if self.rotation_speed > 0:
            self.rotation_speed -= self.speed / 6 * time.dt
        elif self.rotation_speed < 0:
            self.rotation_speed += self.speed / 6 * time.dt

        if self.y <= -100:
            if self.grass_track.enabled is True:
                self.position = (-80, -30, 15) + (random.randint(0, 5), 0, random.randint(0, 5))
                self.rotation = (0, 90, 0)
            elif self.sand_track.enabled is True:
                self.position = (0, -40, 4) + (random.randint(0, 5), 0, random.randint(0, 5))
                self.rotation = (0, 65, 0)
            elif self.snow_track.enabled == True:
                self.position = (-5, -35, 90) + (random.randint(0, 5), 0, random.randint(0, 5))
                self.rotation = (0, 90, 0)
            elif self.plains_track.enabled == True:
                self.position = (12, -40, 73) + (random.randint(0, 5), 0, random.randint(0, 5))
                self.rotation = (0, 90, 0)
            else:
                self.position = (0, 0, 0) + (random.randint(0, 5), 0, random.randint(0, 5))
                self.rotation = (0, 0, 0)
            self.speed = 0

        ground_check = raycast(origin = self.position, direction = self.down, distance = 5, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])

        if ground_check.hit:
            r = random.randint(0, 2)
            if r == 0:
                self.speed += self.acceleration * 50 * time.dt

                self.particles = ParticleSystem(position = self.particle_pivot.world_position, rotation_y = random.random() * 360, number_of_particles = self.number_of_particles)
                if self.sand_track.enabled == True:
                    self.particles.texture = "particle_sand_track.png"
                elif self.grass_track.enabled == True:
                    self.particles.texture = "particle_grass_track.png"
                elif self.snow_track.enabled == True:
                    self.particles.texture = "particle_snow_track.png"
                elif self.plains_track.enabled == True:
                    self.particles.texture = "particle_plains_track.png"
                else:
                    self.particles.texture = "particle_sand_track.png"
                self.particles.fade_out(duration = 0.2, delay = 1 - 0.2, curve = curve.linear)
                invoke(self.particles.disable, delay = 1)

        if self.speed != 0:
            r = random.randint(0, 3)
            if r == 1:
                self.rotation_speed -= 20 * time.dt
                self.drift_speed -= 10 * time.dt
            elif r == 2:
                self.rotation_speed += 20 * time.dt
                self.drift_speed -= 10 * time.dt
            else:
                self.drift_speed += 0.01 * time.dt
                if self.rotation_speed > 0:
                    self.rotation_speed -= 5 * time.dt
                elif self.rotation_speed < 0:
                    self.rotation_speed += 5 * time.dt

        if self.speed >= self.topspeed:
            self.speed = self.topspeed
        if self.speed <= 0.1:
            self.speed = 0.1
            self.pivot.rotation = self.rotation

        if self.acceleration >= 0.4:
            self.acceleration = 0.4
        if self.acceleration <= 0.1:
            self.acceleration = 0.1

        if self.drift_speed <= 20:
            self.drift_speed = 20
        if self.drift_speed >= 40:
            self.drift_speed = 40

        if self.rotation_speed >= self.max_rotation_speed:
            self.rotation_speed = self.max_rotation_speed
        if self.rotation_speed <= -self.max_rotation_speed:
            self.rotation_speed = -self.max_rotation_speed

        movementY = self.velocity_y * time.dt
        direction = (0, sign(movementY), 0)

        y_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_y * 1.4 + abs(movementY), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])

        if y_ray.hit:
            self.jump_count = 0
            self.velocity_y = 0
        else:
            self.y += movementY * 50 * time.dt
            self.velocity_y -= 1

        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        if movementX != 0:
            direction = (sign(movementX), 0, 0)
            x_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_x / 2 + abs(movementX), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ], thickness = (1, 1))

            if not x_ray.hit:
                self.x += movementX
            else:
                top_x_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_x / 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])

                if not top_x_ray.hit:
                    self.x += movementX
                    height_ray = raycast(origin = self.world_position + (sign(movementX) * self.scale_x / 2, -self.scale_y / 2, 0), direction = (0, 1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])
                    if height_ray.distance < self.slope * 10:
                        self.y += height_ray.distance

        if movementZ != 0:
            direction = (0, 0, sign(movementZ))
            z_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_z / 2 + abs(movementZ), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ], thickness = (1, 1))

            if not z_ray.hit:
                self.z += movementZ
            else:
                top_z_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_z / 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])

                if not top_z_ray.hit:
                    self.z += movementZ
                    height_ray = raycast(origin = self.world_position + (0, -self.scale_y / 2, sign(movementZ) * self.scale_z / 2), direction = (0, 1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, ])
                    if height_ray.hit:
                        if height_ray.distance < self.slope * 10:
                            self.y += height_ray.distance