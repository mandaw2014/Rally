from ursina import *

class SandTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "sand_track.obj", 
            texture = "sand_track.png", 
            position = (-80, -50, -75), 
            scale = (18, 18, 18), 
            rotation = (0, 270, 0),
            collider = "mesh"
        )

        self.car = car

        self.finish_line = Entity(model = "cube", position = (-50, -50.2, -7), collider = "box", rotation = (0, 90, 0), scale = (30, 8, 3), visible = False)
        self.boundaries = Entity(model = "sand_track_bounds.obj", collider = "mesh", position = (-80, -50, -75), rotation = (0, 270, 0), scale = (18, 50, 18), visible = False)

        self.wall1 = Entity(model = "cube", position = (-75, 450, -48), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall2 = Entity(model = "cube", position = (-74, 450, -75), rotation = (0, 90, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall3 = Entity(model = "cube", position = (-61, 450, -60), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 40), visible = False)
        self.wall4 = Entity(model = "cube", position = (-90, 450, -60), rotation = (0, 0, 0), collider = "box", scale = (5, 2000, 40), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (-100, -50, -114), rotation = (0, 90, 0), collider = "box", scale = (30, 100, 5), visible = False)

        self.track = [
            self.finish_line, self.boundaries, self.wall1, self.wall2, self.wall3, 
            self.wall4, self.wall_trigger
        ]
        
        self.disable()

        for i in self.track:
            i.disable()

        self.played = False

    def update(self):
        if self.enabled == True:
            if self.car.intersects(self.finish_line):
                if self.car.anti_cheat == 1:
                    self.car.timer_running = True
                    self.car.last_count = self.car.count
                    self.car.anti_cheat = 0
                    invoke(self.car.reset_timer, delay = 3)

                    if self.car.time_trial == False:
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

                        self.car.sand_track_hs = float(self.car.highscore_count)
                        self.car.save_highscore()

                    elif self.car.time_trial:
                        if self.car.start_time:
                            self.car.laps += 1
                        self.car.start_time = True

                    self.wall1.enable()
                    self.wall2.enable()
                    self.wall3.disable()
                    self.wall4.disable()

            if self.car.intersects(self.wall_trigger):
                self.wall1.disable()
                self.wall2.disable()
                self.wall3.enable()
                self.wall4.enable()
                self.car.anti_cheat = 1