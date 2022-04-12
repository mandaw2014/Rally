from ursina import *

class SandTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "sand_track.obj", 
            texture = "sand_track.png", 
            position = (-80, -50, -75), 
            scale = (10, 10, 10), 
            collider = "mesh"
        )

        self.car = car

        self.finish_line = Entity(position = (24, -44.5, 7), collider = "box", rotation = (0, -251, 0), scale = (20, 5, 3), visible = False)
        self.boundaries = Entity(model = "sand_track_bounds.obj", collider = "mesh", position = (-80, -50, -75), scale = (10, 10, 10), visible = False)

        self.wall1 = Entity(model = "cube", position = (-29, 450, -39.8), rotation = (0, 313, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall2 = Entity(model = "cube", position = (-40, 450, -71.8), rotation = (0, 325, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall3 = Entity(model = "cube", position = (-15, 450, -69.5), rotation = (0, 566.549, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall4 = Entity(model = "cube", position = (-43, 450, -41.6), rotation = (0, 751.312, 0), collider = "box", scale = (5, 2000, 40), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (-72, 450, -84.9), rotation = (0, 447.72, 0), collider = "box", scale = (50, 2000, 5), visible = False)

        self.disable()
        self.finish_line.disable()
        self.boundaries.disable()
        self.wall1.disable()
        self.wall2.disable()
        self.wall3.disable()
        self.wall4.disable()
        self.wall_trigger.disable()

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

                    with open(self.car.highscore_path_sand, "w") as hs:
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
                self.car.anti_cheat = 1