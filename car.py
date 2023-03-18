from ursina import *
from ursina import curve
from particles import Particles, TrailRenderer
import json

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)
Text.default_resolution = 1080 * Text.size

class Car(Entity):
    def __init__(self, position = (0, 0, 4), rotation = (0, 0, 0), topspeed = 30, acceleration = 0.35, braking_strength = 30, friction = 0.6, camera_speed = 8, drift_speed = 35):
        super().__init__(
            model = "sports-car.obj",
            texture = "sports-red.png",
            collider = "box",
            position = position,
            rotation = rotation,
        )

        # Rotation parent
        self.rotation_parent = Entity()

        # Controls
        self.controls = ["w", "a", "s", "d"]
        self.hand_brake_control = "space"
        self.respawn_control = "g"

        # Car's values
        self.speed = 0
        self.velocity_y = 0
        self.rotation_speed = 0
        self.max_rotation_speed = 2.6
        self.steering_amount = 8
        self.topspeed = topspeed
        self.braking_strenth = braking_strength
        self.camera_speed = camera_speed
        self.acceleration = acceleration
        self.friction = friction
        self.drift_speed = drift_speed
        self.drift_amount = 4.5
        self.turning_speed = 5
        self.max_drift_speed = 40
        self.min_drift_speed = 20
        self.pivot_rotation_distance = 1

        # Camera Follow
        self.camera_angle = "top"
        self.camera_offset = (0, 60, -70)
        self.camera_rotation = 40
        self.camera_follow = False
        self.change_camera = False
        self.c_pivot = Entity()
        self.camera_pivot = Entity(parent = self.c_pivot, position = self.camera_offset)

        # Pivot for drifting
        self.pivot = Entity()
        self.pivot.position = self.position
        self.pivot.rotation = self.rotation
        self.drifting = False

        # Car Type
        self.car_type = "sports"

        # Particles
        self.particle_time = 0
        self.particle_amount = 0.07 # The lower, the more
        self.particle_pivot = Entity(parent = self)
        self.particle_pivot.position = (0, -1, -2)

        # TrailRenderer
        self.trail_pivot = Entity(parent = self, position = (0, -1, 2))

        self.trail_renderer1 = TrailRenderer(parent = self.particle_pivot, position = (0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        self.trail_renderer2 = TrailRenderer(parent = self.particle_pivot, position = (-0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        self.trail_renderer3 = TrailRenderer(parent = self.trail_pivot, position = (0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        self.trail_renderer4 = TrailRenderer(parent = self.trail_pivot, position = (-0.8, -0.2, 0), color = color.black, alpha = 0, thickness = 7, length = 200)
        
        self.trails = [self.trail_renderer1, self.trail_renderer2, self.trail_renderer3, self.trail_renderer4]
        self.start_trail = True

        # Audio
        self.audio = True
        self.volume = 1
        self.start_sound = True
        self.start_fall = True
        self.drive_sound = Audio("rally.mp3", loop = True, autoplay = False, volume = 0.5)
        self.dirt_sound = Audio("dirt-skid.mp3", loop = True, autoplay = False, volume = 0.8)
        self.skid_sound = Audio("skid.mp3", loop = True, autoplay = False, volume = 0.5)
        self.hit_sound = Audio("hit.wav", autoplay = False, volume = 0.5)
        self.drift_swush = Audio("unlock.mp3", autoplay = False, volume = 0.8)

        # Collision
        self.copy_normals = False
        self.hitting_wall = False

        # Making tracks accessible in update
        self.sand_track = None
        self.grass_track = None
        self.snow_track = None
        self.forest_track = None
        self.savannah_track = None
        self.lake_track = None

        # Cosmetics
        self.current_cosmetic = "none"
        self.viking_helmet = Entity(model = "viking_helmet.obj", texture = "viking_helmet.png", parent = self)
        self.duck = Entity(model = "duck.obj", parent = self)
        self.banana = Entity(model = "banana.obj", parent = self)
        self.surfinbird = Entity(model = "surfinbird.obj", texture = "surfinbird.png", parent = self)
        self.surfboard = Entity(model = "surfboard.obj", texture = "surfboard.png", parent = self.surfinbird)
        self.cosmetics = [self.viking_helmet, self.duck, self.banana, self.surfinbird]
        self.viking_helmet.disable()
        self.duck.disable()
        self.banana.disable()
        self.surfinbird.disable()

        # Graphics
        self.graphics = "fancy"

        # Stopwatch/Timer
        self.timer_running = False
        self.count = 0.0
        self.highscore_count = None
        self.last_count = self.count
        self.reset_count = 0.0
        self.timer = Text(text = "", origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        self.highscore = Text(text = "", origin = (0, 0), size = 0.05, scale = (0.6, 0.6), position = (-0.7, 0.38))
        self.laps_text = Text(text = "", origin = (0, 0), size = 0.05, scale = (1.1, 1.1), position = (0, 0.43))
        self.reset_count_timer = Text(text = str(round(self.reset_count, 1)), origin = (0, 0), size = 0.05, scale = (1, 1), position = (-0.7, 0.43))
        
        self.timer.disable()
        self.highscore.disable()
        self.laps_text.disable()
        self.reset_count_timer.disable()

        self.gamemode = "race"
        self.start_time = False
        self.laps = 0
        self.laps_hs = 0
        self.anti_cheat = 1

        # Drift Gamemode
        self.drift_text = Text(text = "", origin = (0, 0), color = color.white, size = 0.05, scale = (1.1, 1.1), position = (0, 0.43), visible = False)
        self.drift_timer = Text(text = "", origin = (0, 0), size = 0.05, scale = (1, 1), position = (0.7, 0.43))
        self.start_drift = False
        self.drift_score = 0
        self.drift_time = 0
        self.drift_multiplier = 20
        self.get_hundred = False
        self.get_thousand = False
        self.get_fivethousand = False

        # Bools
        self.driving = False
        self.braking = False

        self.ai = False
        self.ai_list = []

        # Multiplayer
        self.multiplayer = False
        self.multiplayer_update = False
        self.server_running = False

        # Shows whether you are connected to a server or not
        self.connected_text = True
        self.disconnected_text = True

        # Camera shake
        self.shake_amount = 0.1
        self.can_shake = False
        self.camera_shake_option = True

        # Get highscore from json file
        path = os.path.dirname(sys.argv[0])
        self.highscore_path = os.path.join(path, "./highscore/highscore.json")
        
        try:
            with open(self.highscore_path, "r") as hs:
                self.highscores = json.load(hs)
        except FileNotFoundError:
            with open(self.highscore_path, "w+") as hs:
                self.reset_highscore()
                self.highscores = json.load(hs)

        self.sand_track_hs = self.highscores["race"]["sand_track"]
        self.grass_track_hs = self.highscores["race"]["grass_track"]
        self.snow_track_hs = self.highscores["race"]["snow_track"]
        self.forest_track_hs = self.highscores["race"]["forest_track"]
        self.savannah_track_hs = self.highscores["race"]["savannah_track"]
        self.lake_track_hs = self.highscores["race"]["lake_track"]

        self.sand_track_laps = self.highscores["time_trial"]["sand_track"]
        self.grass_track_laps = self.highscores["time_trial"]["grass_track"]
        self.snow_track_laps = self.highscores["time_trial"]["snow_track"]
        self.forest_track_laps = self.highscores["time_trial"]["forest_track"]
        self.savannah_track_laps = self.highscores["time_trial"]["savannah_track"]
        self.lake_track_laps = self.highscores["time_trial"]["lake_track"]

        self.sand_track_drift = self.highscores["drift"]["sand_track"]
        self.grass_track_drift = self.highscores["drift"]["grass_track"]
        self.snow_track_drift = self.highscores["drift"]["snow_track"]
        self.forest_track_drift = self.highscores["drift"]["forest_track"]
        self.savannah_track_drift = self.highscores["drift"]["savannah_track"]
        self.lake_track_drift = self.highscores["drift"]["lake_track"]

        self.highscore_count = self.sand_track_hs
        self.highscore_count = float(self.highscore_count)

        self.username_path = os.path.join(path, "./highscore/username.txt")
        with open(self.username_path, "r") as username:
            self.username_text = username.read()

        self.unlocked_json = os.path.join(path, "./highscore/unlocked.json")
        try:
            with open(self.unlocked_json, "r") as u:
                self.unlocked = json.load(u)
        except FileNotFoundError:
            with open(self.unlocked_json, "w+") as u:
                self.save_unlocked()
                self.unlocked = json.load(u)

        self.beat_mandaw_sand_track = False
        self.beat_mandaw_grass_track = False
        self.beat_mandaw_snow_track = False
        self.beat_mandaw_forest_track = False
        self.beat_mandaw_savannah_track = False
        self.beat_mandaw_lake_track = False

        self.model_path = str(self.model).replace("render/scene/car/", "")

        invoke(self.set_unlocked, delay = 1)
        invoke(self.update_model_path, delay = 3)

    def sports_car(self):
        self.car_type = "sports"
        self.model = "sports-car.obj"
        self.texture = "sports-red.png"
        self.drive_sound.clip = "sports.mp3"
        self.topspeed = 30
        self.acceleration = 0.38
        self.drift_amount = 5
        self.turning_speed = 5
        self.min_drift_speed = 18
        self.max_drift_speed = 38
        self.max_rotation_speed = 3
        self.steering_amount = 8
        self.particle_pivot.position = (0, -1, -1.5)
        self.trail_pivot.position = (0, -1, 1.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0

    def muscle_car(self):
        self.car_type = "muscle"
        self.model = "muscle-car.obj"
        self.texture = "muscle-orange.png"
        self.drive_sound.clip = "muscle.mp3"
        self.topspeed = 38
        self.acceleration = 0.32
        self.drift_amount = 6
        self.turning_speed = 10
        self.min_drift_speed = 22
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8.5
        self.particle_pivot.position = (0, -1, -1.8)
        self.trail_pivot.position = (0, -1, 1.8)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0

    def limo(self):
        self.car_type = "limo"
        self.model = "limousine.obj"
        self.texture = "limo-black.png"
        self.drive_sound.clip = "limo.mp3"
        self.topspeed = 30
        self.acceleration = 0.33
        self.drift_amount = 5.5
        self.turning_speed = 8
        self.min_drift_speed = 20
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8
        self.particle_pivot.position = (0, -1, -3.5)
        self.trail_pivot.position = (0, -1, 3.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0.1

    def lorry(self):
        self.car_type = "lorry"
        self.model = "lorry.obj"
        self.texture = "lorry-white.png"
        self.drive_sound.clip = "lorry.mp3"
        self.topspeed = 30
        self.acceleration = 0.3
        self.drift_amount = 7
        self.turning_speed = 7
        self.min_drift_speed = 20
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 7.5
        self.particle_pivot.position = (0, -1, -3.5)
        self.trail_pivot.position = (0, -1, 3.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 1.5

    def hatchback(self):
        self.car_type = "hatchback"
        self.model = "hatchback.obj"
        self.texture = "hatchback-green.png"
        self.drive_sound.clip = "hatchback.mp3"
        self.topspeed = 28
        self.acceleration = 0.43
        self.drift_amount = 6
        self.turning_speed = 15
        self.min_drift_speed = 20
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8.5
        self.particle_pivot.position = (0, -1, -1.5)
        self.trail_pivot.position = (0, -1, 1.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0.4

    def rally_car(self):
        self.car_type = "rally"
        self.model = "rally-car.obj"
        self.texture = "rally-red.png"
        self.drive_sound.clip = "rally.mp3"
        self.topspeed = 34
        self.acceleration = 0.46
        self.drift_amount = 4
        self.turning_speed = 7
        self.min_drift_speed = 22
        self.max_drift_speed = 40
        self.max_rotation_speed = 3
        self.steering_amount = 8.5
        self.particle_pivot.position = (0, -1, -1.5)
        self.trail_pivot.position = (0, -1, 1.5)
        for cosmetic in self.cosmetics:
            cosmetic.y = 0.3

    def update(self):
        # Stopwatch/Timer
        # Race Gamemode
        if self.gamemode == "race":
            self.highscore.text = str(round(self.highscore_count, 1))
            self.laps_text.disable()
            if self.timer_running:
                self.count += time.dt
                self.reset_count += time.dt
        # Time Trial Gamemode
        elif self.gamemode == "time trial":
            self.highscore.text = str(self.laps_hs)
            self.laps_text.text = str(self.laps)
            if self.timer_running:
                self.count -= time.dt
                self.reset_count -= time.dt
                if self.count <= 0.0:
                    self.count = 100.0
                    self.reset_count = 100.0
                    self.timer_running = False

                    if self.laps >= self.laps_hs:
                        self.laps_hs = self.laps

                    self.laps = 0

                    if self.sand_track.enabled:
                        self.sand_track_laps = self.laps_hs
                    elif self.grass_track.enabled:
                        self.grass_track_laps = self.laps_hs
                    elif self.snow_track.enabled:
                        self.snow_track_laps = self.laps_hs
                    elif self.forest_track.enabled:
                        self.forest_track_laps = self.laps_hs
                    elif self.savannah_track.enabled:
                        self.savannah_track_laps = self.laps_hs
                    elif self.lake_track.enabled:
                        self.lake_track_laps = self.laps_hs

                    self.start_time = False

                    self.save_highscore()
                    self.reset_car()
        # Drift Gamemode
        elif self.gamemode == "drift":
            self.timer.text = str(int(self.drift_score))
            self.drift_text.text = str(int(self.count))
            self.drift_timer.text = str(float(round(self.drift_time, 1)))
            self.laps_text.disable()
            if self.timer_running:
                self.drift_time -= time.dt
                if self.drifting and held_keys["w"]:
                    self.count += self.drift_multiplier * time.dt
                    self.drift_multiplier += time.dt * 10
                    self.start_drift = True
                    self.drift_text.visible = True
                    self.drift_text.x = 0

                    if abs(100 - self.count) <= 5 or abs(200 - self.count) <= 20:
                        if not self.get_hundred:
                            self.animate_text(self.drift_text, 1.7, 1.1)
                            self.get_hundred = True
                    if abs(1000 - self.count) <= 10 or abs(2000 - self.count) <= 50:
                        if not self.get_thousand:
                            self.animate_text(self.drift_text, 1.7, 1.1)
                            self.get_thousand = True
                    if abs(5000 - self.count) <= 20 or abs(10000 - self.count) <= 100:
                        if not self.get_fivethousand:
                            self.animate_text(self.drift_text, 1.7, 1.1)
                            self.get_fivethousand = True

                    if self.count >= 100 and self.count < 1000:
                        self.drift_text.color = color.hex("#6eb1ff")
                    elif self.count >= 1000 and self.count < 5000:
                        self.drift_text.color = color.gold
                    elif self.count >= 5000:
                        self.drift_text.color = color.red
                    else:
                        self.drift_text.color = color.white
                else:
                    if self.start_drift:
                        self.reset_drift()
                        self.start_drift = False
                if self.drift_time <= 0:
                    self.drift_timer.shake()
                    self.reset_car()

        if self.gamemode != "drift":
            self.timer.text = str(round(self.count, 1))
            self.reset_count_timer.text = str(round(self.reset_count, 1))
        else:
            self.reset_count_timer.text = str(int(self.reset_count))

        # Read the username
        with open(self.username_path, "r") as username:
            self.username_text = username.read()

        self.pivot.position = self.position
        self.c_pivot.position = self.position
        self.c_pivot.rotation_y = self.rotation_y
        self.camera_pivot.position = self.camera_offset

        # Camera
        if self.camera_follow:
            # Side Camera Angle
            if self.camera_angle == "side":
                camera.rotation = (35, -20, 0)
                self.camera_speed = 8
                self.change_camera = False
                camera.world_position = lerp(camera.world_position, self.world_position + (20, 40, -50), time.dt * self.camera_speed)
            # Top Camera Angle
            elif self.camera_angle == "top":
                if self.change_camera:
                    camera.rotation_x = 35
                    self.camera_rotation = 40
                self.camera_offset = (0, 60, -70)
                self.camera_speed = 4
                self.change_camera = False
                camera.rotation_x = lerp(camera.rotation_x, self.camera_rotation, 2 * time.dt)
                camera.world_position = lerp(camera.world_position, self.camera_pivot.world_position, time.dt * self.camera_speed / 2)
                camera.world_rotation_y = lerp(camera.world_rotation_y, self.world_rotation_y, time.dt * self.camera_speed / 2)
            # Third Person Camera Angle
            elif self.camera_angle == "behind":
                if self.change_camera:
                    camera.rotation_x = 12
                    self.camera_rotation = 40
                self.camera_offset = (0, 10, -30)
                self.change_camera = False
                self.camera_speed = 8
                camera.rotation_x = lerp(camera.rotation_x, self.camera_rotation / 3, 2 * time.dt)
                camera.world_position = lerp(camera.world_position, self.camera_pivot.world_position, time.dt * self.camera_speed / 2)
                camera.world_rotation_y = lerp(camera.world_rotation_y, self.world_rotation_y, time.dt * self.camera_speed / 2)
            # First Person Camera Angle
            elif self.camera_angle == "first-person":
                self.change_camera = False
                self.camera_speed = 8
                camera.world_position = lerp(camera.world_position, self.world_position + (0.5, 0, 0), time.dt * 30)
                camera.world_rotation = lerp(camera.world_rotation, self.world_rotation, time.dt * 30)

        # The y rotation distance between the car and the pivot
        self.pivot_rotation_distance = (self.rotation_y - self.pivot.rotation_y)

        # Drifting
        if self.pivot.rotation_y != self.rotation_y:
            if self.pivot.rotation_y > self.rotation_y:
                self.pivot.rotation_y -= (self.drift_speed * ((self.pivot.rotation_y - self.rotation_y) / 40)) * time.dt
                if self.speed > 1 or self.speed < -1:
                    self.speed += self.pivot_rotation_distance / self.drift_amount * time.dt
                self.camera_rotation -= self.pivot_rotation_distance / 3 * time.dt
                self.rotation_speed -= 1 * time.dt
                if self.pivot_rotation_distance >= 50 or self.pivot_rotation_distance <= -50:
                    self.drift_speed += self.pivot_rotation_distance / 5 * time.dt
                else:
                    self.drift_speed -= self.pivot_rotation_distance / 5 * time.dt
            if self.pivot.rotation_y < self.rotation_y:
                self.pivot.rotation_y += (self.drift_speed * ((self.rotation_y - self.pivot.rotation_y) / 40)) * time.dt
                if self.speed > 1 or self.speed < -1:
                    self.speed -= self.pivot_rotation_distance / self.drift_amount * time.dt
                self.camera_rotation += self.pivot_rotation_distance / 3 * time.dt
                self.rotation_speed += 1 * time.dt
                if self.pivot_rotation_distance >= 50 or self.pivot_rotation_distance <= -50:
                    self.drift_speed -= self.pivot_rotation_distance / 5 * time.dt
                else:
                    self.drift_speed += self.pivot_rotation_distance / 5 * time.dt

        # Gravity
        movementY = self.velocity_y / 50
        direction = (0, sign(movementY), 0)

        # Main raycast for collision
        y_ray = raycast(origin = self.world_position, direction = (0, -1, 0), ignore = [self, ])

        if y_ray.distance <= 5:
            # Driving
            if held_keys[self.controls[0]] or held_keys["up arrow"]:
                self.speed += self.acceleration * 50 * time.dt
                self.speed += -self.velocity_y * 4 * time.dt

                self.camera_rotation -= self.acceleration * 30 * time.dt
                self.driving = True

                # Particles
                self.particle_time += time.dt
                if self.particle_time >= self.particle_amount:
                    self.particle_time = 0
                    self.particles = Particles(self, self.particle_pivot.world_position - (0, 1, 0))
                    self.particles.destroy(1)

                # TrailRenderer / Skid Marks
                if self.graphics != "ultra fast":
                    if self.drift_speed <= self.min_drift_speed + 2 and self.start_trail:
                        if self.pivot_rotation_distance > 60 or self.pivot_rotation_distance < -60 and self.speed > 10:
                            for trail in self.trails:
                                trail.start_trail()
                            if self.audio:
                                self.skid_sound.volume = self.volume / 2
                                self.skid_sound.play()
                            self.start_trail = False
                            self.drifting = True
                        else:
                            self.drifting = False
                    elif self.drift_speed > self.min_drift_speed + 2 and not self.start_trail:
                        if self.pivot_rotation_distance < 60 or self.pivot_rotation_distance > -60:
                            for trail in self.trails:
                                if trail.trailing:
                                    trail.end_trail()
                            if self.audio:
                                self.skid_sound.stop(False)
                            self.start_trail = True
                            self.drifting = False
                        self.drifting = False
                    if self.speed < 10:
                        self.drifting = False
            else:
                self.driving = False
                if self.speed > 1:
                    self.speed -= self.friction * 5 * time.dt
                elif self.speed < -1:
                    self.speed += self.friction * 5 * time.dt
                self.camera_rotation += self.friction * 20 * time.dt

            # Braking
            if held_keys[self.controls[2]] or held_keys["down arrow"]:
                self.speed -= self.braking_strenth * time.dt
                self.drift_speed -= 20 * time.dt
                self.braking = True
            else:
                self.braking = False

            # Audio
            if self.driving or self.braking:
                if self.start_sound and self.audio:
                    if not self.drive_sound.playing:
                        self.drive_sound.loop = True
                        self.drive_sound.play()
                    if not self.dirt_sound.playing:
                        self.drive_sound.loop = True
                        self.dirt_sound.play()
                    self.start_sound = False

                if self.speed > 0:
                    self.drive_sound.volume = self.speed / 80 * self.volume
                elif self.speed < 0:
                    self.drive_sound.volume = -self.speed / 80 * self.volume

                if self.pivot_rotation_distance > 0:
                    self.dirt_sound.volume = self.pivot_rotation_distance / 110 * self.volume
                elif self.pivot_rotation_distance < 0:
                    self.dirt_sound.volume = -self.pivot_rotation_distance / 110 * self.volume
            else:
                self.drive_sound.volume -= 0.5 * time.dt
                self.dirt_sound.volume -= 0.5 * time.dt
                if self.skid_sound.playing:
                    self.skid_sound.stop(False)

            # Hand Braking
            if held_keys[self.hand_brake_control]:
                if self.rotation_speed < 0:
                    self.rotation_speed -= 3 * time.dt
                elif self.rotation_speed > 0:
                    self.rotation_speed += 3 * time.dt
                self.drift_speed -= 40 * time.dt
                self.speed -= 20 * time.dt
                self.max_rotation_speed = 3.0

        # If Car is not hitting the ground, stop the trail
        if self.graphics != "ultra fast":
            if y_ray.distance > 2.5:
                if self.trail_renderer1.trailing:
                    for trail in self.trails:
                        trail.end_trail()
                    self.start_trail = True

        # Steering
        self.rotation_y += self.rotation_speed * 50 * time.dt

        if self.rotation_speed > 0:
            self.rotation_speed -= self.speed / 6 * time.dt
        elif self.rotation_speed < 0:
            self.rotation_speed += self.speed / 6 * time.dt

        if self.speed > 1 or self.speed < -1:
            if held_keys[self.controls[1]] or held_keys["left arrow"]:
                self.rotation_speed -= self.steering_amount * time.dt
                self.drift_speed -= 5 * time.dt
                if self.speed > 1:
                    self.speed -= self.turning_speed * time.dt
                elif self.speed < 0:
                    self.speed += self.turning_speed / 5 * time.dt
            elif held_keys[self.controls[3]] or held_keys["right arrow"]:
                self.rotation_speed += self.steering_amount * time.dt
                self.drift_speed -= 5 * time.dt
                if self.speed > 1:
                    self.speed -= self.turning_speed * time.dt
                elif self.speed < 0:
                    self.speed += self.turning_speed / 5 * time.dt
            else:
                self.drift_speed += 15 * time.dt
                if self.rotation_speed > 0:
                    self.rotation_speed -= 5 * time.dt
                elif self.rotation_speed < 0:
                    self.rotation_speed += 5 * time.dt
        else:
            self.rotation_speed = 0

        # Cap the speed
        if self.speed >= self.topspeed:
            self.speed = self.topspeed
        if self.speed <= -15:
            self.speed = -15
        if self.speed <= 0:
            self.pivot.rotation_y = self.rotation_y

        # Cap the drifting
        if self.drift_speed <= self.min_drift_speed:
            self.drift_speed = self.min_drift_speed
        if self.drift_speed >= self.max_drift_speed:
            self.drift_speed = self.max_drift_speed

        # Cap the steering
        if self.rotation_speed >= self.max_rotation_speed:
            self.rotation_speed = self.max_rotation_speed
        if self.rotation_speed <= -self.max_rotation_speed:
            self.rotation_speed = -self.max_rotation_speed

        # Respawn
        if held_keys[self.respawn_control]:
            self.reset_car()

        # Reset the car's position if y value is less than -100
        if self.y <= -100:
            self.reset_car()

        # Reset the car's position if y value is greater than 300
        if self.y >= 300:
            self.reset_car()

        # Cap the camera rotation
        if self.camera_rotation >= 40:
            self.camera_rotation = 40
        elif self.camera_rotation <= 30:
            self.camera_rotation = 30

        # Camera Shake
        if self.speed >= 1 and self.driving:
            self.can_shake = True
            if self.pivot_rotation_distance > 0:
                self.shake_amount = self.speed * self.pivot_rotation_distance / 200
            elif self.pivot_rotation_distance < 0:
                self.shake_amount = self.speed * -self.pivot_rotation_distance / 200
        else:
            self.can_shake = False

        # Cap the camera shake amount
        if self.shake_amount <= 0:
            self.shake_amount = 0
        if self.shake_amount >= 0.03:
            self.shake_amount = 0.03

        # If the camera can shake and camera shake is on, then shake the camera
        if self.can_shake and self.camera_shake_option and self.camera_angle != "first-person":
            self.shake_camera()

        # Rotation
        self.rotation_parent.position = self.position

        # Lerps the car's rotation to the rotation parent's rotation (Makes it smoother)
        self.rotation_x = lerp(self.rotation_x, self.rotation_parent.rotation_x, 20 * time.dt)
        self.rotation_z = lerp(self.rotation_z, self.rotation_parent.rotation_z, 20 * time.dt)

        # Check if car is hitting the ground
        if self.visible:
            if y_ray.distance <= self.scale_y * 1.7 + abs(movementY):
                self.velocity_y = 0
                # Check if hitting a wall or steep slope
                if y_ray.world_normal.y > 0.7 and y_ray.world_point.y - self.world_y < 0.5:
                    # Set the y value to the ground's y value
                    self.y = y_ray.world_point.y + 1.4
                    self.hitting_wall = False
                else:
                    # Car is hitting a wall
                    self.hitting_wall = True

                if self.copy_normals:
                    self.ground_normal = self.position + y_ray.world_normal
                else:
                    self.ground_normal = self.position + (0, 180, 0)

                # Rotates the car according to the grounds normals
                if not self.hitting_wall:
                    self.rotation_parent.look_at(self.ground_normal, axis = "up")
                    self.rotation_parent.rotate((0, self.rotation_y + 180, 0))
                else:
                    self.rotation_parent.rotation = self.rotation

                if self.start_fall and self.audio:
                    self.hit_sound.volume = self.volume / 2
                    self.hit_sound.play()
                    self.start_fall = False
            else:
                self.y += movementY * 50 * time.dt
                self.velocity_y -= 50 * time.dt
                self.rotation_parent.rotation = self.rotation
                self.start_fall = True

        # Movement
        movementX = self.pivot.forward[0] * self.speed * time.dt
        movementZ = self.pivot.forward[2] * self.speed * time.dt

        # Collision Detection
        if movementX != 0:
            direction = (sign(movementX), 0, 0)
            x_ray = raycast(origin = self.world_position, direction = direction, ignore = [self, ])

            if x_ray.distance > self.scale_x / 2 + abs(movementX):
                self.x += movementX

        if movementZ != 0:
            direction = (0, 0, sign(movementZ))
            z_ray = raycast(origin = self.world_position, direction = direction, ignore = [self, ])

            if z_ray.distance > self.scale_z / 2 + abs(movementZ):
                self.z += movementZ

    def reset_car(self):
        """
        Resets the car
        """
        if self.sand_track.enabled:
            self.position = (-63, -40, -7)
            self.rotation = (0, 90, 0)
        elif self.grass_track.enabled:
            self.position = (-80, -30, 18.5)
            self.rotation = (0, 90, 0)
        elif self.snow_track.enabled:
            self.position = (-5, -35, 93)
            self.rotation = (0, 90, 0)
        elif self.forest_track.enabled:
            self.position = (12, -35, 76)
            self.rotation = (0, 90, 0)
        elif self.savannah_track.enabled:
            self.position = (-14, -35, 42)
            self.rotation = (0, 90, 0)
        elif self.lake_track.enabled:
            self.position = (-121, -40, 158)
            self.rotation = (0, 90, 0)
        camera.world_rotation_y = self.rotation_y
        self.speed = 0
        self.velocity_y = 0
        self.anti_cheat = 1
        self.timer_running = False
        if self.gamemode == "race":
            self.count = 0.0
            self.reset_count = 0.0
        elif self.gamemode == "time trial":
            self.count = 100.0
            self.reset_count = 100.0
            self.laps = 0
            self.start_time = False
        elif self.gamemode == "drift":
            self.reset_drift_score()
        for trail in self.trails:
            if trail.trailing:
                trail.end_trail()
        self.start_trail = True
        self.start_sound = True
        if self.audio:
            if self.skid_sound.playing:
                self.skid_sound.stop(False)
            if self.dirt_sound.playing:
                self.dirt_sound.stop(False)

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

    def check_highscore(self):
        """
        Checks if the score is lower than the highscore
        """
        if self.gamemode == "race":
            self.last_count = self.count
            self.reset_count = 0.0
            self.timer.disable()
            self.reset_count_timer.enable()

            if self.highscore_count == 0:
                if self.last_count >= 5:
                    self.highscore_count = self.last_count
                    self.animate_text(self.highscore)
            if self.last_count <= self.highscore_count and self.last_count != 0:
                if self.last_count >= 5:
                    self.highscore_count = self.last_count
                    self.animate_text(self.highscore)
                if self.highscore_count <= 6:
                    self.highscore_count = self.last_count
                    self.animate_text(self.highscore)

            if self.sand_track.enabled:
                self.sand_track_hs = float(self.highscore_count)
            elif self.grass_track.enabled:
                self.grass_track_hs = float(self.highscore_count)
            elif self.snow_track.enabled:
                self.snow_track_hs = float(self.highscore_count)
            elif self.forest_track.enabled:
                self.forest_track_hs = float(self.highscore_count)
            elif self.savannah_track.enabled:
                self.savannah_track_hs = float(self.highscore_count)
            elif self.lake_track.enabled:
                self.lake_track_hs = float(self.highscore_count)
            self.save_highscore()

        elif self.gamemode == "time trial":
            self.last_count = self.count
            if self.start_time:
                self.laps += 1
                self.animate_text(self.laps_text, 1.7, 1.1)
            self.start_time = True

        elif self.gamemode == "drift":
            self.drift_score += self.count

            if self.drift_score >= self.highscore_count:
                self.highscore_count = self.drift_score
                if self.highscore_count != 0:
                    self.animate_text(self.highscore)

            self.reset_count = self.drift_score
            self.reset_count_timer.enable()
            self.timer.disable()
            invoke(self.reset_count_timer.disable, delay = 3)
            invoke(self.timer.enable, delay = 3)

            self.reset_drift_score()
            
            self.highscore.text = str(int(self.highscore_count))
            
            if self.sand_track.enabled:
                self.sand_track_drift = int(self.highscore_count)
            elif self.grass_track.enabled:
                self.grass_track_drift = int(self.highscore_count)
            elif self.snow_track.enabled:
                self.snow_track_drift = int(self.highscore_count)
            elif self.forest_track.enabled:
                self.forest_track_drift = int(self.highscore_count)
            elif self.savannah_track.enabled:
                self.savannah_track_drift = int(self.highscore_count)
            elif self.lake_track.enabled:
                self.lake_track_drift = int(self.highscore_count)

            self.save_highscore()

    def save_highscore(self):
        """
        Saves the highscore to a json file
        """
        self.highscore_dict = {
            "race": {
                "sand_track": self.sand_track_hs,
                "grass_track": self.grass_track_hs,
                "snow_track": self.snow_track_hs,
                "forest_track": self.forest_track_hs,
                "savannah_track": self.savannah_track_hs,
                "lake_track": self.lake_track_hs
            },
            
            "time_trial": {
                "sand_track": self.sand_track_laps,
                "grass_track": self.grass_track_laps, 
                "snow_track": self.snow_track_laps, 
                "forest_track": self.forest_track_laps,
                "savannah_track": self.savannah_track_laps,
                "lake_track": self.lake_track_laps
            },

            "drift": {
                "sand_track": self.sand_track_drift,
                "grass_track": self.grass_track_drift, 
                "snow_track": self.snow_track_drift, 
                "forest_track": self.forest_track_drift,
                "savannah_track": self.savannah_track_drift,
                "lake_track": self.lake_track_drift
            }
        }

        with open(self.highscore_path, "w") as hs:
            json.dump(self.highscore_dict, hs, indent = 4)

    def reset_highscore(self):
        """
        Resets all of the highscores
        """
        self.sand_track_hs = 0.0
        self.grass_track_hs = 0.0
        self.snow_track_hs = 0.0
        self.forest_track_hs = 0.0
        self.savannah_track_hs = 0.0
        self.lake_track_hs = 0.0

        self.sand_track_laps = 0
        self.grass_track_laps = 0
        self.snow_track_laps = 0
        self.forest_track_laps = 0
        self.savannah_track_laps = 0
        self.lake_track_laps = 0

        self.sand_track_drift = 0.0
        self.grass_track_drift = 0.0
        self.snow_track_drift = 0.0
        self.forest_track_drift = 0.0
        self.savannah_track_drift = 0.0
        self.lake_track_drift = 0.0

        self.save_highscore()

    def set_unlocked(self):
        """
        Declares variables with data from a json file
        """
        self.sand_track.unlocked = self.unlocked["tracks"]["sand_track"]
        self.grass_track.unlocked = self.unlocked["tracks"]["grass_track"]
        self.snow_track.unlocked = self.unlocked["tracks"]["snow_track"]
        self.forest_track.unlocked = self.unlocked["tracks"]["forest_track"]
        self.savannah_track.unlocked = self.unlocked["tracks"]["savannah_track"]
        self.lake_track.unlocked = self.unlocked["tracks"]["lake_track"]

        self.beat_mandaw_sand_track = self.unlocked["beat_mandaw"]["sand_track"]
        self.beat_mandaw_grass_track = self.unlocked["beat_mandaw"]["grass_track"]
        self.beat_mandaw_snow_track = self.unlocked["beat_mandaw"]["snow_track"]
        self.beat_mandaw_forest_track = self.unlocked["beat_mandaw"]["forest_track"]
        self.beat_mandaw_savannah_track = self.unlocked["beat_mandaw"]["savannah_track"]
        self.beat_mandaw_lake_track = self.unlocked["beat_mandaw"]["lake_track"]

        self.sports_unlocked = self.unlocked["cars"]["sports_car"]
        self.muscle_unlocked = self.unlocked["cars"]["muscle_car"]
        self.limo_unlocked = self.unlocked["cars"]["limo"]
        self.lorry_unlocked = self.unlocked["cars"]["lorry"]
        self.hatchback_unlocked = self.unlocked["cars"]["hatchback"]
        self.rally_unlocked = self.unlocked["cars"]["rally_car"]

        self.sports_red_unlocked = self.unlocked["textures"]["sports_car"]["red"]
        self.sports_blue_unlocked = self.unlocked["textures"]["sports_car"]["blue"]
        self.sports_green_unlocked = self.unlocked["textures"]["sports_car"]["green"]
        self.sports_orange_unlocked = self.unlocked["textures"]["sports_car"]["orange"]
        self.sports_black_unlocked = self.unlocked["textures"]["sports_car"]["black"]
        self.sports_white_unlocked = self.unlocked["textures"]["sports_car"]["white"]

        self.muscle_red_unlocked = self.unlocked["textures"]["muscle_car"]["red"]
        self.muscle_blue_unlocked = self.unlocked["textures"]["muscle_car"]["blue"]
        self.muscle_green_unlocked = self.unlocked["textures"]["muscle_car"]["green"]
        self.muscle_orange_unlocked = self.unlocked["textures"]["muscle_car"]["orange"]
        self.muscle_black_unlocked = self.unlocked["textures"]["muscle_car"]["black"]
        self.muscle_white_unlocked = self.unlocked["textures"]["muscle_car"]["white"]

        self.limo_red_unlocked = self.unlocked["textures"]["limo"]["red"]
        self.limo_blue_unlocked = self.unlocked["textures"]["limo"]["blue"]
        self.limo_green_unlocked = self.unlocked["textures"]["limo"]["green"]
        self.limo_orange_unlocked = self.unlocked["textures"]["limo"]["orange"]
        self.limo_black_unlocked = self.unlocked["textures"]["limo"]["black"]
        self.limo_white_unlocked = self.unlocked["textures"]["limo"]["white"]

        self.lorry_red_unlocked = self.unlocked["textures"]["lorry"]["red"]
        self.lorry_blue_unlocked = self.unlocked["textures"]["lorry"]["blue"]
        self.lorry_green_unlocked = self.unlocked["textures"]["lorry"]["green"]
        self.lorry_orange_unlocked = self.unlocked["textures"]["lorry"]["orange"]
        self.lorry_black_unlocked = self.unlocked["textures"]["lorry"]["black"]
        self.lorry_white_unlocked = self.unlocked["textures"]["lorry"]["white"]

        self.hatchback_red_unlocked = self.unlocked["textures"]["hatchback"]["red"]
        self.hatchback_blue_unlocked = self.unlocked["textures"]["hatchback"]["blue"]
        self.hatchback_green_unlocked = self.unlocked["textures"]["hatchback"]["green"]
        self.hatchback_orange_unlocked = self.unlocked["textures"]["hatchback"]["orange"]
        self.hatchback_black_unlocked = self.unlocked["textures"]["hatchback"]["black"]
        self.hatchback_white_unlocked = self.unlocked["textures"]["hatchback"]["white"]

        self.rally_red_unlocked = self.unlocked["textures"]["rally_car"]["red"]
        self.rally_blue_unlocked = self.unlocked["textures"]["rally_car"]["blue"]
        self.rally_green_unlocked = self.unlocked["textures"]["rally_car"]["green"]
        self.rally_orange_unlocked = self.unlocked["textures"]["rally_car"]["orange"]
        self.rally_black_unlocked = self.unlocked["textures"]["rally_car"]["black"]
        self.rally_white_unlocked = self.unlocked["textures"]["rally_car"]["white"]

        self.viking_helmet_unlocked = self.unlocked["cosmetics"]["viking_helmet"]
        self.duck_unlocked = self.unlocked["cosmetics"]["duck"]
        self.banana_unlocked = self.unlocked["cosmetics"]["banana"]
        self.surfinbird_unlocked = self.unlocked["cosmetics"]["surfinbird"]

        self.drift_unlocked = self.unlocked["gamemodes"]["drift"]

    def save_unlocked(self):
        """
        Saves the unlocks to a json file
        """
        self.unlocked_dict = {
            "tracks": {
                "sand_track": self.sand_track.unlocked,
                "grass_track": self.grass_track.unlocked,
                "snow_track": self.snow_track.unlocked,
                "forest_track": self.forest_track.unlocked,
                "savannah_track": self.savannah_track.unlocked,
                "lake_track": self.lake_track.unlocked
            },
            "beat_mandaw": {
                "sand_track": self.beat_mandaw_sand_track,
                "grass_track": self.beat_mandaw_grass_track,
                "snow_track": self.beat_mandaw_snow_track,
                "forest_track": self.beat_mandaw_forest_track,
                "savannah_track": self.beat_mandaw_savannah_track,
                "lake_track": self.beat_mandaw_lake_track
            },
            "cars": {
                "sports_car": self.sports_unlocked,
                "muscle_car": self.muscle_unlocked,
                "limo": self.limo_unlocked,
                "lorry": self.lorry_unlocked,
                "hatchback": self.hatchback_unlocked,
                "rally_car": self.rally_unlocked
            },
            "textures": {
                "sports_car": {
                    "red": self.sports_red_unlocked,
                    "blue": self.sports_blue_unlocked,
                    "green": self.sports_green_unlocked,
                    "orange": self.sports_orange_unlocked,
                    "black": self.sports_black_unlocked,
                    "white": self.sports_white_unlocked
                },
                "muscle_car": {
                    "red": self.muscle_red_unlocked,
                    "blue": self.muscle_blue_unlocked,
                    "green": self.muscle_green_unlocked,
                    "orange": self.muscle_orange_unlocked,
                    "black": self.muscle_black_unlocked,
                    "white": self.muscle_white_unlocked
                },
                "limo": {
                    "red": self.limo_red_unlocked,
                    "blue": self.limo_blue_unlocked,
                    "green": self.limo_green_unlocked,
                    "orange": self.limo_orange_unlocked,
                    "black": self.limo_black_unlocked,
                    "white": self.limo_white_unlocked
                },
                "lorry": {
                    "red": self.lorry_red_unlocked,
                    "blue": self.lorry_blue_unlocked,
                    "green": self.lorry_green_unlocked,
                    "orange": self.lorry_orange_unlocked,
                    "black": self.lorry_black_unlocked,
                    "white": self.lorry_white_unlocked
                },
                "hatchback": {
                    "red": self.hatchback_red_unlocked,
                    "blue": self.hatchback_blue_unlocked,
                    "green": self.hatchback_green_unlocked,
                    "orange": self.hatchback_orange_unlocked,
                    "black": self.hatchback_black_unlocked,
                    "white": self.hatchback_white_unlocked
                },
                "rally_car": {
                    "red": self.rally_red_unlocked,
                    "blue": self.rally_blue_unlocked,
                    "green": self.rally_green_unlocked,
                    "orange": self.rally_orange_unlocked,
                    "black": self.rally_black_unlocked,
                    "white": self.rally_white_unlocked
                }
            },
            "cosmetics": {
                "viking_helmet": self.viking_helmet_unlocked,
                "duck": self.duck_unlocked,
                "banana": self.banana_unlocked,
                "surfinbird": self.surfinbird_unlocked
            },
            "gamemodes": {
                "drift": self.drift_unlocked
            }
        }

        with open(self.unlocked_json, "w") as hs:
            json.dump(self.unlocked_dict, hs, indent = 4)
    
    def reset_timer(self):
        """
        Resets the timer
        """
        self.count = self.reset_count
        self.timer.enable()
        self.reset_count_timer.disable()

    def reset_drift(self):
        """
        Resets the drift
        """
        self.animate_text(self.drift_text, 1.7, 1.1)
        invoke(self.drift_text.animate_position, (-0.8, 0.43), 0.3, curve = curve.out_expo, delay = 0.3)
        invoke(self.reset_drift_text, delay = 0.4)
        self.drift_swush.play()
        self.get_hundred = False
        self.get_thousand = False
        self.get_fivethousand = False

    def reset_drift_text(self):
        """
        Resets the drift text
        """
        self.drift_score += self.count
        self.drift_multiplier = 20
        self.count = 0
        self.drifting = False
        invoke(setattr, self.drift_text, "visible", False, delay = 0.1)
        invoke(setattr, self.drift_text, "position", (0, 0.43), delay = 0.3)

    def reset_drift_score(self):
        self.count = 0
        self.drift_score = 0
        self.drift_multiplier = 20
        self.drifting = False

        if self.sand_track.enabled:
            self.drift_time = 25.0
        elif self.grass_track.enabled:
            self.drift_time = 30.0
        elif self.snow_track.enabled:
            self.drift_time = 50.0
        elif self.forest_track.enabled:
            self.drift_time = 40.0
        elif self.savannah_track.enabled:
            self.drift_time = 25.0
        elif self.lake_track.enabled:
            self.drift_time = 75.0

    def animate_text(self, text, top = 1.2, bottom = 0.6):
        """
        Animates the scale of text
        """
        if self.gamemode != "drift":
            if self.last_count > 1:
                text.animate_scale((top, top, top), curve = curve.out_expo)
                invoke(text.animate_scale, (bottom, bottom, bottom), delay = 0.2)
        else:
            text.animate_scale((top, top, top), curve = curve.out_expo)
            invoke(text.animate_scale, (bottom, bottom, bottom), delay = 0.2)

    def shake_camera(self):
        """
        Camera shake
        """
        camera.x += random.randint(-1, 1) * self.shake_amount
        camera.y += random.randint(-1, 1) * self.shake_amount
        camera.z += random.randint(-1, 1) * self.shake_amount

    def update_model_path(self):
        """
        Updates the model's file path for multiplayer
        """
        self.model_path = str(self.model).replace("render/scene/car/", "")
        invoke(self.update_model_path, delay = 3)

# Class for copying the car's position, rotation for multiplayer
class CarRepresentation(Entity):
    def __init__(self, car, position = (0, 0, 0), rotation = (0, 65, 0)):
        super().__init__(
            parent = scene,
            model = "sports-car.obj",
            texture = "sports-red.png",
            position = position,
            rotation = rotation,
            scale = (1, 1, 1)
        )

        self.model_path = str(self.model).replace("render/scene/car_representation/", "")
        
        self.viking_helmet = Entity(model = "viking_helmet.obj", texture = "viking_helmet.png", parent = self)
        self.duck = Entity(model = "duck.obj", parent = self)
        self.banana = Entity(model = "banana.obj", parent = self)
        self.surfinbird = Entity(model = "surfinbird.obj", texture = "surfinbird.png", parent = self)
        self.surfboard = Entity(model = "surfboard.obj", texture = "surfboard.png", parent = self.surfinbird)
        self.viking_helmet.disable()
        self.duck.disable()
        self.banana.disable()
        self.surfinbird.disable()

        self.cosmetics = [self.viking_helmet, self.duck, self.banana, self.surfinbird]

        self.text_object = None
        self.highscore = 0.0

        invoke(self.update_representation, delay = 5)

    def update_representation(self):
        for cosmetic in self.cosmetics:
            if cosmetic.enabled:
                if self.model_path == "lorry.obj":
                    cosmetic.y = 1.5
                elif self.model_path == "limo.obj":
                    cosmetic.y = 0.1
                elif self.model_path == "sports-car.obj" or self.model_path == "muscle-car.obj":
                    cosmetic.y = 0

        invoke(self.update_representation, delay = 5)

# Username shown above the car
class CarUsername(Text):
    def __init__(self, car):
        super().__init__(
            parent = car,
            text = "Guest",
            y = 3,
            scale = 30,
            color = color.white,
            billboard = True
        )
    
        self.username_text = "Guest"

    def update(self):
        self.text = self.username_text