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

        self.finish_line = Entity(model = "cube", position = (-50, -50.2, -7), rotation = (0, 0, 0), scale = (3, 8, 30), visible = False)
        self.boundaries = Entity(model = "sand_track_bounds.obj", collider = "mesh", position = (-80, -50, -75), rotation = (0, 270, 0), scale = (18, 50, 18), visible = False)

        self.wall1 = Entity(model = "cube", position = (-75, -50, -48), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 40), visible = False)
        self.wall2 = Entity(model = "cube", position = (-74, -50, -75), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 40), visible = False)
        self.wall3 = Entity(model = "cube", position = (-61, -50, -60), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 40), visible = False)
        self.wall4 = Entity(model = "cube", position = (-90, -50, -60), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 40), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (-100, -50, -114), rotation = (0, 0, 0), scale = (5, 20, 30), visible = False)

        self.cacti = Entity(model = "cacti-sand.obj", texture = "cactus-sand.png", position = (-80, -50, -75), scale = (18, 18, 18), rotation = (0, 270, 0))
        self.rocks = Entity(model = "rocks-sand.obj", texture = "rock-sand.png", position = (-80, -50, -75), scale = (18, 18, 18), rotation = (0, 270, 0))

        self.track = [
            self.finish_line, self.boundaries, self.wall1, self.wall2, self.wall3, 
            self.wall4, self.wall_trigger
        ]

        self.details = [
            self.cacti, self.rocks
        ]
        
        self.disable()

        for i in self.track:
            i.disable()
        for i in self.details:
            i.disable()

        self.played = False
        self.unlocked = True

    def update(self):
        if self.car.simple_intersects(self.finish_line):
            if self.car.anti_cheat == 1:
                self.car.timer_running = True
                self.car.anti_cheat = 0
                if self.car.gamemode != "drift":
                    invoke(self.car.reset_timer, delay = 3)

                self.car.check_highscore()

                self.wall1.enable()
                self.wall2.enable()
                self.wall3.disable()
                self.wall4.disable()

        if self.car.simple_intersects(self.wall_trigger):
            self.wall1.disable()
            self.wall2.disable()
            self.wall3.enable()
            self.wall4.enable()
            self.car.anti_cheat = 1