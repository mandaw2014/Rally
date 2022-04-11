from ursina import *
import os

class MainMenu(Entity):
    def __init__(self, car, sand_track, grass_track, garage):
        super().__init__(
            parent = camera.ui
        )

        self.main_menu = Entity(parent = self, enabled = True)
        self.maps_menu = Entity(parent = self, enabled = False)
        self.garage_menu = Entity(parent = self, enabled = False)
        self.pause_menu = Entity(parent = self, enabled = False)
        self.car = car

        def start():
            self.maps_menu.enable()
            self.main_menu.disable()

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

        def back():
            self.maps_menu.disable()
            self.main_menu.enable()

        def back_garage():
            self.garage_menu.disable()
            self.main_menu.enable()
            self.car.disable()
            self.car.garage_mode = False
            garage.disable()
            grass_track.enable()

        def respawn():
            if grass_track.enabled == True:
                self.car.position = (-80, -30, 15)
                self.car.rotation = (0, 90, 0)
            if sand_track.enabled == True:
                self.car.position = (0, -40, 4)
                self.car.rotation = (0, 65, 0)
            self.car.speed = 0
            self.car.count = 0.0
            self.car.reset_count = 0.0
            self.car.timer_running = False
            self.car.anti_cheat = 1

        def main_menu():
            self.car.position = (0, 0, 4)
            self.car.disable()
            self.car.rotation = (0, 65, 0)
            self.car.speed = 0
            self.car.count = 0.0
            self.car.reset_count = 0.0
            self.car.timer_running = False
            self.car.anti_cheat = 1
            self.main_menu.enable()
            self.pause_menu.disable()
            sand_track.disable()
            grass_track.enable()

        def sand_track_func():
            self.car.enable()
            mouse.locked = True
            self.maps_menu.disable()
            self.car.position = (0, 0, 4)
            camera.position = (-80, -30, 15)
            sand_track.enable()
            grass_track.disable()
            
            sand_track.finish_line.enable()
            sand_track.boundaries.enable()
            sand_track.wall1.enable()
            sand_track.wall2.enable()
            sand_track.wall3.enable()
            sand_track.wall4.enable()
            sand_track.wall_trigger.enable()

            grass_track.finish_line.disable()
            grass_track.boundaries.disable()
            grass_track.wall1.disable()
            grass_track.wall2.disable()
            grass_track.wall3.disable()
            grass_track.wall4.disable()
            grass_track.wall_trigger.disable()
            grass_track.wall_trigger_ramp.disable()

            path = os.path.dirname(os.path.abspath(__file__))
            highscore = os.path.join(path, "./highscore/highscore-sandtrack.txt")

            with open(highscore, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        def grass_track_func():
            self.car.enable()
            mouse.locked = True
            self.maps_menu.disable()
            self.car.position = (-80, -30, 15)
            self.car.rotation = (0, 90, 0)
            grass_track.enable()
            sand_track.disable()

            sand_track.finish_line.disable()
            sand_track.boundaries.disable()
            sand_track.wall1.disable()
            sand_track.wall2.disable()
            sand_track.wall3.disable()
            sand_track.wall4.disable()
            sand_track.wall_trigger.disable()

            grass_track.finish_line.enable()
            grass_track.boundaries.enable()
            grass_track.wall1.enable()
            grass_track.wall2.enable()
            grass_track.wall3.enable()
            grass_track.wall4.enable()
            grass_track.wall_trigger.enable()
            grass_track.wall_trigger_ramp.enable()

            path = os.path.dirname(os.path.abspath(__file__))
            highscore = os.path.join(path, "./highscore/highscore-grasstrack.txt")

            with open(highscore, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)
        
        def garage_button_func():
            self.garage_menu.enable()
            self.main_menu.disable()
            self.car.enable()
            self.car.garage_mode = True
            garage.enable()
            grass_track.disable()

        def reset_highscore():
            if sand_track.enabled == True:
                path = os.path.dirname(os.path.abspath(__file__))
                highscore = os.path.join(path, "./highscore/highscore-sandtrack.txt")

                with open(highscore, "w") as hs:
                    hs.write(str(0.0))

                with open(highscore, "r") as hs:
                    self.car.highscore_count = hs.read()

                self.car.highscore_count = float(self.car.highscore_count)
            
            if grass_track.enabled == True:
                path = os.path.dirname(os.path.abspath(__file__))
                highscore = os.path.join(path, "./highscore/highscore-grasstrack.txt")

                with open(highscore, "w") as hs:
                    hs.write(str(0.0))

                with open(highscore, "r") as hs:
                    self.car.highscore_count = hs.read()

                self.car.highscore_count = float(self.car.highscore_count)

        def red_car():
            car.texture = "car-red.png"
        
        def blue_car():
            car.texture = "car-blue.png"
        
        def green_car():
            car.texture = "car-green.png"
        
        def orange_car():
            car.texture = "car-orange.png"

        def black_car():
            car.texture = "car-black.png"

        def white_car():
            car.texture = "car-white.png"

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        start_button = Button(text = "S t a r t - G a m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        garage_button = Button(text = "G a r a g e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        quit_button.on_click = application.quit
        start_button.on_click = Func(start)
        garage_button.on_click = Func(garage_button_func)

        sand_track_button = Button(text = "S a n d - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "G r a s s - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        back_button = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.maps_menu)

        sand_track_button.on_click = Func(sand_track_func)
        grass_track_button.on_click = Func(grass_track_func)
        back_button.on_click = Func(back)

        back_button_garage = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.garage_menu)
        red_button = Button(color = color.red, scale_y = 0.1, scale_x = 0.15, y = 0.2, x = -0.3, parent = self.garage_menu)
        blue_button = Button(color = color.cyan, scale_y = 0.1, scale_x = 0.15, y = 0.2, x = 0, parent = self.garage_menu)
        green_button = Button(color = color.lime, scale_y = 0.1, scale_x = 0.15, y = 0.2, x = 0.3, parent = self.garage_menu)
        orange_button = Button(color = color.orange, scale_y = 0.1, scale_x = 0.15, y = -0.2, x = -0.3, parent = self.garage_menu)
        black_button = Button(color = color.black, scale_y = 0.1, scale_x = 0.15, y = -0.2, x = 0, parent = self.garage_menu)
        white_button = Button(color = color.white, scale_y = 0.1, scale_x = 0.15, y = -0.2, x = 0.3, parent = self.garage_menu)

        back_button_garage.on_click = Func(back_garage)
        red_button.on_click = Func(red_car)
        blue_button.on_click = Func(blue_car)
        green_button.on_click = Func(green_car)
        orange_button.on_click = Func(orange_car)
        black_button.on_click = Func(black_car)
        white_button.on_click = Func(white_car)

        p_resume_button = Button(text = "R e s u m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.23, parent = self.pause_menu)
        p_respawn_button = Button(text = "R e s p a w n", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.11, parent = self.pause_menu)
        p_reset_highsore_button = Button(text = "R e s e t - H i g h s c o r e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.01, parent = self.pause_menu)
        p_mainmenu_button = Button(text = "M a i n - M e n u", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.13, parent = self.pause_menu)
        p_mainmenu_button.on_click = Func(main_menu)
        p_reset_highsore_button.on_click = Func(reset_highscore)
        p_respawn_button.on_click = Func(respawn)
        p_resume_button.on_click = Func(resume)