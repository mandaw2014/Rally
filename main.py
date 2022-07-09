from ursina import *
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
from tracks.forest_track import ForestTrack
from tracks.savannah_track import SavannahTrack
from tracks.lake_track import LakeTrack

Text.default_font = "./assets/Roboto.ttf"
Text.default_resolution = 1080 * Text.size

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

# Starting new thread for assets

def load_assets():
    models_to_load = [
        # Tracks
        "car.obj", "sand_track.obj", "grass_track.obj", "snow_track.obj",
        "forest_track.obj", "savannah_track.obj", "lake_track.obj", "particles.obj",
        # Track Bounds
        "sand_track_bounds.obj", "grass_track_bounds.obj", "snow_track_bounds.obj", 
        "forest_track_bounds.obj", "savannah_track_bounds.obj", "lake_track_bounds.obj",
        # Track Details
        "rocks-sand.obj", "trees-grass.obj", "trees-snow.obj", "trees-forest.obj", "rocks-savannah.obj",
        "trees-lake.obj", "rocks-lake.obj", "lake_bounds.obj",
        # Cosmetics
        "viking_helmet.obj", "duck.obj", "banana.obj", "surfinbird.obj", "surfboard.obj"
    ]

    textures_to_load = [
        # Car Textures
        "car-red.png", "car-orange.png", "car-green.png", "car-white.png", "car-black.png",
        "car-blue.png", 
        # Track Textures
        "sand_track.png", "grass_track.png", "snow_track.png", "forest_track.png",
        "savannah_track.png", "lake_track.png",
        # Track Detail Textures
        "rock-sand.png", "tree-grass.png", "tree-snow.png", "tree-forest.png", "rock-savannah.png",
        "tree-lake.png", "rock-lake.png",
        # Particle Textures
        "particle_sand_track.png", "particle_grass_track.png", "particle_snow_track", 
        "particle_forest_track.png", "particle_savannah_track.png", "particle_lake_track.png",
        # Cosmetic Textures + Icons
        "viking_helmet.png", "surfinbird.png", "surfboard.png", "viking_helmet-icon.png", "duck-icon.png",
        "banana-icon.png", "surfinbird-icon.png"
    ]

    for i, m in enumerate(models_to_load):
        load_model(m)

    for i, t in enumerate(textures_to_load):
        load_texture(t)

try:
    thread.start_new_thread(function = load_assets, args = "")
except Exception as e:
    print("error starting thread", e)

# Car
car = Car()

# Tracks
sand_track = SandTrack(car)
grass_track = GrassTrack(car)
snow_track = SnowTrack(car)
forest_track = ForestTrack(car)
savannah_track = SavannahTrack(car)
lake_track = LakeTrack(car)

car.sand_track = sand_track
car.grass_track = grass_track
car.snow_track = snow_track
car.forest_track = forest_track
car.savannah_track = savannah_track
car.lake_track = lake_track

# AI
ai_list = []

ai = AICar(car, ai_list, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track)
ai1 = AICar(car, ai_list, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track)
ai2 = AICar(car, ai_list, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track)

ai_list.append(ai)
ai_list.append(ai1)
ai_list.append(ai2)

car.ai_list = ai_list

# Main menu
main_menu = MainMenu(car, ai_list, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track)

# Achievements
achievements = RallyAchievements(car, main_menu, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track)

# Lighting + shadows
sun = SunLight(direction = (-0.7, -0.9, 0.5), resolution = 2048, car = car)
ambient = AmbientLight(color = Vec4(0.5, 0.55, 0.66, 0) * 0.75)

render.setShaderAuto()

# Sky
Sky(texture = "sky")

def update():
    # If multiplayer, Call the Multiplayer class
    if car.multiplayer:
        global multiplayer
        multiplayer = Multiplayer(car)
        car.multiplayer_update = True
        car.multiplayer = False
    
    # Update the multiplayer and check whether the client is connected
    if car.multiplayer_update:
        multiplayer.update_multiplayer()
        if multiplayer.client.connected:
            if car.connected_text:
                main_menu.connected.enable()
                car.connected_text = False
            else:
                invoke(main_menu.connected.disable, delay = 2)
            main_menu.not_connected.disable()
        else:
            if car.disconnected_text:
                main_menu.not_connected.enable()
                car.disconnected_text = False
            else:
                invoke(main_menu.not_connected.disable, delay = 2)
            main_menu.connected.disable()

    # If the user is hosting the server, update the server
    if car.server_running:
        car.server.update_server()
        if car.server.server_update:
            car.server.easy.process_net_events()
    
    if achievements.time_spent < 10:
        achievements.time_spent += time.dt

def input(key):
    # If multiplayer, send the client's position, rotation, texture, username and highscore to the server
    if car.multiplayer_update:
        multiplayer.client.send_message("MyPosition", tuple(car.position))
        multiplayer.client.send_message("MyRotation", tuple(car.rotation))
        multiplayer.client.send_message("MyTexture", str(car.texture))
        multiplayer.client.send_message("MyUsername", str(car.username_text))
        multiplayer.client.send_message("MyHighscore", str(round(car.highscore_count, 2)))

app.run()