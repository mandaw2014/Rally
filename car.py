from ursina import *
from particles import ParticleSystem

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class Car(Entity):
    def __init__(self, position = (0, 0, 0), topspeed = 25, acceleration = 0.7, friction = 0.3, rotation_speed = 1.8, camera_speed = 0.05, drift_speed = 25):
        super().__init__(
            model = "car",
            color = color.white,
            position = position,
            rotation = (0, 65, 0),
            collider = "box",
            scale = (1, 1, 1)
        )

        camera.position = (20, 30, -50)
        camera.rotation = (35, -20, 0)

        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = rotation_speed
        self.topspeed = topspeed
        self.camera_speed = camera_speed
        self.acceleration = acceleration
        self.friction = friction

        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        self.drift_speed = drift_speed

        self.slope = 99999999999999999999999999999999999999999999999

        self.sand_track = None

        self.timer_running = False
        self.count = 0.0
        self.last_count = self.count
        self.reset_count = 0.0
        self.timer = Text(text = str(round(self.count, 1)), origin = (0, 0), size = 0.05, scale = (1, 1), position = (0, 0.43))
        self.last_count_timer = Text(text = str(round(self.last_count, 1)), origin = (0, 0), size = 0.05, scale = (1, 1), position = (0, 0.43))
        self.last_count_timer.disable()

    def update(self):
        self.count += time.dt
        self.reset_count += time.dt
        self.timer.text = str(round(self.count, 1))
        self.last_count_timer.text = str(round(self.last_count, 1))

        camera_follow = SmoothFollow(target = self, offset = (20, 40, -50), speed = self.camera_speed)
        camera.add_script(camera_follow)

        self.pivot.position = self.position

        if self.pivot.rotation_x != self.rotation_x:
            if self.pivot.rotation_x > self.rotation_x:
                self.pivot.rotation_x -= (self.drift_speed * ((self.pivot.rotation_x - self.rotation_x) / 40)) * time.dt
            if self.pivot.rotation_x < self.rotation_x:
                self.pivot.rotation_x += (self.drift_speed * ((self.rotation_x - self.pivot.rotation_x) / 40)) * time.dt
        if self.pivot.rotation_y != self.rotation_y:
            if self.pivot.rotation_y > self.rotation_y:
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
            if self.pivot.rotation_y < self.rotation_y:
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
        if self.pivot.rotation_z != self.rotation_z:
            if self.pivot.rotation_z > self.rotation_z:
                self.pivot.rotation_z -= (self.drift_speed * ((self.pivot.rotation_z - self.rotation_z) / 40)) * time.dt
            if self.pivot.rotation_z < self.rotation_z:
                self.pivot.rotation_z += (self.drift_speed * ((self.rotation_z - self.pivot.rotation_z) / 40)) * time.dt

        ground_check = raycast(origin = self.position, direction = self.down, distance = 4, ignore = [self, ], traverse_target = self.sand_track)

        if held_keys["w"]:
            if ground_check.hit:
                self.speed += self.acceleration * 50 * time.dt
                # particles = ParticleSystem(position = Vec3(self.x, self.y - 2, self.z), color = color.hex("925B3A"), rotation_y = random.random() * 360)
                # particles.fade_out(duration = 0.2, delay = 1 - 0.2, curve = curve.linear)
        else:
            if ground_check.hit:
                self.speed -= self.friction * 50 * time.dt
            self.rotation_speed -= 5 * time.dt

        if held_keys["s"]:
            self.speed -= 10 * time.dt
            # self.rotation_speed -= 0.01 + self.speed * time.dt
        # else:
        #     self.speed += 0.8

        if self.speed != 0:
            if held_keys["a"]:
                self.rotation_y -= self.rotation_speed * 50 * time.dt
                self.speed -= 25 * time.dt
                self.rotation_speed += 0.5 * time.dt
            elif held_keys["d"]:
                self.rotation_y += self.rotation_speed * 50 * time.dt
                self.speed -= 25 * time.dt
                self.rotation_speed += 0.5 * time.dt
            else:
                self.rotation_speed -= 5
            
            # self.speed -= 0.5 * self.drift_length * time.dt

        if self.speed >= self.topspeed:
            self.speed = self.topspeed
        if self.speed <= 0:
            self.speed = 0
            self.pivot.rotation = self.rotation

        if self.rotation_speed >= 5:
            self.rotation_speed = 5
        if self.rotation_speed <= 1.8:
            self.rotation_speed = 1.8

        movementY = self.velocity_y * time.dt
        direction = (0, sign(movementY), 0)

        y_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_y * 3 + abs(movementY), ignore = [self, ], traverse_target = self.sand_track)

        if y_ray.hit:
            self.jump_count = 0
            self.velocity_y = 0
        else:
            self.y += movementY
            self.velocity_y -= 1 * time.dt * 25

        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        if movementX != 0:
            direction = (sign(movementX), 0, 0)
            x_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_x / 2 + abs(movementX), ignore = [self, ], thickness = (1, 1), traverse_target = self.sand_track)

            if not x_ray.hit:
                self.x += movementX
            else:
                top_x_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_x / 2 + math.tan(math.radians(self.slope)), ignore = [self, ], traverse_target = self.sand_track)

                if not top_x_ray.hit:
                    self.x += movementX
                    height_ray = raycast(origin = self.world_position + (sign(movementX) * self.scale_x / 2, -self.scale_y / 2, 0), direction = (0, 1, 0), ignore = [self, ], traverse_target = self.sand_track)
                    if height_ray.hit:
                        self.y += height_ray.distance

        if movementZ != 0:
            direction = (0, 0, sign(movementZ))
            z_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_z / 2 + abs(movementZ), ignore = [self, ], thickness = (1, 1), traverse_target = self.sand_track)

            if not z_ray.hit:
                self.z += movementZ
            else:
                top_z_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_z / 2 + math.tan(math.radians(self.slope)), ignore = [self, ], traverse_target = self.sand_track)

                if not top_z_ray.hit:
                    self.z += movementZ
                    height_ray = raycast(origin = self.world_position + (0, -self.scale_y / 2, sign(movementZ) * self.scale_z / 2), direction = (0, 1, 0), ignore = [self, ], traverse_target = self.sand_track)
                    if height_ray.hit:
                        self.y += height_ray.distance

    def reset_timer(self):
        self.count = self.reset_count
        self.last_count_timer.disable()
        self.timer.enable()

        """

        Old Camera Mechanics:

        camera.x = self.x + 20
        camera.z = self.z - 50
        camera.y = self.y + 25

        """

        """

        Old Car

        self.wheel1 = Entity(model = "sphere", color = color.white, scale = (0.4, 0.5, 0.3), parent = self, x = self.x + 0.5, y = self.y - 30.5, z = self.z + 0.25)
        self.wheel2 = Entity(model = "sphere", color = color.white, scale = (0.4, 0.5, 0.3), parent = self, x = self.x + 0.5, y = self.y - 30.5, z = self.z - 0.25)
        self.wheel3 = Entity(model = "sphere", color = color.white, scale = (0.4, 0.5, 0.3), parent = self, x = self.x - 0.5, y = self.y - 30.5, z = self.z + 0.25)
        self.wheel4 = Entity(model = "sphere", color = color.white, scale = (0.4, 0.5, 0.3), parent = self, x = self.x - 0.5, y = self.y - 30.5, z = self.z - 0.25)
        
        if self.pivot.rotation_x > self.rotation_x:
            self.drift_length += 20 * time.dt
        if self.pivot.rotation_x < self.rotation_x:
            self.drift_length -= 20 * time.dt
        if self.pivot.rotation_y > self.rotation_y:
            self.drift_length += 20 * time.dt
        if self.pivot.rotation_y < self.rotation_y:
            self.drift_length -= 20 * time.dt
        if self.pivot.rotation_z > self.rotation_z:
            self.drift_length += 20 * time.dt
        if self.pivot.rotation_z < self.rotation_z:
            self.drift_length -= 20 * time.dt

        """