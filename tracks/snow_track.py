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

        self.finish_line = Entity(model = "cube", position = (11, -42, 90), rotation = (0, 0, 0), scale = (3, 8, 30), visible = False)
        self.boundaries = Entity(model = "snow_track_bounds.obj", collider = "mesh", rotation = (0, 90, 0), position = (0, -50, 0), scale = (8, 8, 8), visible = False)

        self.wall1 = Entity(model = "cube", position = (-10, -42, 38), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall2 = Entity(model = "cube", position = (-36, -42, 38), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall3 = Entity(model = "cube", position = (-21, -42, 54), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall4 = Entity(model = "cube", position = (-21, -42, 28), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall5 = Entity(model = "cube", position = (-10, -42, -10), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall6 = Entity(model = "cube", position = (-36, -42, -10), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall7 = Entity(model = "cube", position = (-21, -42, 8), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 50), visible = False)
        self.wall8 = Entity(model = "cube", position = (-21, -42, -28), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 50), visible = False) 
        self.wall9 = Entity(model = "cube", position = (-36, -42, 84), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 45), visible = False)
        self.wall10 = Entity(model = "cube", position = (-10, -42, 100), rotation = (0, 0, 0), collider = "box", scale = (5, 30, 70), visible = False)
        self.wall11 = Entity(model = "cube", position = (-20, -42, 105), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 30), visible = False)
        self.wall12 = Entity(model = "cube", position = (-20, -42, 76), rotation = (0, 90, 0), collider = "box", scale = (5, 30, 30), visible = False)

        self.wall_trigger = Entity(model = "cube", position = (29, -40.2, -51), rotation = (0, 0, 0), scale = (3, 20, 35), visible = False)
        self.wall_trigger_end = Entity(model = "cube", position = (-70, -40.2, 100), rotation = (0, 0, 0), scale = (35, 20, 3), visible = False)

        self.trees = Entity(model = "trees-snow.obj", texture = "tree-snow.png", y = -50, rotation_y = 90, scale = 8)
        self.thin_trees = Entity(model = "thintrees-snow.obj", texture = "thintree-snow.png", y = -50, rotation_y = 90, scale = 8)
        self.rocks = Entity(model = "rocks-snow.obj", texture = "rock-snow.png", y = -50, rotation_y = 90, scale = 8)

        self.disable()
        
        self.track = [
            self.finish_line, self.boundaries, self.wall1, self.wall2, self.wall3, 
            self.wall4, self.wall5, self.wall6, self.wall7, self.wall8, self.wall9, 
            self.wall10, self.wall11, self.wall12, self.wall_trigger, self.wall_trigger_end,
        ]

        self.details = [
            self.trees, self.thin_trees, self.rocks
        ]

        for i in self.track:
            i.disable()
        for i in self.details:
            i.disable()

        self.played = False

    def update(self):
        if self.car.simple_intersects(self.finish_line):
            if self.car.anti_cheat == 1:
                self.car.timer_running = True
                self.car.anti_cheat = 0
                if self.car.gamemode != "drift":
                    invoke(self.car.reset_timer, delay = 3)

                self.car.check_highscore()

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

        if self.car.simple_intersects(self.wall_trigger):
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
        
        if self.car.simple_intersects(self.wall_trigger_end):
            self.wall9.disable()
            self.wall10.disable()
            self.wall11.enable()
            self.wall12.enable()
            if self.car.anti_cheat == 0.5:
                self.car.anti_cheat = 1