from ursina import *

class SavannahTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "savannah_track.obj", 
            texture = "savannah_track.png", 
            position = (0, -50, 0), 
            rotation = (0, 270, 0), 
            scale = (27, 27, 27), 
            collider = "mesh"
        )

        self.car = car

        self.finish_line = Entity(model = "cube", position = (3, -50, 41), collider = "box", rotation = (0, 0, 0), scale = (3, 8, 30), visible = False)
        self.boundaries = Entity(model = "savannah_track_bounds.obj", collider = "mesh", position = (0, -50, 0), rotation = (0, 270, 0), scale = (27, 27, 27), visible = False)
        self.wall_trigger = Entity(model = "cube", position = (-63, -48, -47), collider = "box", rotation = (0, 0, 0), scale = (50, 20, 3), visible = False)

        self.rocks = Entity(model = "rocks-savannah", texture = "rock-savannah", y = -50, rotation_y = 270, scale = 27)

        self.track = [
            self.finish_line, self.boundaries, self.wall_trigger, self.rocks
        ]
        
        for i in self.track:
            i.disable()

        self.played = False
        self.unlocked = False

        self.disable()

    def update(self):
        if self.car.simple_intersects(self.finish_line):
            if self.car.anti_cheat == 1:
                self.car.timer_running = True
                self.car.last_count = self.car.count
                self.car.anti_cheat = 0
                invoke(self.car.reset_timer, delay = 3)

                self.car.check_highscore()

        if self.car.simple_intersects(self.wall_trigger):
            self.car.anti_cheat = 1