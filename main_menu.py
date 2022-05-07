from ursina import *
from ursina import curve
from server import Server
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, car, sand_track, grass_track, snow_track):
        super().__init__(
            parent = camera.ui
        )

        self.start_menu = Entity(parent = self, enabled = True)
        self.host_menu = Entity(parent = self, enabled = False)
        self.created_server_menu = Entity(parent = self, enabled = False)
        self.server_menu = Entity(parent = self, enabled = False)
        self.main_menu = Entity(parent = self, enabled = False)
        self.maps_menu = Entity(parent = self, enabled = False)
        self.settings_menu = Entity(parent = self, enabled = False)
        self.controls_menu = Entity(parent = self, enabled = False)
        self.garage_menu = Entity(parent = self, enabled = False)
        self.pause_menu = Entity(parent = self, enabled = False)
        
        self.car = car
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track

        # Start Menu

        self.car.position = (-80, -42, 18.8)
        self.car.rotation = (0, 90, 0)
        self.car.enable()
        self.grass_track.enable()

        def singleplayer():
            car.multiplayer = False
            self.start_menu.disable()
            self.main_menu.enable()
            grass_track.enable()
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = (20, 40, -50)
            self.car.disable()

        def multiplayer():
            self.start_menu.disable()
            self.host_menu.enable()
            self.car.enable()
            self.car.position = (-3, -44.5, 92)
            grass_track.disable()
            snow_track.enable()

        start_title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.start_menu, y = 0.3)

        singleplayer_button = Button(text = "S i n g l e p l a y e r", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = 0.05, parent = self.start_menu)
        multiplayer_button = Button(text = "M u l t i p l a y e r", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = -0.08, parent = self.start_menu)
        
        singleplayer_button.on_click = Func(singleplayer)
        multiplayer_button.on_click = Func(multiplayer)

        # Host Server Menu

        def create_server():
            self.car.server = Server(car.host_ip, car.host_port)
            self.car.server_running = True
            self.car.server.start_server = True
            self.host_menu.disable()
            self.created_server_menu.enable()
            self.car.enable()
            self.car.position = (-32, -48.4, -45)
            snow_track.disable()
            sand_track.enable()
            back_button_server.disable()

        def join_server_func():
            self.host_menu.disable()
            self.server_menu.enable()
            self.car.enable()
            self.car.position = (-32, -48.4, -45)
            snow_track.disable()
            sand_track.enable()

        def back_host():
            self.host_menu.disable()
            self.start_menu.enable()
            self.car.position = (-80, -42, 18.8)
            self.car.rotation = (0, 90, 0)
            self.car.enable()
            self.grass_track.enable()
            self.snow_track.disable()
        
        self.car.host_ip = InputField(default_value = "localhost", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.host_menu)
        self.car.host_port = InputField(default_value = "25565", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.host_menu)

        create_server_button = Button(text = "C r e a t e", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.host_menu)
        join_server_button = Button(text = "J o i n - S e r v e r", color = color.hex("0097F5"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.host_menu)
        back_button_host = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.host_menu)

        create_server_button.on_click = Func(create_server)
        join_server_button.on_click = Func(join_server_func)
        back_button_host.on_click = Func(back_host)

        # Created Server

        def join_hosted_server_func():
            car.ip.text = car.host_ip.text
            car.port.text = car.host_port.text
            car.multiplayer = True
            self.created_server_menu.disable()
            self.main_menu.enable()
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = (20, 40, -50)
            self.car.disable()
            self.sand_track.disable()
            self.grass_track.enable()

        def stop_server():
            application.quit()
            os._exit(0)

        self.username_created_server = InputField(default_value = car.username_text, color = color.black, alpha = 100, y = 0.05, parent = self.created_server_menu)
        join_hosted_server = Button(text = "J o i n - S e r v e r", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.created_server_menu)
        running = Text(text = "Running server...", scale = 1.5, line_height = 2, x = 0, origin = 0, y = 0.2, parent = self.created_server_menu)
        stop_button = Button(text = "S t o p", color = color.hex("D22828"), scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.created_server_menu)

        join_hosted_server.on_click = Func(join_hosted_server_func)
        stop_button.on_click = Func(stop_server)

        # Server Menu

        def join_server():
            car.multiplayer = True
            self.server_menu.disable()
            self.main_menu.enable()
            grass_track.enable()
            sand_track.disable()
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = (20, 40, -50)
            self.car.disable()

        def back_server():
            self.host_menu.enable()
            self.server_menu.disable()
            self.car.enable()
            self.car.position = (-3, -44.5, 92)
            sand_track.disable()
            snow_track.enable()

        car.username = InputField(default_value = car.username_text, color = color.black, alpha = 100, y = 0.18, parent = self.server_menu)
        car.ip = InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.server_menu)
        car.port = InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.server_menu)
        join_button = Button(text = "J o i n", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.server_menu)
        back_button_server = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.server_menu)

        join_button.on_click = Func(join_server)
        back_button_server.on_click = Func(back_server)

        # Main Menu

        def quit_app():
            application.quit()
            if self.car.multiplayer_update:
                os._exit(0)

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.34, parent = self.main_menu)
        quit_button.on_click = Func(quit_app)

        # Maps Menu

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
            self.car.position = (0, -20, 4)
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

            snow_track.finish_line.disable()
            snow_track.boundaries.disable()
            snow_track.wall1.disable()
            snow_track.wall2.disable()
            snow_track.wall3.disable()
            snow_track.wall4.disable()
            snow_track.wall5.disable()
            snow_track.wall6.disable()
            snow_track.wall7.disable()
            snow_track.wall8.disable()
            snow_track.wall9.disable()
            snow_track.wall10.disable()
            snow_track.wall11.disable()
            snow_track.wall12.disable()
            snow_track.wall_trigger.disable()
            snow_track.wall_trigger_end.disable()

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

            snow_track.finish_line.disable()
            snow_track.boundaries.disable()
            snow_track.finish_line.disable()
            snow_track.boundaries.disable()
            snow_track.wall1.disable()
            snow_track.wall2.disable()
            snow_track.wall3.disable()
            snow_track.wall4.disable()
            snow_track.wall5.disable()
            snow_track.wall6.disable()
            snow_track.wall7.disable()
            snow_track.wall8.disable()
            snow_track.wall9.disable()
            snow_track.wall10.disable()
            snow_track.wall11.disable()
            snow_track.wall12.disable()
            snow_track.wall_trigger.disable()
            snow_track.wall_trigger_end.disable()

            with open(self.car.highscore_path_grass, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        def snow_track_func():
            self.car.enable()
            mouse.locked = True
            self.maps_menu.disable()
            self.car.position = (-5, -35, 90)
            self.car.rotation = (0, 90, 0)
            self.car.reset_count_timer.enable()
            grass_track.disable()
            sand_track.disable()
            snow_track.enable()
            
            sand_track.finish_line.disable()
            sand_track.boundaries.disable()
            sand_track.wall1.disable()
            sand_track.wall2.disable()
            sand_track.wall3.disable()
            sand_track.wall4.disable()
            sand_track.wall_trigger.disable()

            grass_track.finish_line.disable()
            grass_track.boundaries.disable()
            grass_track.wall1.disable()
            grass_track.wall2.disable()
            grass_track.wall3.disable()
            grass_track.wall4.disable()
            grass_track.wall_trigger.disable()
            grass_track.wall_trigger_ramp.disable()

            snow_track.finish_line.enable()
            snow_track.boundaries.enable()
            snow_track.wall1.enable()
            snow_track.wall2.enable()
            snow_track.wall3.enable()
            snow_track.wall4.enable()
            snow_track.wall5.enable()
            snow_track.wall6.enable()
            snow_track.wall7.enable()
            snow_track.wall8.enable()
            snow_track.wall9.enable()
            snow_track.wall10.enable()
            snow_track.wall11.enable()
            snow_track.wall12.enable()
            snow_track.wall_trigger.enable()
            snow_track.wall_trigger_end.enable()

            with open(self.car.highscore_path_snow, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        start_button = Button(text = "S t a r t - G a m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        sand_track_button = Button(text = "S a n d - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "G r a s s - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        snow_track_button = Button(text = "S n o w - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0.5, parent = self.maps_menu)
        back_button = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.maps_menu)
        
        self.leaderboard_background = Entity(model = "quad", color = color.hex("0099ff"), alpha = 100, scale = (0.4, 0.42), position = Vec2(0.6, 0.25), parent = camera.ui)
        self.leaderboard_title = Text("Leaderboard", color = color.gold, scale = 5, line_height = 2, origin = 0, y = 0.4, parent = self.leaderboard_background)
        
        self.leaderboard_01 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0.2, parent = self.leaderboard_background)
        self.leaderboard_02 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0.1, parent = self.leaderboard_background)
        self.leaderboard_03 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = 0, parent = self.leaderboard_background)
        self.leaderboard_04 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = -0.1, parent = self.leaderboard_background)
        self.leaderboard_05 = Text(text = "", color = color.hex("#CCCCCC"), scale = 3, line_height = 2, x = 0, origin = 0, y = -0.2, parent = self.leaderboard_background)
        
        self.leaderboard_background.disable()
        self.leaderboard_title.disable()

        start_button.on_click = Func(start)
        sand_track_button.on_click = Func(sand_track_func)
        grass_track_button.on_click = Func(grass_track_func)
        snow_track_button.on_click = Func(snow_track_func)
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

        def fps_on():
            window.fps_counter.enable()

        def fps_off():
            window.fps_counter.disable()

        def exit_button_on():
            window.exit_button.enable()

        def exit_button_off():
            window.exit_button.disable()

        def reset_highscore():
            with open(self.car.highscore_path_sand, "w") as hs:
                hs.write(str(0.0))

            with open(self.car.highscore_path_sand, "r") as hs:
                self.car.highscore_count = hs.read()

            with open(self.car.highscore_path_grass, "w") as hs:
                hs.write(str(0.0))

            with open(self.car.highscore_path_grass, "r") as hs:
                self.car.highscore_count = hs.read()

            with open(self.car.highscore_path_snow, "w") as hs:
                hs.write(str(0.0))

            with open(self.car.highscore_path_snow, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        settings_button = Button(text = "S e t t i n g s", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)

        back_button_settings = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.settings_menu)
        
        camera_shake = Text(text = "Camera Shake", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.3, x = -0.8, parent = self.settings_menu)
        camera_shake_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = -0.3, parent = self.settings_menu)
        camera_shake_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = -0.1, parent = self.settings_menu)
        
        fullscreen = Text(text = "Fullscreen", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.1, x = -0.7, parent = self.settings_menu)
        fullscreen_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.085, x = -0.3, parent = self.settings_menu)
        fullscreen_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.085, x = -0.1, parent = self.settings_menu)
        
        borderless = Text(text = "Borderless", size = 10, resolution = 4096, scale = (1.5, 1.5), y = -0.1, x = -0.7, parent = self.settings_menu)
        borderless_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = -0.125, x = -0.3, parent = self.settings_menu)
        borderless_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = -0.125, x = -0.1, parent = self.settings_menu)
        
        fps = Text(text = "FPS", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.3, x = 0.2, parent = self.settings_menu)
        fps_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = 0.5, parent = self.settings_menu)
        fps_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.285, x = 0.7, parent = self.settings_menu)

        exit_button = Text(text = "Exit Button", size = 10, resolution = 4096, scale = (1.5, 1.5), y = 0.1, x = 0.2, parent = self.settings_menu)
        exit_button_on_ = Button("On", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.085, x = 0.5, parent = self.settings_menu)
        exit_button_off_ = Button("Off", color = color.light_gray, scale_y = 0.1, scale_x = 0.1, y = 0.085, x = 0.7, parent = self.settings_menu)

        reset_highsore_button = Button(text = "R e s e t - H i g h s c o r e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.27, parent = self.settings_menu)

        settings_button.on_click = Func(settings)
        camera_shake_on_.on_click = Func(camera_shake_on)
        camera_shake_off_.on_click = Func(camera_shake_off)
        fullscreen_on_.on_click = Func(fullscreen_on)
        fullscreen_off_.on_click = Func(fullscreen_off)
        borderless_on_.on_click = Func(borderless_on)
        borderless_off_.on_click = Func(borderless_off)
        fps_on_.on_click = Func(fps_on)
        fps_off_.on_click = Func(fps_off)
        exit_button_on_.on_click = Func(exit_button_on)
        exit_button_off_.on_click = Func(exit_button_off)
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
            if snow_track.enabled == True:
                self.car.position = (-5, -35, 90)
                self.car.rotation = (0, 90, 0)
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
            snow_track.disable()
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
            self.car.position = (0, 0, 4)
            camera.rotation = (35, -20, 0)
            self.car.camera_follow.offset = (20, 40, -50)
            self.car.disable()
            grass_track.enable()
            sand_track.disable()

            with open(self.car.highscore_path_grass, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        def garage_button_func():
            self.garage_menu.enable()
            self.main_menu.disable()
            self.car.enable()
            self.car.position = (-32, -48.4, -45)
            grass_track.disable()
            sand_track.enable()

        def change_color(color):
            """
            Changes the car color to the selected color after a small animation.
            """
            if self.start_spin == True:
                car.animate_rotation_y(car.rotation_y + 360, duration = 0.4, curve = curve.in_out_quad)
            car.texture = f"car-{color}.png"

        self.start_spin = True

        garage_button = Button(text = "G a r a g e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)

        back_button_garage = Button(text = "< - B a c k", color = color.gray, scale_y = 0.05, scale_x = 0.2, y = 0.45, x = -0.65, parent = self.garage_menu)
        red_button = Button(color = color.red, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.7, parent = self.garage_menu)
        blue_button = Button(color = color.cyan, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.5, parent = self.garage_menu)
        green_button = Button(color = color.lime, scale_y = 0.1, scale_x = 0.15, y = 0.1, x = -0.3, parent = self.garage_menu)
        orange_button = Button(color = color.orange, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.7, parent = self.garage_menu)
        black_button = Button(color = color.black, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.5, parent = self.garage_menu)
        white_button = Button(color = color.white, scale_y = 0.1, scale_x = 0.15, y = -0.1, x = -0.3, parent = self.garage_menu)

        garage_button.on_click = Func(garage_button_func)
        back_button_garage.on_click = Func(back_garage)
        red_button.on_click = Func(change_color, "red")
        blue_button.on_click = Func(change_color, "blue")
        green_button.on_click = Func(change_color, "green")
        orange_button.on_click = Func(change_color, "orange")
        black_button.on_click = Func(change_color, "black")
        white_button.on_click = Func(change_color, "white")

    def update(self):
        if self.start_menu.enabled:
            if not held_keys["right mouse"]:
                self.car.rotation_y += 15 * time.dt
            else:
                self.car.rotation_y = mouse.x * 500
            self.car.camera_follow.offset = (-25, 4, 0)
            camera.rotation = (5, 90, 0)

        if self.host_menu.enabled:
            if not held_keys["right mouse"]:
                self.car.rotation_y += 15 * time.dt
            else:
                self.car.rotation_y = mouse.x * 500
            self.car.camera_follow.offset = (-25, 8, 0)
            camera.rotation = (14, 90, 0)

        if self.garage_menu.enabled:
            if not held_keys["right mouse"]:
                self.car.rotation_y += 15 * time.dt
            else:
                self.car.rotation_y = mouse.x * 500
            self.car.camera_follow.offset = (-25, 5, 3)
            camera.rotation = (10, 90, 0)

        if self.server_menu.enabled:
            if not held_keys["right mouse"]:
                self.car.rotation_y += 15 * time.dt
            else:
                self.car.rotation_y = mouse.x * 500
            self.car.camera_follow.offset = (-25, 6, 5)
            camera.rotation = (10, 90, 0)

        if self.host_menu.enabled or self.server_menu.enabled:
            with open(self.car.username_path, "w") as user:
                user.write(self.car.username.text)
            
        if self.created_server_menu.enabled:
            with open(self.car.username_path, "w") as user:
                user.write(self.username_created_server.text)

        if self.car.multiplayer_update:
            if self.main_menu.enabled == False and self.server_menu.enabled == False and self.maps_menu.enabled == False:
                if self.garage_menu.enabled == False and self.settings_menu.enabled == False and self.controls_menu.enabled == False:
                    if self.sand_track.enabled or self.grass_track.enabled or self.snow_track.enabled:
                        invoke(self.start_leaderboard, delay = 0.1)
            else:
                self.leaderboard_background.disable()
                self.leaderboard_title.disable()
                self.leaderboard_01.disable()
                self.leaderboard_02.disable()
                self.leaderboard_03.disable()
                self.leaderboard_04.disable()
                self.leaderboard_05.disable()
        else:
            self.leaderboard_background.disable()
            self.leaderboard_title.disable()
            self.leaderboard_01.disable()
            self.leaderboard_02.disable()
            self.leaderboard_03.disable()
            self.leaderboard_04.disable()
            self.leaderboard_05.disable()

        if held_keys["w"] or held_keys["up arrow"]:
            self.start_spin = False
        else:
            self.start_spin = True
            
    def start_leaderboard(self):
        self.leaderboard_background.enable()
        self.leaderboard_title.enable()
        self.leaderboard_01.enable()
        self.leaderboard_02.enable()
        self.leaderboard_03.enable()
        self.leaderboard_04.enable()
        self.leaderboard_05.enable()

        self.leaderboard_01.text = str(self.car.leaderboard_01)
        self.leaderboard_02.text = str(self.car.leaderboard_02)
        self.leaderboard_03.text = str(self.car.leaderboard_03)
        self.leaderboard_04.text = str(self.car.leaderboard_04)
        self.leaderboard_05.text = str(self.car.leaderboard_05)