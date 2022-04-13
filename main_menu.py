from ursina import *
from ursina import curve
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import os

class MainMenu(Entity):
    def __init__(self, car, sand_track, grass_track, garage):
        super().__init__(
            parent = camera.ui
        )

        self.main_menu = Entity(parent = self, enabled = True)
        self.maps_menu = Entity(parent = self, enabled = False)
        self.settings_menu = Entity(parent = self, enabled = False)
        self.controls_menu = Entity(parent = self, enabled = False)
        self.garage_menu = Entity(parent = self, enabled = False)
        self.pause_menu = Entity(parent = self, enabled = False)
        self.car = car

        # Main Menu

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.34, parent = self.main_menu)
        quit_button.on_click = application.quit

        # Start Menu

        def start():
            self.maps_menu.enable()
            self.main_menu.disable()

        def back():
            self.maps_menu.disable()
            self.main_menu.enable()

        def sand_track_func():
            self.car.enable()
            mouse.locked = True
            self.maps_menu.disable()
            self.car.position = (0, 0, 4)
            self.car.rotation = (0, 65, 0)
            self.car.reset_count_timer.enable()
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

            with open(self.car.highscore_path_sand, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        def grass_track_func():
            self.car.enable()
            mouse.locked = True
            self.maps_menu.disable()
            self.car.position = (-80, -30, 15)
            self.car.rotation = (0, 90, 0)
            self.car.reset_count_timer.enable()
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

            with open(self.car.highscore_path_grass, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        start_button = Button(text = "S t a r t - G a m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        sand_track_button = Button(text = "S a n d - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "G r a s s - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        back_button = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.maps_menu)
        
        start_button.on_click = Func(start)
        sand_track_button.on_click = Func(sand_track_func)
        grass_track_button.on_click = Func(grass_track_func)
        back_button.on_click = Func(back)

        # Settings

        def settings():
            self.main_menu.disable()
            self.settings_menu.enable()

        def back_settings():
            self.settings_menu.disable()
            self.main_menu.enable()

        def camera_shake_on():
            self.car.camera_shake_option = True

        def camera_shake_off():
            self.car.camera_shake_option = False

        def fullscreen_on():
            window.fullscreen = True

        def fullscreen_off():
            window.fullscreen = False

        def borderless_on():
            window.borderless = True
            window.exit_button.enable()

        def borderless_off():
            window.borderless = False
            window.exit_button.enable()

        def reset_highscore():
            with open(self.car.highscore_path_sand, "w") as hs:
                hs.write(str(0.0))

            with open(self.car.highscore_path_sand, "r") as hs:
                self.car.highscore_count = hs.read()

            with open(self.car.highscore_path_grass, "w") as hs:
                hs.write(str(0.0))

            with open(self.car.highscore_path_grass, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        settings_button = Button(text = "S e t t i n g s", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)

        back_button_settings = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.settings_menu)
        
        camera_shake = Text(text = "C a m e r a - S h a k e", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.3, x = -0.5, parent = self.settings_menu)
        camera_shake_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = 0, parent = self.settings_menu)
        camera_shake_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = 0.2, parent = self.settings_menu)
        
        fullscreen = Text(text = "Fullscreen", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.1, x = -0.4, parent = self.settings_menu)
        fullscreen_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.085, x = 0, parent = self.settings_menu)
        fullscreen_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.085, x = 0.2, parent = self.settings_menu)
        
        borderless = Text(text = "Borderless", size = 10, resolution = 4096, scale = (1.5, 1.5), y = -0.1, x = -0.4, parent = self.settings_menu)
        borderless_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = -0.125, x = 0, parent = self.settings_menu)
        borderless_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = -0.125, x = 0.2, parent = self.settings_menu)
        
        reset_highsore_button = Button(text = "R e s e t - H i g h s c o r e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.27, parent = self.settings_menu)

        settings_button.on_click = Func(settings)
        camera_shake_on_.on_click = Func(camera_shake_on)
        camera_shake_off_.on_click = Func(camera_shake_off)
        fullscreen_on_.on_click = Func(fullscreen_on)
        fullscreen_off_.on_click = Func(fullscreen_off)
        borderless_on_.on_click = Func(borderless_on)
        borderless_off_.on_click = Func(borderless_off)
        reset_highsore_button.on_click = Func(reset_highscore)
        
        back_button_settings.on_click = Func(back_settings)

        # Controls

        def controls():
            self.settings_menu.disable()
            self.controls_menu.enable()

        def back_controls():
            self.controls_menu.disable()
            self.settings_menu.enable()

        def controls_wasd():
            self.car.controls = "wasd"

        def controls_zqsd():
            self.car.controls = "zqsd"

        controls_button = Button(text = "C o n t r o l s", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.4, parent = self.settings_menu)
        back_button_controls = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.controls_menu)

        controls_ = Text(text = "C o n t r o l s", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.3, x = -0.5, parent = self.controls_menu)
        controls_wasd_ = Button("WASD", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = 0, parent = self.controls_menu)
        controls_zqsd_ = Button("ZQSD", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = 0.2, parent = self.controls_menu)

        controls_button.on_click = Func(controls)
        back_button_controls.on_click = Func(back_controls)
        controls_wasd_.on_click = Func(controls_wasd)
        controls_zqsd_.on_click = Func(controls_zqsd)

        # Pause Menu

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

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
            self.car.reset_count_timer.disable()
            self.car.timer_running = False
            self.car.anti_cheat = 1
            self.main_menu.enable()
            self.pause_menu.disable()
            sand_track.disable()
            grass_track.enable()

        p_resume_button = Button(text = "R e s u m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.11, parent = self.pause_menu)
        p_respawn_button = Button(text = "R e s p a w n", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.01, parent = self.pause_menu)
        p_mainmenu_button = Button(text = "M a i n - M e n u", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.13, parent = self.pause_menu)
        p_mainmenu_button.on_click = Func(main_menu)
        p_respawn_button.on_click = Func(respawn)
        p_resume_button.on_click = Func(resume)

        # Garage

        def back_garage():
            self.garage_menu.disable()
            self.main_menu.enable()
            camera.rotation = (35, -20, 0)
            self.car.garage_mode = False
            self.car.disable()
            garage.disable()
            grass_track.enable()

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

        def change_color(color):
            """
            Changes the car color to the selected color after a small animation.
            """
            car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            car.texture = f"car-{color}.png"

        garage_button = Button(text = "G a r a g e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)

        back_button_garage = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.garage_menu)
        red_button = Button(color = color.red, scale_y = 0.1, scale_x = 0.15, y = 0.2, x = -0.3, parent = self.garage_menu)
        blue_button = Button(color = color.cyan, scale_y = 0.1, scale_x = 0.15, y = 0.2, x = 0, parent = self.garage_menu)
        green_button = Button(color = color.lime, scale_y = 0.1, scale_x = 0.15, y = 0.2, x = 0.3, parent = self.garage_menu)
        orange_button = Button(color = color.orange, scale_y = 0.1, scale_x = 0.15, y = -0.2, x = -0.3, parent = self.garage_menu)
        black_button = Button(color = color.black, scale_y = 0.1, scale_x = 0.15, y = -0.2, x = 0, parent = self.garage_menu)
        white_button = Button(color = color.white, scale_y = 0.1, scale_x = 0.15, y = -0.2, x = 0.3, parent = self.garage_menu)

        garage_button.on_click = Func(garage_button_func)
        back_button_garage.on_click = Func(back_garage)
        red_button.on_click = Func(change_color, "red")
        blue_button.on_click = Func(change_color, "blue")
        green_button.on_click = Func(change_color, "green")
        orange_button.on_click = Func(change_color, "orange")
        black_button.on_click = Func(change_color, "black")
        white_button.on_click = Func(change_color, "white")