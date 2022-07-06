from ursina import *
from ursina import curve
from particles import ParticleSystem

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class AICar(Entity):
    def __init__(self, car, ai_list, sand_track, grass_track, snow_track, forrest_track, savannah_track):
        super().__init__(
            model = "car.obj",
            texture = "car-red.png",
            collider = "box",
            position = (0, 0, 0),
            rotation = (0, 0, 0),
        )

        # Rotation parent
        self.rotation_parent = Entity()

        self.car = car

        # Sets the texture of the car randomly
        self.set_random_texture()

        # Values
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.topspeed = 30
        self.acceleration = 0.35
        self.friction = 0.6
        self.drift_speed = 35
        self.pivot_rotation_distance = 1

        # Pivot for drifting
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        # Particles
        self.number_of_particles = 0.05
        self.particle_pivot = Entity()
        self.particle_pivot.parent = self
        self.particle_pivot.position = self.position - (0, 1, 2)

        # Makes the tracks accessible
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forrest_track = forrest_track
        self.savannah_track = savannah_track

        self.ai_list = ai_list
        self.set_enabled = True
        self.hitting_wall = False

        # Makes sure the AI doesn't get stuck
        self.old_pos = round(self.position)

        # Sand Track Points
        self.sap1 = PathObject((-41, -50, -7), (0, 90, 0))
        self.sap2 = PathObject((-20, -50, -30), (0, 180, 0))
        self.sap3 = PathObject((-48, -47, -55), (0, 270, 0))
        self.sap4 = PathObject((-100, -50, -61), (0, 270, 0))
        self.sap5 = PathObject((-128, -50, -80), (0, 150, 0))
        self.sap6 = PathObject((-100, -50, -115), (0, 70, 0))
        self.sap7 = PathObject((-80, -46, -86), (0, -30, 0))
        self.sap8 = PathObject((-75, -50, -34), (0, 0, 0))

        # Grass Track Points
        self.gp1 = PathObject((-47, -41, 15), (0, 90, 0))
        self.gp2 = PathObject((12, -42, 14), (0, 90, 0))
        self.gp3 = PathObject((48, -42, 34), (0, 0, 0))
        self.gp4 = PathObject((25, -42, 68), (0, -90, 0))
        self.gp5 = PathObject((0, -42, 50), (0, -210, 0))
        self.gp6 = PathObject((2, -42, -25), (0, -180, 0))
        self.gp7 = PathObject((-10, -42, -60), (0, -90, 0))
        self.gp8 = PathObject((-70, -39, -67), (0, -70, 0))
        self.gp9 = PathObject((-105, -42, -26), (0, 00, 0))
        self.gp10 = PathObject((-106, -42, -2), (0, 50, 0))
        self.gp11 = PathObject((-60, -42, 15), (0, 120, 0))

        # Snow Track Points
        self.snp1 = PathObject((32, -44, 94), (0, 90, 0))
        self.snp2 = PathObject((48, -44, 72), (0, 180, 0))
        self.snp3 = PathObject((39, -44, 42), (0, 280, 0))
        self.snp4 = PathObject((-37, -44, 42), (0, 270, 0))
        self.snp5 = PathObject((-73, -43, 25), (0, 180, 0))
        self.snp6 = PathObject((-40, -44, -8), (0, 65, 0))
        self.snp7 = PathObject((20, -44, -8), (0, 90, 0))
        self.snp8 = PathObject((50, -42, -25), (0, 250, 0))
        self.snp9 = PathObject((30, -43, -55), (0, 290, 0))
        self.snp10 = PathObject((5, -44, -51), (0, 290, 0))
        self.snp11 = PathObject((-15, -44, -39), (0, 380, 0))
        self.snp12 = PathObject((-22, -44, 70), (0, 363, 0))
        self.snp13 = PathObject((-21, -44, 106), (0, 340, 0))
        self.snp14 = PathObject((-47, -41, 126), (0, 240, 0))
        self.snp15 = PathObject((-70, -44, 100), (0, 140, 0))
        self.snp16 = PathObject((-30, -44, 90), (0, 90, 0))
        self.snp17 = PathObject((-14, -44, 94), (0, 90, 0))

        # Forrest Track Points
        self.fp1 = PathObject((57, -51, 76), (0, 90, 0))
        self.fp2 = PathObject((82, -51, 63), (0, 180, 0))
        self.fp3 = PathObject((57, -51, 36), (0, 275, 0))
        self.fp4 = PathObject((-29, -51, 36), (0, 270, 0))
        self.fp5 = PathObject((-62, -51, 16), (0, 170, 0))
        self.fp6 = PathObject((-42, -51, -11), (0, 80, 0))
        self.fp7 = PathObject((4, -51, -11), (0, 90, 0))
        self.fp8 = PathObject((41, -51, -40), (0, 180, 0))
        self.fp9 = PathObject((5, -51, -66), (0, 270, 0))
        self.fp10 = PathObject((-17, -51, -53), (0, 360, 0))
        self.fp11 = PathObject((-18, -51, -6), (0, 0, 0))
        self.fp12 = PathObject((-18, -46, 40), (0, 0, 0))
        self.fp13 = PathObject((-3, -51, 75), (0, 120, 0))

        # Savannah Track Points
        self.svp1 = PathObject((28, -51, 40), (0, 90, 0))
        self.svp2 = PathObject((50, -51, 40), (0, 160, 0))
        self.svp3 = PathObject((61, -51, 18), (0, 260, 0))
        self.svp4 = PathObject((-30, -51, -77), (0, 230, 0))
        self.svp5 = PathObject((-64, -51, -50), (0, 390, 0))
        self.svp6 = PathObject((-64, -45, 0), (0, 360, 0))
        self.svp7 = PathObject((-50, -51, 40), (0, 500, 0))
        self.svp8 = PathObject((-24, -51, 41), (0, 450, 0))

        # Path points lists
        self.sand_path = [self.sap1, self.sap2, self.sap3, self.sap4, self.sap5, self.sap6, self.sap7, self.sap8]
        self.grass_path = [self.gp1, self.gp2, self.gp3, self.gp4, self.gp5, self.gp6, self.gp7, self.gp8, self.gp9, self.gp10, self.gp11]
        self.snow_path = [self.snp1, self.snp2, self.snp3, self.snp4, self.snp5, self.snp6, self.snp7, self.snp8, self.snp9, self.snp10, self.snp11, self.snp12, self.snp13, self.snp14, self.snp15, self.snp16, self.snp17]
        self.forrest_path = [self.fp1, self.fp2, self.fp3, self.fp4, self.fp5, self.fp6, self.fp7, self.fp8, self.fp9, self.fp10, self.fp11, self.fp12, self.fp13]
        self.savannah_path = [self.svp1, self.svp2, self.svp3, self.svp4, self.svp5, self.svp6, self.svp7, self.svp8]

        # The next point the ai is going to
        self.next_path = self.gp1

        # The speed of the AI
        self.difficulty = 50

        invoke(self.same_pos, delay = 5)

        self.disable()

    def set_random_texture(self):
        """
        Sets a random car colour
        """
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

    def same_pos(self):
        """
        Checks if the AI is in the same position. If it is, it moved it randomly in
        a certain direction. This stops the AI from getting stuck on things.
        """
        if self.enabled:
            distance = sqrt((self.position[0] - self.old_pos[0]) ** 2 + (self.position[1] - self.old_pos[1]) ** 2 + (self.position[2] - self.old_pos[2]) ** 2)
            if distance <= 2:
                self.x += random.randint(-10, 10) * time.dt
                self.y += 40 * time.dt
                self.z += random.randint(-10, 10) * time.dt
            self.old_pos = round(self.position)
        invoke(self.same_pos, delay = 1)

    def update(self):
        # Drifting
        self.pivot.position = self.position
        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

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

        if self.sand_track.enabled or self.grass_track.enabled:
            self.difficulty = 60
        elif self.snow_track.enabled or self.forrest_track.enabled:
            self.difficulty = 40

        """
        Rotation
        """
        # Set the position of the rotation parent to the car's position
        self.rotation_parent.position = self.position

        # Lerps the car's rotation to the rotation parent's rotation (Makes it smoother)
        self.rotation_x = lerp(self.rotation_x, self.rotation_parent.rotation_x, 20 * time.dt)
        self.rotation_z = lerp(self.rotation_z, self.rotation_parent.rotation_z, 20 * time.dt)

        # Gravity
        movementY = self.velocity_y * time.dt

        # Main raycast for collision
        y_ray = raycast(origin = self.world_position, direction = (0, -1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, self.forrest_track.finish_line, self.forrest_track.wall_trigger, self.savannah_track.finish_line, self.savannah_track.wall_trigger, ])

        if y_ray.distance <= 4:
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
                elif self.forrest_track.enabled == True:
                    self.particles.texture = "particle_forrest_track.png"
                else:
                    self.particles.texture = "particle_sand_track.png"
                self.particles.fade_out(duration = 0.2, delay = 1 - 0.2, curve = curve.linear)
                invoke(self.particles.destroy, delay = 1)

        # Main AI bit
        # If the ai's rotation y does not equal the next paths rotation, change it
        if self.next_path.rotation_y > self.rotation_y:
            self.rotation_y += 80 * time.dt
        elif self.next_path.rotation_y < self.rotation_y:
            self.rotation_y -= 80 * time.dt

        """
        If the distance between the next path point and the ai is less than 12, 
        change the path point to be the next point in the list
        """
        if self.sand_track.enabled:
            for p in self.sand_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.sand_path[self.sand_path.index(p) - len(self.sand_path) + 1]
        elif self.grass_track.enabled:
            for p in self.grass_path:
                if distance(p, self) < 14 and self.next_path == p:
                    self.next_path = self.grass_path[self.grass_path.index(p) - len(self.grass_path) + 1]
        elif self.snow_track.enabled:
            for p in self.snow_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.snow_path[self.snow_path.index(p) - len(self.snow_path) + 1]
        elif self.forrest_track.enabled:
            if distance(self.fp10, self) < 12:
                self.rotation_y = 0
                self.pivot.rotation_y = self.rotation_y
            for p in self.forrest_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.forrest_path[self.forrest_path.index(p) - len(self.forrest_path) + 1]
        elif self.savannah_track.enabled:
            if distance(self.svp4, self) < 10:
                self.speed -= 10 * time.dt
            if distance(self.svp8, self) < 12:
                self.rotation_y = 90
                self.pivot.rotation_y = self.rotation_y
            for p in self.savannah_path:
                if distance(p, self) < 15 and self.next_path == p:
                    self.next_path = self.savannah_path[self.savannah_path.index(p) - len(self.savannah_path) + 1]

        # Cap the speed
        if self.speed >= self.topspeed:
            self.speed = self.topspeed
        if self.speed <= 0.1:
            self.speed = 0.1
            self.pivot.rotation = self.rotation

        # Cap the drifting
        if self.drift_speed <= 20:
            self.drift_speed = 20
        if self.drift_speed >= 40:
            self.drift_speed = 40
        
        # If the AI is below -100, reset the position
        if self.y <= -100:
            self.reset()

        # If the AI is above 100, reset the position
        if self.y >= 100:
            self.reset()

        if y_ray.distance <= self.scale_y * 1.7 + abs(movementY):
            self.velocity_y = 0
            # Check if hitting a wall or steep slope
            if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                # Set the y value to the ground's y value
                self.y = y_ray.world_point.y + 1.4
                self.hitting_wall = False
            else:
                self.hitting_wall = True

            if not self.hitting_wall:
                self.rotation_parent.look_at(self.position + y_ray.world_normal, axis = "up")
                self.rotation_parent.rotate((0, self.rotation_y + 180, 0))
            else:
                self.rotation_parent.rotation = self.rotation
        else:
            self.y += movementY * 50 * time.dt
            self.velocity_y -= 50 * time.dt
            self.rotation_parent.rotation = self.rotation

        # Movement
        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        if movementX != 0:
            self.x += movementX
        if movementZ != 0:
            self.z += movementZ

    def reset(self):
        if self.grass_track.enabled == True:
            self.position = (-80 + random.randint(-5, 5), -30 + random.randint(-3, 5), 15 + random.randint(-5, 5))
            self.rotation = (0, 90, 0)
            self.next_path = self.gp1
        elif self.sand_track.enabled == True:
            self.position = (-63 + random.randint(-5, 5), -40 + random.randint(-3, 5), -7 + random.randint(-5, 5))
            self.rotation = (0, 65, 0)
            self.next_path = self.sap1
        elif self.snow_track.enabled == True:
            self.position = (-5 + random.randint(-5, 5), -35 + random.randint(-3, 5), 90 + random.randint(-5, 5))
            self.rotation = (0, 90, 0)
            self.next_path = self.snp1
        elif self.forrest_track.enabled == True:
            self.position = (12 + random.randint(-5, 5), -40 + random.randint(-3, 5), 73 + random.randint(-5, 5))
            self.rotation = (0, 90, 0)
            self.next_path = self.fp1
        else:
            self.position = (0, 0, 0)
            self.rotation = (0, 0, 0)
        self.speed = 0
        self.velocity_y = 0

# Path Point class
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