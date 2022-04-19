from ursina import *

class SnowTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "snow_track.obj",
            texture = "snow_track.png",
            position = (0, -50, 0),
            rotation = (0, 90, 0),
            collider = "mesh",
            scale = (8, 8, 8)
        )

        self.car = car

        self.finish_line = Entity(model = "cube", position = (11, -42, 90), collider = "box", rotation = (0, 90, 0), scale = (30, 8, 3), visible = False)
        self.boundaries = Entity(model = "snow_track_bounds.obj", collider = "mesh", rotation = (0, 90, 0), position = (0, 0, 0), scale = (8, 30, 8), visible = False)

        self.wall1 = Entity(model = "cube", position = (-10, 450, 38), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall2 = Entity(model = "cube", position = (-36, 450, 38), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall3 = Entity(model = "cube", position = (-21, 450, 54), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall4 = Entity(model = "cube", position = (-21, 450, 28), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall5 = Entity(model = "cube", position = (-10, 450, -10), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall6 = Entity(model = "cube", position = (-36, 450, -10), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall7 = Entity(model = "cube", position = (-21, 450, 8), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall8 = Entity(model = "cube", position = (-21, 450, -28), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False) 
        self.wall9 = Entity(model = "cube", position = (-36, 450, 84), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 45), visible = False)
        self.wall10 = Entity(model = "cube", position = (-10, 450, 100), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 70), visible = False)
        self.wall11 = Entity(model = "cube", position = (-20, 450, 105), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 30), visible = False)
        self.wall12 = Entity(model = "cube", position = (-20, 450, 76), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 30), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (29, -40.2, -51), collider = "box", rotation = (0, 90, 0), scale = (35, 20, 3), visible = False)
        self.wall_trigger_end = Entity(model = "cube", position = (-70, -40.2, 100), collider = "box", rotation = (0, 0, 0), scale = (35, 20, 3), visible = False)

        self.disable()
        self.finish_line.disable()
        self.boundaries.disable()
        self.wall1.disable()
        self.wall2.disable()
        self.wall3.disable()
        self.wall4.disable()
        self.wall5.disable()
        self.wall6.disable()
        self.wall7.disable()
        self.wall8.disable()
        self.wall9.disable()
        self.wall10.disable()
        self.wall11.disable()
        self.wall12.disable()
        self.wall_trigger.disable()
        self.wall_trigger_end.disable()

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

                    with open(self.car.highscore_path_snow, "w") as hs:
                        hs.write(str(self.car.highscore_count))

                    self.car.anti_cheat = 0

                    self.wall1.disable()
                    self.wall2.disable()
                    self.wall3.enable()
                    self.wall4.enable()
                    self.wall5.disable()
                    self.wall6.disable()
                    self.wall7.enable()
                    self.wall8.enable()
                    self.wall9.enable()
                    self.wall10.enable()
                    self.wall11.disable()
                    self.wall12.disable()

                    invoke(self.car.reset_timer, delay = 3)

            if self.car.intersects(self.wall_trigger):
                self.wall1.enable()
                self.wall2.enable()
                self.wall3.disable()
                self.wall4.disable()
                self.wall5.enable()
                self.wall6.enable()
                self.wall7.disable()
                self.wall8.disable()
                self.wall9.enable()
                self.wall10.enable()
                self.wall11.disable()
                self.wall12.disable()
                self.car.anti_cheat = 0.5
            
            if self.car.intersects(self.wall_trigger_end):
                self.wall9.disable()
                self.wall10.disable()
                self.wall11.enable()
                self.wall12.enable()
                if self.car.anti_cheat == 0.5:
                    self.car.anti_cheat = 1