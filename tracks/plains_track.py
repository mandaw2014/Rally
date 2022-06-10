from ursina import *

class PlainsTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "plains_track.obj", 
            texture = "plains_track.png", 
            position = (0, -50, 0), 
            rotation = (0, 270, 0), 
            scale = (12, 12, 12), 
            collider = "mesh"
        )

        self.car = car

        self.finish_line = Entity(model = "cube", position = (31, -48, 72), collider = "box", rotation = (0, 90, 0), scale = (30, 8, 3), visible = False)
        self.boundaries = Entity(model = "plains_track_bounds.obj", collider = "mesh", position = (0, -50, 0), rotation = (0, 270, 0), scale = (12, 12, 12), visible = False)

        self.wall1 = Entity(model = "cube", position = (-16, 450, 50), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall2 = Entity(model = "cube", position = (-16, 450, 23), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall3 = Entity(model = "cube", position = (5, 450, 33), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall4 = Entity(model = "cube", position = (-34, 450, 33), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall5 = Entity(model = "cube", position = (-18, 450, 0), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall6 = Entity(model = "cube", position = (-18, 450, -30), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall7 = Entity(model = "cube", position = (-4, 450, -15), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)
        self.wall8 = Entity(model = "cube", position = (-30, 450, -15), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 50), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (11, -45, -70), collider = "box", rotation = (0, 90, 0), scale = (40, 20, 3), visible = False)

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
        self.wall_trigger.disable()

        self.played = False

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

                    with open(self.car.highscore_path_plains, "w") as hs:
                        hs.write(str(self.car.highscore_count))

                    self.car.highscore_count = float(self.car.highscore_count)

                    self.car.anti_cheat = 0

                    invoke(self.car.reset_timer, delay = 3)

                    self.wall1.enable()
                    self.wall2.enable()
                    self.wall3.disable()
                    self.wall4.disable()
                    self.wall5.enable()
                    self.wall6.enable()
                    self.wall7.disable()
                    self.wall8.disable()

            if self.car.intersects(self.wall_trigger):
                if self.car.anti_cheat == 0:
                    self.wall1.disable()
                    self.wall2.disable()
                    self.wall3.enable()
                    self.wall4.enable()
                    self.wall5.disable()
                    self.wall6.disable()
                    self.wall7.enable()
                    self.wall8.enable()
                    
                    self.car.anti_cheat = 1