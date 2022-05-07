from ursina import *
from ursina import curve
from particles import ParticleSystem

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)

class Car(Entity):
    def __init__(self, position = (0, 0, 0), rotation = (0, 65, 0), topspeed = 25, acceleration = 0.4, friction = 0.6, camera_speed = 8, drift_speed = 35):
        super().__init__(
            model = "car.obj",
            texture = "car-red.png",
            position = position,
            rotation = rotation,
            collider = "box",
            scale = (1, 1, 1)
        )

        camera.position = self.position + (20, 40, -50)
        camera.rotation = (35, -20, 0)

        self.controls = "wasd"

        self.original_camera_position = camera.position
        self.shake_duration = 2.0
        self.shake_amount = 0.1
        self.can_shake = False
        self.camera_shake_option = True

        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.topspeed = topspeed
        self.camera_speed = camera_speed
        self.acceleration = acceleration
        self.friction = friction
        self.pivot_rotation_distance = 1

        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation

        self.particle_pivot = Entity()
        self.particle_pivot.parent = self
        self.particle_pivot.position = self.position - (0, 1, 5)

        self.drift_speed = drift_speed

        self.slope = 100

        self.sand_track = None
        self.grass_track = None
        self.snow_track = None

        self.timer_running = False
        self.count = 0.0
        self.highscore_count = None
        self.last_count = self.count
        self.reset_count = 0.0
        self.timer = Text(text = "", origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        self.highscore = Text(text = "", origin = (0, 0), size = 0.05, scale = (0.6, 0.6), position = (-0.7, 0.38))
        self.reset_count_timer = Text(text = str(round(self.reset_count, 1)), origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        
        self.reset_count_timer.disable()

        self.laps = 0
        self.anti_cheat = 1
        self.started = False
        self.server_running = False
        self.scores = {}

        self.camera_follow = SmoothFollow(target = self, offset = (20, 40, -50), speed = self.camera_speed)
        camera.add_script(self.camera_follow)

        path = os.path.dirname(os.path.abspath(__file__))
        self.highscore_path_sand = os.path.join(path, "./highscore/highscore-sandtrack.txt")
        self.highscore_path_grass = os.path.join(path, "./highscore/highscore-grasstrack.txt")
        self.highscore_path_snow = os.path.join(path, "./highscore/highscore-snowtrack.txt")

        with open(self.highscore_path_sand, "r") as hs:
            self.highscore_count = hs.read()

        self.highscore_count = float(self.highscore_count)
        self.old_highscore = self.highscore_count

        self.username_path = os.path.join(path, "./highscore/username.txt")
        with open(self.username_path, "r") as username:
            self.username_text = username.read()
            print(self.username_text)

    def update(self):
        if self.timer_running is True:
            self.count += time.dt
            self.reset_count += time.dt
        self.timer.text = str(round(self.count, 1))
        self.reset_count_timer.text = str(round(self.reset_count, 1))

        self.highscore.text = str(round(self.highscore_count, 1))

        with open(self.username_path, "r") as username:
            self.username_text = username.read()

        self.pivot.position = self.position

        camera.rotation = (35, -20, 0)
        self.camera_follow.offset = (20, 40, -50)

        if self.pivot.rotation_y != self.rotation_y:
            if self.pivot.rotation_y > self.rotation_y:
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
                self.speed += self.pivot_rotation_distance / 5 * time.dt
                self.rotation_speed -= 2 * time.dt
            if self.pivot.rotation_y < self.rotation_y:
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
                self.speed -= self.pivot_rotation_distance / 5 * time.dt
                self.rotation_speed += 2 * time.dt

        ground_check = raycast(origin = self.position, direction = self.down, distance = 5, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ])

        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        if held_keys[self.controls[0]] or held_keys["up arrow"]:
            if ground_check.hit:
                self.speed += self.acceleration * 50 * time.dt
                self.rotation_y += self.rotation_speed * 50 * time.dt

                if self.rotation_speed > 0:
                    self.rotation_speed -= self.speed / 4 * time.dt
                elif self.rotation_speed < 0:
                    self.rotation_speed += self.speed / 4 * time.dt

                self.particles = ParticleSystem(position = self.particle_pivot.world_position, rotation_y = random.random() * 360)
                if self.sand_track.enabled == True:
                    self.particles.color = color.hex("925B3A")
                elif self.grass_track.enabled == True:
                    self.particles.color = color.hex("8C6C30")
                elif self.snow_track.enabled == True:
                    self.particles.color = color.hex("76604C")
                else:
                    self.particles.color = color.hex("925B3A")
                self.particles.fade_out(duration = 0.2, delay = 1 - 0.2, curve = curve.linear)
                invoke(self.particles.disable, delay = 1)
        else:
            if ground_check.hit:
                self.speed -= self.friction * 50 * time.dt
            self.shake_amount -= 0.001 * time.dt

        if held_keys[self.controls[2] or held_keys["down arrow"]]:
            self.speed -= 10 * time.dt

        if held_keys["space"]:
            self.drift_speed -= 20 * time.dt
            self.speed -= 20 * time.dt
            self.rotation_speed *= 60 * time.dt
            self.max_rotation_speed = 3
        else:
            self.max_rotation_speed = 2.6

        if held_keys["g"]:
            if self.grass_track.enabled is True:
                self.position = (-80, -30, 15)
                self.rotation = (0, 90, 0)
            if self.sand_track.enabled is True:
                self.position = (0, -40, 4)
                self.rotation = (0, 65, 0)
            if self.snow_track.enabled == True:
                self.position = (-5, -35, 90)
                self.rotation = (0, 90, 0)
            self.speed = 0
            self.count = 0.0
            self.reset_count = 0.0
            self.timer_running = False
            self.anti_cheat = 1

        if self.speed != 0:
            if held_keys[self.controls[1]] or held_keys["left arrow"]:
                self.rotation_speed -= 13 * time.dt
                self.drift_speed -= 10 * time.dt
            elif held_keys[self.controls[3]] or held_keys["right arrow"]:
                self.rotation_speed += 13 * time.dt
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

        if self.rotation_speed >= self.max_rotation_speed:
            self.rotation_speed = self.max_rotation_speed
        if self.rotation_speed <= -self.max_rotation_speed:
            self.rotation_speed = -self.max_rotation_speed

        if self.speed >= 1:
            self.can_shake = True
            self.shake_amount += self.speed / 5000 * time.dt
        else:
            self.shake_amount -= 0.1 * time.dt

        if self.shake_amount <= 0:
            self.shake_amount = 0
        if self.shake_amount >= 0.03:
            self.shake_amount = 0.03

        if self.can_shake and self.camera_shake_option:
            self.shake_camera()

        if self.y <= -200:
            if self.grass_track.enabled is True:
                self.position = (-80, -30, 15)
                self.rotation = (0, 90, 0)
            if self.sand_track.enabled is True:
                self.position = (0, -40, 4)
                self.rotation = (0, 65, 0)
            if self.snow_track.enabled == True:
                self.car.position = (-5, -35, 90)
                self.car.rotation = (0, 90, 0)
            self.speed = 0
            self.count = 0.0
            self.reset_count = 0.0
            self.timer_running = False
            self.anti_cheat = 1

        if self.y >= 500:
            if self.grass_track.enabled is True:
                self.position = (-80, -30, 15)
                self.rotation = (0, 90, 0)
            if self.sand_track.enabled is True:
                self.position = (0, -40, 4)
                self.rotation = (0, 65, 0)
            if self.snow_track.enabled == True:
                self.position = (-5, -35, 90)
                self.rotation = (0, 90, 0)
            self.speed = 0
            self.count = 0.0
            self.reset_count = 0.0
            self.timer_running = False
            self.anti_cheat = 1

        movementY = self.velocity_y * time.dt
        direction = (0, sign(movementY), 0)

        y_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_y * 4 + abs(movementY), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ])

        if y_ray.hit:
            self.jump_count = 0
            self.velocity_y = 0
            
            # self.animate_rotation_x(y_ray.normal[0] * 200, duration = 0.1, curve = curve.linear)
            # self.animate_rotation_z((y_ray.world_normal[2] * 30), duration = 0.1, curve = curve.linear)

        else:
            self.y += movementY * 50 * time.dt
            self.velocity_y -= 1

        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        if movementX != 0:
            direction = (sign(movementX), 0, 0)
            x_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_x / 2 + abs(movementX), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ], thickness = (1, 1))

            if not x_ray.hit:
                self.x += movementX
            else:
                top_x_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_x / 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ])

                if not top_x_ray.hit:
                    # if top_x_ray.distance < self.slope:
                    self.x += movementX
                    height_ray = raycast(origin = self.world_position + (sign(movementX) * self.scale_x / 2, -self.scale_y / 2, 0), direction = (0, 1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ])
                    if height_ray.distance < self.slope:
                        self.y += height_ray.distance

        if movementZ != 0:
            direction = (0, 0, sign(movementZ))
            z_ray = boxcast(origin = self.world_position, direction = direction, distance = self.scale_z / 2 + abs(movementZ), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ], thickness = (1, 1))

            if not z_ray.hit:
                self.z += movementZ
            else:
                top_z_ray = raycast(origin = self.world_position - (0, self.scale_y / 2 - 0.1, 0), direction = direction, distance = self.scale_z / 2, ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ])

                if not top_z_ray.hit:
                    # if top_z_ray.distance < self.slope:
                    self.z += movementZ
                    height_ray = raycast(origin = self.world_position + (0, -self.scale_y / 2, sign(movementZ) * self.scale_z / 2), direction = (0, 1, 0), ignore = [self, self.sand_track.finish_line, self.sand_track.wall_trigger, self.grass_track.finish_line, self.grass_track.wall_trigger, self.grass_track.wall_trigger_ramp, self.snow_track.finish_line, self.snow_track.wall_trigger, self.snow_track.wall_trigger_end, ])
                    if height_ray.hit:
                        if height_ray.distance < self.slope * 10:
                            self.y += height_ray.distance

    def reset_timer(self):
        self.count = self.reset_count
        self.timer.enable()
        self.reset_count_timer.disable()
        self.old_highscore = self.highscore_count

    def update_camera_pos(self):
        self.original_camera_position = camera.position

    def shake_camera(self):
        camera.x += random.randint(-1, 1) * self.shake_amount
        camera.y += random.randint(-1, 1) * self.shake_amount
        camera.z += random.randint(-1, 1) * self.shake_amount

class CarRepresentation(Entity):
    def __init__(self, car, position = (0, 0, 0), rotation = (0, 65, 0)):
        super().__init__(
            parent = scene,
            model = "car.obj",
            texture = "car-red.png",
            position = position,
            rotation = rotation,
            scale = (1, 1, 1)
        )

        self.text_object = None
        self.highscore = 0.0

class CarUsername(Text):
    def __init__(self, car):
        super().__init__(
            parent = car,
            text = "Guest",
            y = 3,
            scale = 30,
            color = color.white,
        )
    
        self.username_text = "Guest"

    def update(self):
        self.text = self.username_text