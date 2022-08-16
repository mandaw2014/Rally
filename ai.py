from ursina import *
from particles import Particles

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class AICar(Entity):
    def __init__(self, car, ai_list, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track):
        super().__init__(
            model = "sports-car.obj",
            texture = "sports-red.png",
            collider = "box",
            position = (0, 0, 0),
            rotation = (0, 0, 0),
        )

        # Rotation parent
        self.rotation_parent = Entity()

        self.car = car
        self.car_type = "sports"

        # Sets the car and texture of the car randomly
        self.set_random_car()
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
        self.particle_time = 0
        self.particle_amount = 0.125 # The lower, the more
        self.particle_pivot = Entity(parent = self)
        self.particle_pivot.position = (0, -1, -2)

        # Makes the tracks accessible
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forest_track = forest_track
        self.savannah_track = savannah_track
        self.lake_track = lake_track

        self.current_track = self.sand_track

        self.tracks = [self.sand_track, self.grass_track, self.snow_track, self.forest_track, self.savannah_track, self.lake_track]

        self.ai_list = ai_list
        self.set_enabled = True
        self.hitting_wall = False

        self.t = 0
        self.update_step = 0.05

        # Collision raycast
        self.y_ray = raycast(origin = self.world_position, direction = (0, -1, 0), traverse_target = self.current_track, ignore = [self, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.forest_track.wall1, self.forest_track.wall2, self.forest_track.wall3, self.forest_track.wall4, self.forest_track.wall1, self.forest_track.wall2, self.forest_track.wall3, self.forest_track.wall4, ])

        # Makes sure the AI doesn't get stuck
        self.old_pos = round(self.position)

        # Sand Track Points
        self.sap1 = PathObject((-41, -50, -7), 90)
        self.sap2 = PathObject((-20, -50, -30), 180)
        self.sap3 = PathObject((-48, -47, -55), 270)
        self.sap4 = PathObject((-100, -50, -61), 270)
        self.sap5 = PathObject((-128, -50, -80), 150)
        self.sap6 = PathObject((-100, -50, -115), 70)
        self.sap7 = PathObject((-80, -46, -86), -30)
        self.sap8 = PathObject((-75, -50, -34), 0)

        # Grass Track Points
        self.gp1 = PathObject((-47, -41, 15), 90)
        self.gp2 = PathObject((12, -42, 14), 90)
        self.gp3 = PathObject((48, -42, 34), 0)
        self.gp4 = PathObject((25, -42, 68), -90)
        self.gp5 = PathObject((0, -42, 50), -210)
        self.gp6 = PathObject((2, -42, -25), -180)
        self.gp7 = PathObject((-10, -42, -60), -90)
        self.gp8 = PathObject((-70, -39, -67), -70)
        self.gp9 = PathObject((-105, -42, -26), 00)
        self.gp10 = PathObject((-106, -42, -2), 50)
        self.gp11 = PathObject((-60, -42, 15), 120)

        # Snow Track Points
        self.snp1 = PathObject((32, -44, 94), 90)
        self.snp2 = PathObject((48, -44, 72), 180)
        self.snp3 = PathObject((39, -44, 42), 280)
        self.snp4 = PathObject((-37, -44, 42), 270)
        self.snp5 = PathObject((-73, -43, 25), 180)
        self.snp6 = PathObject((-40, -44, -8), 65)
        self.snp7 = PathObject((20, -44, -8), 90)
        self.snp8 = PathObject((50, -42, -25), 250)
        self.snp9 = PathObject((30, -43, -55), 290)
        self.snp10 = PathObject((5, -44, -51), 290)
        self.snp11 = PathObject((-15, -44, -39), 380)
        self.snp12 = PathObject((-22, -44, 70), 363)
        self.snp13 = PathObject((-21, -44, 106), 340)
        self.snp14 = PathObject((-47, -41, 126), 240)
        self.snp15 = PathObject((-70, -44, 100), 140)
        self.snp16 = PathObject((-30, -44, 90), 90)
        self.snp17 = PathObject((-14, -44, 94), 90)

        # Forrest Track Points
        self.fp1 = PathObject((57, -51, 76), 90)
        self.fp2 = PathObject((82, -51, 63), 180)
        self.fp3 = PathObject((57, -51, 36), 275)
        self.fp4 = PathObject((-29, -51, 36), 270)
        self.fp5 = PathObject((-62, -51, 16), 170)
        self.fp6 = PathObject((-42, -51, -11), 80)
        self.fp7 = PathObject((4, -51, -11), 90)
        self.fp8 = PathObject((41, -51, -40), 180)
        self.fp9 = PathObject((5, -51, -66), 270)
        self.fp10 = PathObject((-17, -51, -53), 360)
        self.fp11 = PathObject((-18, -51, -6), 0)
        self.fp12 = PathObject((-18, -46, 40), 0)
        self.fp13 = PathObject((-3, -51, 75), 120)

        # Savannah Track Points
        self.svp1 = PathObject((28, -51, 40), 90)
        self.svp2 = PathObject((50, -51, 40), 160)
        self.svp3 = PathObject((61, -51, 18), 260)
        self.svp4 = PathObject((-30, -51, -77), 230)
        self.svp5 = PathObject((-64, -51, -50), 390)
        self.svp6 = PathObject((-64, -45, 0), 360)
        self.svp7 = PathObject((-50, -51, 40), 500)
        self.svp8 = PathObject((-24, -51, 41), 450)

        # Lake Track Points
        self.lp1 = PathObject((-70, -50, 157), 90)
        self.lp2 = PathObject((-51, -50, 165), 45)
        self.lp3 = PathObject((-25, -50, 160), 135)
        self.lp4 = PathObject((-4, -50, 156), 45)
        self.lp5 = PathObject((30, -50, 165), 121)
        self.lp6 = PathObject((84, -38, 163), 90)
        self.lp7 = PathObject((117, -37, 157), 210)
        self.lp8 = PathObject((121, -50, 114), 180)
        self.lp9 = PathObject((150, -50, 88), 60)
        self.lp10 = PathObject((170, -50, 80), 192)
        self.lp11 = PathObject((150, -50, 30), 280)
        self.lp12 = PathObject((131, -50, 20), 150)
        self.lp13 = PathObject((127, -50, -157), 177)
        self.lp14 = PathObject((131, -46, -190), 100)
        self.lp15 = PathObject((170, -39, -170), 0)
        self.lp16 = PathObject((170, -35, -153), -70)
        self.lp17 = PathObject((100, -46, -147), -90)
        self.lp18 = PathObject((-109, -50, -145), -90)
        self.lp19 = PathObject((-146, -50, -122), 60)
        self.lp20 = PathObject((-144, -44, 115), 0)
        self.lp21 = PathObject((-127, -50, 155), 120)

        # Path points lists
        self.sand_path = [self.sap1, self.sap2, self.sap3, self.sap4, self.sap5, self.sap6, self.sap7, self.sap8]
        self.grass_path = [self.gp1, self.gp2, self.gp3, self.gp4, self.gp5, self.gp6, self.gp7, self.gp8, self.gp9, self.gp10, self.gp11]
        self.snow_path = [self.snp1, self.snp2, self.snp3, self.snp4, self.snp5, self.snp6, self.snp7, self.snp8, self.snp9, self.snp10, self.snp11, self.snp12, self.snp13, self.snp14, self.snp15, self.snp16, self.snp17]
        self.forest_path = [self.fp1, self.fp2, self.fp3, self.fp4, self.fp5, self.fp6, self.fp7, self.fp8, self.fp9, self.fp10, self.fp11, self.fp12, self.fp13]
        self.savannah_path = [self.svp1, self.svp2, self.svp3, self.svp4, self.svp5, self.svp6, self.svp7, self.svp8]
        self.lake_path = [self.lp1, self.lp2, self.lp3, self.lp4, self.lp5, self.lp6, self.lp7, self.lp8, self.lp9, self.lp10, self.lp11, self.lp12, self.lp13, self.lp14, self.lp15, self.lp16, self.lp17, self.lp18, self.lp19, self.lp20, self.lp21]
        
        # The next point the ai is going to
        self.next_path = self.gp1

        # The speed of the AI
        self.difficulty = 50

        invoke(self.same_pos, delay = 5)

        self.disable()

    def sports_car(self):
        self.model = "sports-car.obj"
        self.texture = "sports-red.png"
        self.car_type = "sports"
    
    def muscle_car(self):
        self.model = "muscle-car.obj"
        self.texture = "muscle-orange.png"
        self.car_type = "muscle"

    def limo(self):
        self.model = "limousine.obj"
        self.texture = "limo-black.png"
        self.car_type = "limo"

    def lorry(self):
        self.model = "lorry.obj"
        self.texture = "lorry-white.png"
        self.car_type = "lorry"

    def hatchback(self):
        self.model = "hatchback.obj"
        self.texture = "hatchback-green.png"
        self.car_type = "hatchback"

    def rally_car(self):
        self.model = "rally-car.obj"
        self.texture = "rally-red.png"
        self.car_type = "rally"

    def set_random_car(self):
        """
        Sets a random car
        """
        i = random.randint(0, 5)
        if i == 0:
            self.sports_car()
        elif i == 1:
            self.muscle_car()
        elif i == 2:
            self.limo()
        elif i == 3:
            self.lorry()
        elif i == 4:
            self.hatchback()
        elif i == 5:
            self.rally_car()

    def set_random_texture(self):
        """
        Sets a random car colour
        """
        i = random.randint(0, 5)
        if i == 0:
            self.texture = f"{self.car_type}-red.png"
        elif i == 1:
            self.texture = f"{self.car_type}-blue.png"
        elif i == 2:
            self.texture = f"{self.car_type}-orange.png"
        elif i == 3:
            self.texture = f"{self.car_type}-green.png"
        elif i == 4:
            self.texture = f"{self.car_type}-white.png"
        elif i == 5:
            self.texture = f"{self.car_type}-black.png"

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

        if self.sand_track.enabled or self.grass_track.enabled or self.savannah_track.enabled or self.lake_track.enabled:
            self.difficulty = 60
        elif self.snow_track.enabled or self.forest_track.enabled:
            self.difficulty = 40

        """
        Rotation
        """
        # Set the position of the rotation parent to the car's position
        self.rotation_parent.position = self.position

        # Lerps the car's rotation to the rotation parent's rotation (Makes it smoother)
        self.rotation_x = lerp(self.rotation_x, self.rotation_parent.rotation_x, 20 * time.dt)
        self.rotation_z = lerp(self.rotation_z, self.rotation_parent.rotation_z, 20 * time.dt)
        
        # Main raycast for collision
        self.t += time.dt
        if self.t >= self.update_step:
            self.t = 0
            self.y_ray = raycast(origin = self.world_position, direction = (0, -1, 0), traverse_target = self.current_track, ignore = [self, self.sand_track.wall1, self.sand_track.wall2, self.sand_track.wall3, self.sand_track.wall4, self.grass_track.wall1, self.grass_track.wall2, self.grass_track.wall3, self.grass_track.wall4, self.snow_track.wall1, self.snow_track.wall2, self.snow_track.wall3, self.snow_track.wall4, self.snow_track.wall5, self.snow_track.wall6, self.snow_track.wall7, self.snow_track.wall8, self.snow_track.wall9, self.snow_track.wall10, self.snow_track.wall11, self.snow_track.wall12, self.forest_track.wall1, self.forest_track.wall2, self.forest_track.wall3, self.forest_track.wall4, self.forest_track.wall1, self.forest_track.wall2, self.forest_track.wall3, self.forest_track.wall4, ])

        if self.y_ray.distance <= 4:
            r = random.randint(0, 1)
            if r == 0:
                self.speed += self.acceleration * self.difficulty * time.dt

                self.particle_time += time.dt
                if self.particle_time >= self.particle_amount:
                    self.particle_time = 0
                    self.particles = Particles(self, position = self.particle_pivot.world_position - (0, 1, 0))
                    self.particles.destroy(1)

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
        elif self.forest_track.enabled:
            if distance(self.fp10, self) < 12:
                self.rotation_y = 0
                self.pivot.rotation_y = self.rotation_y
            for p in self.forest_path:
                if distance(p, self) < 12 and self.next_path == p:
                    self.next_path = self.forest_path[self.forest_path.index(p) - len(self.forest_path) + 1]
        elif self.savannah_track.enabled:
            if distance(self.svp4, self) < 10:
                self.speed -= 10 * time.dt
            if distance(self.svp8, self) < 12:
                self.rotation_y = 90
                self.pivot.rotation_y = self.rotation_y
            for p in self.savannah_path:
                if distance(p, self) < 15 and self.next_path == p:
                    self.next_path = self.savannah_path[self.savannah_path.index(p) - len(self.savannah_path) + 1]
        elif self.lake_track.enabled:
            if self.simple_intersects(self.lake_track.lake_bounds):
                self.reset()
            for p in self.lake_path:
                if distance(p, self) < 15 and self.next_path == p:
                    self.next_path = self.lake_path[self.lake_path.index(p) - len(self.lake_path) + 1]

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

        # Gravity
        movementY = self.velocity_y * time.dt

        if self.y_ray.distance <= self.scale_y * 1.7 + abs(movementY):
            self.velocity_y = 0
            # Check if hitting a wall or steep slope
            if self.y_ray.world_normal.y > 0.7 and self.y_ray.world_point.y - self.world_y < 0.5:
                # Set the y value to the ground's y value
                self.y = self.y_ray.world_point.y + 1.4
                self.hitting_wall = False
            else:
                self.hitting_wall = True

            if not self.hitting_wall:
                self.rotation_parent.look_at(self.position + self.y_ray.world_normal, axis = "up")
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
        if self.grass_track.enabled:
            self.position = (-80 + random.randint(-5, 5), -30 + random.randint(-3, 5), 15 + random.randint(-5, 5))
            self.rotation = (0, 90, 0)
            self.next_path = self.gp1
        elif self.sand_track.enabled:
            self.position = (-63 + random.randint(-5, 5), -40 + random.randint(-3, 5), -7 + random.randint(-5, 5))
            self.rotation = (0, 65, 0)
            self.next_path = self.sap1
        elif self.snow_track.enabled:
            self.position = (-5 + random.randint(-5, 5), -35 + random.randint(-3, 5), 90 + random.randint(-5, 5))
            self.rotation = (0, 90, 0)
            self.next_path = self.snp1
        elif self.forest_track.enabled:
            self.position = (12 + random.randint(-5, 5), -40 + random.randint(-3, 5), 73 + random.randint(-5, 5))
            self.rotation = (0, 90, 0)
            self.next_path = self.fp1
        elif self.lake_track.enabled:
            self.position = (-121, -40, 158)
            self.rotation = (0, 90, 0)
            self.next_path = self.lp1
        else:
            self.position = (0, 0, 0)
            self.rotation = (0, 0, 0)
        self.speed = 0
        self.velocity_y = 0

    def simple_intersects(self, entity):
        """
        A faster AABB intersects for detecting collision with
        simple objects, doesn't take rotation into account
        """
        minXA = self.x - self.scale_x
        maxXA = self.x + self.scale_x
        minYA = self.y - self.scale_y + (self.scale_y / 2)
        maxYA = self.y + self.scale_y - (self.scale_y / 2)
        minZA = self.z - self.scale_z
        maxZA = self.z + self.scale_z

        minXB = entity.x - entity.scale_x + (entity.scale_x / 2)
        maxXB = entity.x + entity.scale_x - (entity.scale_x / 2)
        minYB = entity.y - entity.scale_y + (entity.scale_y / 2)
        maxYB = entity.y + entity.scale_y - (entity.scale_y / 2)
        minZB = entity.z - entity.scale_z + (entity.scale_z / 2)
        maxZB = entity.z + entity.scale_z - (entity.scale_z / 2)
        
        return (
            (minXA <= maxXB and maxXA >= minXB) and
            (minYA <= maxYB and maxYA >= minYB) and
            (minZA <= maxZB and maxZA >= minZB)
        )

    def check_track(self):
        for track in self.tracks:
            if track.enabled:
                self.current_track = track

# Path Point class
class PathObject(Entity):
    def __init__(self, position = (0, 0, 0), rotation_y = 0):
        super().__init__(
            model = "cube",
            position = position,
            rotation_y = rotation_y,
            texture = "white_cube",
            scale = (1, 20, 20),
            visible = False,
            alpha = 50,
        )