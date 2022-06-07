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

        self.car = car

        self.set_random_texture()

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

        self.ai_list = None

        self.old_pos = round(self.position)
        
        self.slope = 100

        # Sand Track Points

        self.sap1 = PathObject((-41, -50, -7))
        self.sap2 = PathObject((-26, -50, -25), (0, 90, 0))
        self.sap3 = PathObject((-26, -50, -42), (0, 90, 0))
        self.sap4 = PathObject((-48, -47, -55))
        self.sap5 = PathObject((-100, -50, -61))
        self.sap6 = PathObject((-128, -50, -95), (0, 90, 0))
        self.sap7 = PathObject((-105, -50, -105))
        self.sap8 = PathObject((-91, -50, -105))
        self.sap9 = PathObject((-80, -46, -86), (0, 90, 0))
        self.sap10 = PathObject((-75, -50, -34), (0, 90, 0))
        self.sap11 = PathObject((-54, -50, -15))

        # Grass Track Points

        self.gp1 = PathObject((-47, -41, 15))
        self.gp2 = PathObject((12, -42, 14))
        self.gp3 = PathObject((48, -42, 34), (0, 90, 0))
        self.gp4 = PathObject((37, -42, 68))
        self.gp5 = PathObject((10, -42, 60), (0, 0, 0))
        self.gp6 = PathObject((-2, -42, -10), (0, 90, 0))
        self.gp7 = PathObject((3, -42, -40), (0, 90, 0))
        self.gp8 = PathObject((-13, -42, -63))
        self.gp9 = PathObject((-38, -42, -67))
        self.gp10 = PathObject((-94, -39, -57))
        self.gp11 = PathObject((-105, -42, -26), (0, 90, 0))
        self.gp12 = PathObject((-106, -42, -2), (0, 90, 0))
        self.gp13 = PathObject((-90, -42, 15))

        # Snow Track Points

        self.snp1 = PathObject((32, -44, 94))
        self.snp2 = PathObject((48, -44, 78), (0, 90, 0))
        self.snp3 = PathObject((53, -44, 65), (0, 90, 0))
        self.snp4 = PathObject((39, -44, 42))
        self.snp5 = PathObject((-37, -44, 42))
        self.snp6 = PathObject((-73, -43, 35), (0, 90, 0))
        self.snp7 = PathObject((-76, -42, 2), (0, 90, 0))
        self.snp8 = PathObject((-67, -44, -8))
        self.snp9 = PathObject((47, -44, -8))
        self.snp10 = PathObject((65, -42, -27), (0, 90, 0))
        self.snp11 = PathObject((52, -43, -46))
        self.snp12 = PathObject((5, -44, -51))
        self.snp13 = PathObject((-25, -44, -39), (0, 90, 0))
        self.snp14 = PathObject((-22, -44, 50), (0, 90, 0))
        self.snp15 = PathObject((-21, -44, 106), (0, 90, 0))
        self.snp16 = PathObject((-47, -41, 126))
        self.snp17 = PathObject((-70, -44, 100), (0, 90, 0))
        self.snp18 = PathObject((-55, -44, 85))
        self.snp19 = PathObject((-14, -44, 94))

        # Plains Track Points

        self.plp1 = PathObject((57, -51, 76))
        self.plp2 = PathObject((82, -51, 63), (0, 90, 0))
        self.plp3 = PathObject((80, -51, 52), (0, 90, 0))
        self.plp4 = PathObject((57, -51, 36))
        self.plp5 = PathObject((-29, -51, 36))
        self.plp6 = PathObject((-62, -51, 16), (0, 90, 0))
        self.plp7 = PathObject((-42, -51, -11))
        self.plp8 = PathObject((4, -51, -11))
        self.plp9 = PathObject((41, -51, -25), (0, 90, 0))
        self.plp10 = PathObject((41, -51, -46), (0, 90, 0))
        self.plp11 = PathObject((25, -51, -66))
        self.plp12 = PathObject((7, -51, -67))
        self.plp13 = PathObject((-17, -51, -53), (0, 90, 0))
        self.plp14 = PathObject((-18, -51, -6), (0, 90, 0))
        self.plp15 = PathObject((-18, -46, 24), (0, 90, 0))
        self.plp16 = PathObject((-3, -51, 75))

        self.sand_path = [self.sap1, self.sap2, self.sap3, self.sap4, self.sap5, self.sap6, self.sap7, self.sap8, self.sap9, self.sap10, self.sap11]
        self.grass_path = [self.gp1, self.gp2, self.gp3, self.gp4, self.gp5, self.gp6, self.gp7, self.gp8, self.gp9, self.gp10, self.gp11, self.gp12, self.gp13]
        self.snow_path = [self.snp1, self.snp2, self.snp3, self.snp4, self.snp5, self.snp6, self.snp7, self.snp8, self.snp9, self.snp10, self.snp11, self.snp12, self.snp13, self.snp14, self.snp15, self.snp16, self.snp17, self.snp18, self.snp19]
        self.plains_path = [self.plp1, self.plp2, self.plp3, self.plp4, self.plp5, self.plp6, self.plp7, self.plp8, self.plp9, self.plp10, self.plp11, self.plp12, self.plp13, self.plp14, self.plp15, self.plp16]

        self.next_path = self.gp1
        self.difficulty = 70

        invoke(self.same_pos, delay = 5)

    def set_random_texture(self):
        i = random.randint(0, 5)
        if i == 0:
            if self.car.texture != "car-red.png":
                self.texture = "car-red.png"
        elif i == 1:
            if self.car.texture != "car-blue.png":
                self.texture = "car-blue.png"
        elif i == 2:
            if self.car.texture != "car-orange.png":
                self.texture = "car-orange.png"
        elif i == 3:
            if self.car.texture != "car-green.png":
                self.texture = "car-green.png"
        elif i == 4:
            if self.car.texture != "car-white.png":
                self.texture = "car-white.png"
        elif i == 5:
            if self.car.texture != "car-black.png":
                self.texture = "car-black.png"

    def same_pos(self):
        if self.enabled:
            distance = sqrt((self.position[0] - self.old_pos[0]) ** 2 + (self.position[1] - self.old_pos[1]) ** 2 + (self.position[2] - self.old_pos[2]) ** 2)
            if distance <= 2:
                self.x += random.randint(-10, 10) * time.dt
                self.y += 40 * time.dt
                self.z += random.randint(-10, 10) * time.dt
            self.old_pos = round(self.position)
        invoke(self.same_pos, delay = 2)

    def update(self):
        self.pivot.position = self.position

        if self.pivot.rotation_y != self.rotation_y:
            if self.pivot.rotation_y > self.rotation_y:
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
                self.speed += self.pivot_rotation_distance / 4.5 * time.dt
            if self.pivot.rotation_y < self.rotation_y:
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
                self.speed -= self.pivot_rotation_distance / 4.5 * time.dt

        if self.pivot.rotation_y - self.rotation_y < -20 or self.pivot.rotation_y - self.rotation_y > 20:
            self.number_of_particles += 1 * time.dt
        else:
            self.number_of_particles -= 2 * time.dt

        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        if self.sand_track.enabled or self.sand_track.enabled:
            self.difficulty = 70
        elif self.snow_track.enabled or self.plains_track.enabled:
            self.difficulty = 50

        ground_check = raycast(origin = self.position, direction = self.down, distance = 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ])
        
        if ground_check.hit:
            r = random.randint(0, 1)
            if r == 0:
                self.speed += self.acceleration * self.difficulty * time.dt

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

        # Main AI bit
        if self.sand_track.enabled:
            self.look_at(self.next_path)
            for p in self.sand_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.sand_path[self.sand_path.index(p) - len(self.sand_path) + 1]
        elif self.grass_track.enabled:
            self.look_at(self.next_path)
            for p in self.grass_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.grass_path[self.grass_path.index(p) - len(self.grass_path) + 1]
        elif self.snow_track.enabled:
            self.look_at(self.next_path)
            for p in self.snow_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.snow_path[self.snow_path.index(p) - len(self.snow_path) + 1]
        elif self.plains_track.enabled:
            self.look_at(self.next_path)
            for p in self.plains_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.plains_path[self.plains_path.index(p) - len(self.plains_path) + 1]
        else:
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

        if self.drift_speed <= 20:
            self.drift_speed = 20
        if self.drift_speed >= 40:
            self.drift_speed = 40

        movementY = self.velocity_y * time.dt
        direction = (0, sign(movementY), 0)

        y_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_y * 1.4 + abs(movementY), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ])

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
            x_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_x / 2 + abs(movementX), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ], thickness = (1, 1))

            if not x_ray.hit:
                self.x += movementX
            else:
                top_x_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_x / 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ])

                if not top_x_ray.hit:
                    self.x += movementX
                    height_ray = raycast(origin = self.world_position + (sign(movementX) * self.scale_x / 2, -self.scale_y / 2, 0), direction = (0, 1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ])
                    if height_ray.hit and y_ray.hit:
                        if height_ray.distance < self.slope * 10:
                            if height_ray.entity != self.ai_list[0] or height_ray.entity != self.ai_list[1] or height_ray.entity != self.ai_list[2]:
                                self.y += height_ray.distance

        if movementZ != 0:
            direction = (0, 0, sign(movementZ))
            z_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_z / 2 + abs(movementZ), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ], thickness = (1, 1))

            if not z_ray.hit:
                self.z += movementZ
            else:
                top_z_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_z / 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ])

                if not top_z_ray.hit:
                    self.z += movementZ
                    height_ray = raycast(origin = self.world_position + (0, -self.scale_y / 2, sign(movementZ) * self.scale_z / 2), direction = (0, 1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.plains_track.finish_line, self.plains_track.wall_trigger, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.plains_track.wall1, self.plains_track.wall2, self.plains_track.wall3, self.plains_track.wall4, self.plains_track.wall5, self.plains_track.wall6, self.plains_track.wall7, self.plains_track.wall8, ])
                    if height_ray.hit and y_ray.hit:
                        if height_ray.distance < self.slope * 10:
                            if height_ray.entity != self.ai_list[0] or height_ray.entity != self.ai_list[1] or height_ray.entity != self.ai_list[2]:
                                self.y += height_ray.distance

class PathObject(Entity):
    def __init__(self, position = (0, 0, 0), rotation = (0, 0, 0)):
        super().__init__(
            model = "cube",
            position = position,
            rotation = rotation,
            texture = "white_cube",
            scale = (1, 20, 20),
            visible = False,
            alpha = 50,
        )