from ursina import *

class GrassTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "grass_track.obj", 
            texture = "grass_track.png", 
            position = (0, -50, 0), 
            rotation = (0, 270, 0), 
            scale = (25, 25, 25), 
            collider = "mesh"
        )

        self.car = car

        self.finish_line = Entity(model = "cube", position = (-62, -40.2, 15.8), collider = "box", rotation = (0, 90, 0), scale = (30, 8, 3), visible = False)
        self.boundaries = Entity(model = "grass_track_bounds.obj", collider = "mesh", position = (0, -50, 0), rotation = (0, 270, 0), scale = (25, 25, 25), visible = False)

        self.wall1 = Entity(model = "cube", position = (-5, 450, 35), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall2 = Entity(model = "cube", position = (20, 450, 1), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 150), visible = False)
        self.wall3 = Entity(model = "cube", position = (-21, 450, 15), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall4 = Entity(model = "cube", position = (9, 450, 14), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (25, -40.2, 65), collider = "box", rotation = (0, 90, 0), scale = (40, 20, 3), visible = False)
        self.wall_trigger_ramp = Entity(model = "cube", position = (-82, -34, -64), collider = "box", rotation = (0, 90, 0), scale = (40, 20, 3), visible = False)

    def update(self):
        if self.enabled == True:
            if self.car.intersects(self.finish_line):
                if self.car.anti_cheat == 1:
                    self.car.timer_running = True
                    self.car.last_count = self.car.count
                    self.car.reset_count = 0.0
                    self.car.timer.disable()
                    self.car.reset_count_timer.enable()

                    if self.car.highscore_count == 0:
                        if self.car.last_count >= 10:
                            self.car.highscore_count = self.car.last_count
                    if self.car.last_count <= self.car.highscore_count:
                        if self.car.last_count >= 10.0:
                            self.car.highscore_count = self.car.last_count
                        if self.car.highscore_count <= 13:
                            self.car.highscore_count = self.car.last_count

                    with open(self.car.highscore_path_grass, "w") as hs:
                        hs.write(str(self.car.highscore_count))

                    self.car.anti_cheat = 0

                    invoke(self.car.reset_timer, delay = 3)

                self.wall1.enable()
                self.wall2.enable()
                self.wall3.disable()
                self.wall4.disable()

            if self.car.intersects(self.boundaries):
                self.car.speed = 10

            if self.car.intersects(self.wall_trigger):
                self.wall1.disable()
                self.wall2.disable()
                self.wall3.enable()
                self.wall4.enable()
                self.car.anti_cheat = 0.5

            if self.car.intersects(self.wall_trigger):
                if self.car.anti_cheat == 0.5:
                    self.car.anti_cheat = 1