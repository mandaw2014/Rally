from ursina import *

class LakeTrack(Entity):
    def __init__(self, car):
        super().__init__(
            model = "lake_track.obj", 
            texture = "lake_track.png", 
            position = (0, -50, 0), 
            rotation = (0, 90, 0), 
            scale = (14, 14, 14), 
            collider = "mesh"
        )

        self.car = car

        self.finish_line = Entity(model = "cube", position = (-96, -50, 157), scale = (3, 8, 30), visible = False)
        self.boundaries = Entity(model = "lake_track_bounds.obj", collider = "mesh", y = -50, rotation_y = 90, scale = 14, visible = False)
        self.lake_bounds = Entity(model = "cube", y = -59, scale = (1000, 10, 1000), visible = False)
        self.wall_trigger = Entity(model = "cube", position = (143, -30, -145), scale = (3, 10, 30), visible = False)

        self.trees = Entity(model = "trees-lake.obj", texture = "tree-lake.png", y = -50, rotation_y = 90, scale = 14)
        self.thin_trees = Entity(model = "thintrees-lake.obj", texture = "thintree-lake.png", y = -50, rotation_y = 90, scale = 14)
        self.rocks = Entity(model = "rocks-lake.obj", texture = "rock-lake.png", y = -50, rotation_y = 90, scale = 14)
        self.bigrocks = Entity(model = "bigrocks-lake.obj", texture = "rock-lake.png", y = -50, rotation_y = 90, scale = 14)
        self.grass = Entity(model = "grass-lake.obj", texture = "grass-lake.png", y = -50, rotation_y = 90, scale = 14)

        self.track = [
            self.finish_line, self.boundaries, self.lake_bounds, self.wall_trigger
        ]

        self.details = [
            self.trees, self.rocks, self.grass, self.thin_trees, self.bigrocks
        ]
        
        for i in self.track:
            i.disable()
        for i in self.details:
            i.disable()

        self.disable()

        self.played = False
        self.unlocked = False

    def update(self):
        if self.car.simple_intersects(self.lake_bounds):
            self.car.reset_car()

        if self.car.simple_intersects(self.finish_line):
            if self.car.anti_cheat == 1:
                self.car.timer_running = True
                self.car.anti_cheat = 0
                if self.car.gamemode != "drift":
                    invoke(self.car.reset_timer, delay = 3)

                self.car.check_highscore()

        if self.car.simple_intersects(self.wall_trigger):
            self.car.anti_cheat = 1