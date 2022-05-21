from ursina import *
from ursina import curve
from server import Server
import os

Text.default_resolution = 1080 * Text.size

class MainMenu(Entity):
    def __init__(self, car, sand_track, grass_track, snow_track, plains_track):
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
        self.video_menu = Entity(parent = self, enabled = False)
        self.gameplay_menu = Entity(parent = self, enabled = False)
        self.controls_menu = Entity(parent = self, enabled = False)
        self.garage_menu = Entity(parent = self, enabled = False)
        self.pause_menu = Entity(parent = self, enabled = False)
        
        self.car = car
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.plains_track = plains_track

        for menu in (self.start_menu, self.main_menu, self.maps_menu, self.settings_menu, self.video_menu, self.gameplay_menu, self.controls_menu, self.pause_menu):
            def animate_in_menu(menu = menu):
                for i, e in enumerate(menu.children):
                    e.original_scale = e.scale
                    e.scale -= 0.01
                    e.animate_scale(e.original_scale, delay = i * 0.05, duration = 0.1, curve = curve.out_quad)

                    e.alpha = 0
                    e.animate("alpha", 0.7, delay = i * 0.05, duration = 0.1, curve = curve.out_quad)

                    if hasattr(e, "text_entity"):
                        e.text_entity.alpha = 0
                        e.text_entity.animate("alpha", 1, delay = i * 0.05, duration = 0.1)

            menu.on_enable = animate_in_menu

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
        quit_button_start = Button(text = "X", color = color.hex("FF1414"), highlight_color = color.hex("FF4747"), scale_y = 0.058, scale_x = 0.06, y = 0.43, x = 0.85, parent = self.start_menu)

        if window.exit_button.enabled:
            quit_button_start.disable()

        singleplayer_button = Button(text = "S i n g l e p l a y e r", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = 0.05, parent = self.start_menu)
        multiplayer_button = Button(text = "M u l t i p l a y e r", color = color.gray, highlight_color = color.light_gray, scale_y = 0.1, scale_x = 0.3, y = -0.08, parent = self.start_menu)
        
        singleplayer_button.on_click = Func(singleplayer)
        multiplayer_button.on_click = Func(multiplayer)
        quit_button_start.on_click = Func(application.quit)

        # Host Server Menu

        def create_server():
            if str(self.car.host_ip.text) != "IP" and str(self.car.host_port) != "PORT":
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
        
        self.car.host_ip = InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = self.host_menu)
        self.car.host_port = InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = self.host_menu)

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
            if str(self.car.ip.text) != "IP" and str(self.car.port.text) != "PORT":
                car.multiplayer = True
                self.server_menu.disable()
                self.main_menu.enable()
                grass_track.enable()
                sand_track.disable()
                self.car.position = (0, 0, 4)
                camera.rotation = (35, -20, 0)
                self.car.camera_follow.offset = (20, 40, -50)
                self.car.disable()
                self.car.connected = False

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

            plains_track.disable()
            plains_track.finish_line.disable()
            plains_track.boundaries.disable()
            plains_track.wall1.disable()
            plains_track.wall2.disable()
            plains_track.wall3.disable()
            plains_track.wall4.disable()
            plains_track.wall5.disable()
            plains_track.wall6.disable()
            plains_track.wall7.disable()
            plains_track.wall8.disable()
            plains_track.wall_trigger.disable()

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

            plains_track.disable()
            plains_track.finish_line.disable()
            plains_track.boundaries.disable()
            plains_track.wall1.disable()
            plains_track.wall2.disable()
            plains_track.wall3.disable()
            plains_track.wall4.disable()
            plains_track.wall5.disable()
            plains_track.wall6.disable()
            plains_track.wall7.disable()
            plains_track.wall8.disable()
            plains_track.wall_trigger.disable()

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

            plains_track.disable()
            plains_track.finish_line.disable()
            plains_track.boundaries.disable()
            plains_track.wall1.disable()
            plains_track.wall2.disable()
            plains_track.wall3.disable()
            plains_track.wall4.disable()
            plains_track.wall5.disable()
            plains_track.wall6.disable()
            plains_track.wall7.disable()
            plains_track.wall8.disable()
            plains_track.wall_trigger.disable()

            with open(self.car.highscore_path_snow, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        def plains_track_func():
            self.car.enable()
            mouse.locked = True
            self.maps_menu.disable()
            self.car.position = (12, -35, 73)
            self.car.rotation = (0, 90, 0)
            self.car.reset_count_timer.enable()
            grass_track.disable()
            sand_track.disable()
            snow_track.disable
            plains_track.enable()
            
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

            plains_track.enable()
            plains_track.finish_line.enable()
            plains_track.boundaries.enable()
            plains_track.wall1.enable()
            plains_track.wall2.enable()
            plains_track.wall3.enable()
            plains_track.wall4.enable()
            plains_track.wall5.enable()
            plains_track.wall6.enable()
            plains_track.wall7.enable()
            plains_track.wall8.enable()
            plains_track.wall_trigger.enable()

            with open(self.car.highscore_path_plains, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        start_button = Button(text = "S t a r t - G a m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        sand_track_button = Button(text = "S a n d - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = -0.5, parent = self.maps_menu)
        grass_track_button = Button(text = "G r a s s - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0, parent = self.maps_menu)
        snow_track_button = Button(text = "S n o w - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.3, x = 0.5, parent = self.maps_menu)
        plains_track_button = Button(text = "P l a i n s - T r a c k", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.1, x = -0.5, parent = self.maps_menu)
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
        plains_track_button.on_click = Func(plains_track_func)
        back_button.on_click = Func(back)

        # Settings

        def settings():
            self.main_menu.disable()
            self.settings_menu.enable()

        def video():
            self.settings_menu.disable()
            self.video_menu.enable()

        def gameplay():
            self.settings_menu.disable()
            self.gameplay_menu.enable()

        def controls():
            self.settings_menu.disable()
            self.controls_menu.enable()

        def back_settings():
            self.settings_menu.disable()
            self.main_menu.enable()

        settings_button = Button(text = "S e t t i n g s", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        
        video_button = Button(text = "Video", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.18, parent = self.settings_menu)
        gameplay_button = Button(text = "Gameplay", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.06, parent = self.settings_menu)
        controls_button = Button(text = "Controls", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.06, parent = self.settings_menu)

        back_button_settings = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.18, parent = self.settings_menu)

        settings_button.on_click = Func(settings) 
        video_button.on_click = Func(video)
        gameplay_button.on_click = Func(gameplay)
        controls_button.on_click = Func(controls)
        back_button_settings.on_click = Func(back_settings)

        # Gameplay Menu

        def camera_shake():
            self.car.camera_shake_option = not self.car.camera_shake_option
            if self.car.camera_shake_option:
                camera_shake_button.text = "Camera Shake: On"
            elif self.car.camera_shake_option == False:
                camera_shake_button.text = "Camera Shake: Off"

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

            with open(self.car.highscore_path_plains, "w") as hs:
                hs.write(str(0.0))

            with open(self.car.highscore_path_plains, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        def back_gameplay():
            self.gameplay_menu.disable()
            self.settings_menu.enable()

        camera_shake_button = Button("Camera Shake: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.gameplay_menu)
        reset_highsore_button = Button(text = "Reset Highscore", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.gameplay_menu)
        back_button_gameplay = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.gameplay_menu)

        camera_shake_button.on_click = Func(camera_shake)
        reset_highsore_button.on_click = Func(reset_highscore)
        back_button_gameplay.on_click = Func(back_gameplay)

        # Video Menu

        def fullscreen():
            window.fullscreen = not window.fullscreen
            if window.fullscreen:
                fullscreen_button.text = "Fullscreen: On"
            elif window.fullscreen == False:
                fullscreen_button.text = "Fullscreen: Off"

        def borderless():
            window.borderless = not window.borderless
            if window.borderless:
                borderless_button.text = "Borderless: On"
            elif window.borderless == False:
                borderless_button.text = "Borderless: Off"
            window.exit_button.enable()

        def fps():
            window.fps_counter.enabled = not window.fps_counter.enabled
            if window.fps_counter.enabled:
                fps_button.text = "Fps: On"
            elif window.fps_counter.enabled == False:
                fps_button.text = "Fps: Off"

        def exit_button_func():
            window.exit_button.enabled = not window.exit_button.enabled
            if window.exit_button.enabled:
                exit_button.text = "Exit Button: On"
            elif window.exit_button.enabled == False:
                exit_button.text = "Exit Button: Off"

        def back_video():
            self.video_menu.disable()
            self.settings_menu.enable()

        fullscreen_button = Button("Fullscreen: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.24, parent = self.video_menu)
        borderless_button = Button("Borderless: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.12, parent = self.video_menu)
        fps_button = Button("FPS: Off", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0, parent = self.video_menu)
        exit_button = Button("Exit Button: On", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.12, parent = self.video_menu)
        back_button_video = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.24, parent = self.video_menu)

        fullscreen_button.on_click = Func(fullscreen)
        borderless_button.on_click = Func(borderless)
        fps_button.on_click = Func(fps)
        exit_button.on_click = Func(exit_button_func)
        back_button_video.on_click = Func(back_video)

        # Controls

        def back_controls():
            self.controls_menu.disable()
            self.settings_menu.enable()

        def controls_settings():
            if self.car.controls == "wasd":
                self.car.controls = "zqsd"
                controls_settings_button.text = "Controls: ZQSD"
            elif self.car.controls == "zqsd":
                self.car.controls = "wasd"
                controls_settings_button.text = "Controls: WASD"

        controls_settings_button = Button("Controls: WASD", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.06, parent = self.controls_menu)
        back_button_controls = Button(text = "Back", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.06, parent = self.controls_menu)

        back_button_controls.on_click = Func(back_controls)
        controls_settings_button.on_click = Func(controls_settings)

        # Pause Menu

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

        def respawn():
            if grass_track.enabled == True:
                self.car.position = (-80, -30, 15)
                self.car.rotation = (0, 90, 0)
            elif sand_track.enabled == True:
                self.car.position = (0, -40, 4)
                self.car.rotation = (0, 65, 0)
            elif snow_track.enabled == True:
                self.car.position = (-5, -35, 90)
                self.car.rotation = (0, 90, 0)
            elif plains_track.enabled == True:
                self.car.position = (12, -35, 73)
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
            plains_track.disable()
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

        # Error Log

        self.connected = Text(text = "Connected to server!", scale = 1.5, color = color.hex("4dff4d"), line_height = 2, x = -0.55, origin = 0, y = 0.45, parent = camera.ui)
        self.not_connected = Text(text = "Not connected to server...", scale = 1.5, color = color.hex("FF2E2E"), line_height = 2, x = -0.55, origin = 0, y = 0.45, parent = camera.ui)
        self.connected.disable()
        self.not_connected.disable()

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
                    if self.sand_track.enabled or self.grass_track.enabled or self.snow_track.enabled or self.plains_track.enabled:
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