from ursina import *
from ursinanetworking import *
from direct.stdpy import thread

from car import Car
from ai import AICar

from multiplayer import Multiplayer
from main_menu import MainMenu

from sun import SunLight

from achievements import RallyAchievements

from tracks.sand_track import SandTrack
from tracks.grass_track import GrassTrack
from tracks.snow_track import SnowTrack
from tracks.plains_track import PlainsTrack

Text.default_resolution = 1080 * Text.size
Text.default_font = "./assets/Roboto.ttf"

# Window

app = Ursina()
window.title = "Rally"
window.borderless = False
window.show_ursina_splash = True
window.cog_button.disable()
window.fps_counter.disable()
window.exit_button.disable()

if sys.platform != "darwin":
    window.fullscreen = True
else:
    window.size = window.fullscreen_size
    window.position = Vec2(
        int((window.screen_resolution[0] - window.fullscreen_size[0]) / 2),
        int((window.screen_resolution[1] - window.fullscreen_size[1]) / 2)
    )

# Starting new thread for loading textures and models

def load_textures():
    for car_texture in ("black", "blue", "green", "orange", "red", "white"):
        load_texture(f"assets/garage/car-{car_texture}.png")
    for track_texture in ("sand_track/sand_track", "grass_track/grass_track", "snow_track/snow_track", "plains_track/plains_track"):
        load_texture(f"assets/{track_texture}.png")
    for particle_texture in ("sand", "grass", "snow", "plains"):
        load_texture(f"assets/particles/particle_{particle_texture}_track.png")

def load_models():
    models_to_load = [
        "car.obj", "sand_track.obj", "grass_track.obj", "snow_track.obj",
        "plains_track.obj", "sand_track_bounds.obj", "grass_track_bounds.obj",
        "snow_track_bounds.obj", "plains_track_bounds.obj"
    ]
    for i, m in enumerate(models_to_load):
        load_model(m)

try:
    thread.start_new_thread(function = load_textures, args = "")
    thread.start_new_thread(function = load_models, args = "")
except Exception as e:
    print("error starting thread", e)

# Car

car = Car()

# Tracks

sand_track = SandTrack(car)
grass_track = GrassTrack(car)
snow_track = SnowTrack(car)
plains_track = PlainsTrack(car)

car.sand_track = sand_track
car.grass_track = grass_track
car.snow_track = snow_track
car.plains_track = plains_track

# AI

ai = AICar(car, sand_track, grass_track, snow_track, plains_track)
ai1 = AICar(car, sand_track, grass_track, snow_track, plains_track)
ai2 = AICar(car, sand_track, grass_track, snow_track, plains_track)
ai.disable()
ai1.disable()
ai2.disable()

ai_list = [ai, ai1, ai2]

car.ai_list = ai_list

ai.ai_list = ai_list
ai1.ai_list = ai_list
ai2.ai_list = ai_list

# Main menu

main_menu = MainMenu(car, ai_list, sand_track, grass_track, snow_track, plains_track)

car.multiplayer = False
car.multiplayer_update = False

# Achievements
achievements = RallyAchievements(car, main_menu, sand_track, grass_track, snow_track, plains_track)

# Lighting + shadows

sun = SunLight(direction = (-0.7, -0.9, 0.5), resolution = 2048, car = car)
ambient = AmbientLight(color = Vec4(0.5, 0.55, 0.66, 0) * 0.75)

render.setShaderAuto()

# Sky

Sky(texture = "sky")

def update():
    # If multiplayer, Call the Multiplayer class
    if car.multiplayer == True:
        global multiplayer
        multiplayer = Multiplayer(car)
        car.multiplayer_update = True
        car.multiplayer = False
    
    # Update the multiplayer and check whether the client is connected
    if car.multiplayer_update:
        multiplayer.update_multiplayer()
        if multiplayer.client.connected:
            if car.connected_text == True:
                main_menu.connected.enable()
                car.connected_text = False
            else:
                invoke(main_menu.connected.disable, delay = 2)
            main_menu.not_connected.disable()
        else:
            if car.disconnected_text == True:
                main_menu.not_connected.enable()
                car.disconnected_text = False
            else:
                invoke(main_menu.not_connected.disable, delay = 2)
            main_menu.connected.disable()

    # If the user is hosting the server, update the server
    if car.server_running:
        car.server.update_server()
        if car.server.server_update == True:
            car.server.easy.process_net_events()
    
    if achievements.time_spent < 10:
        achievements.time_spent += time.dt

    if car.enabled:
        car.graphics_parent.enable()
    else:
        car.graphics_parent.disable()

def input(key):
    # If multiplayer, send the client's position, rotation, texture, username and highscore to the server
    if car.multiplayer_update:
        multiplayer.client.send_message("MyPosition", tuple(multiplayer.car.position))
        multiplayer.client.send_message("MyRotation", tuple(multiplayer.car.rotation))
        multiplayer.client.send_message("MyTexture", str(multiplayer.car.graphics.texture))
        multiplayer.client.send_message("MyUsername", str(multiplayer.car.username_text))
        multiplayer.client.send_message("MyHighscore", str(round(multiplayer.car.highscore_count, 2)))

app.run()