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
        # Cars
        "sports-car.obj", "muscle-car.obj", "limousine.obj", "lorry.obj", "hatchback.obj", "rally-car.obj",
        # Tracks
        "sand_track.obj", "grass_track.obj", "snow_track.obj",
        "forest_track.obj", "savannah_track.obj", "lake_track.obj", "particles.obj",
        # Track Bounds
        "sand_track_bounds.obj", "grass_track_bounds.obj", "snow_track_bounds.obj", 
        "forest_track_bounds.obj", "savannah_track_bounds.obj", "lake_track_bounds.obj",
        # Track Details
        "rocks-sand.obj", "cacti-sand.obj", "trees-grass.obj", "thintrees-grass.obj", "rocks-grass.obj", "grass-grass_track.obj", "trees-snow.obj", 
        "thintrees-snow.obj", "rocks-snow.obj", "trees-forest.obj", "thintrees-forest.obj", "rocks-savannah.obj", "trees-savannah.obj",
        "trees-lake.obj", "thintrees-lake.obj", "rocks-lake.obj", "bigrocks-lake.obj", "grass-lake.obj", "lake_bounds.obj",
        # Cosmetics
        "viking_helmet.obj", "duck.obj", "banana.obj", "surfinbird.obj", "surfboard.obj"
    ]

    textures_to_load = [
        # Car Textures
        # Sports Car
        "sports-red.png", "sports-orange.png", "sports-green.png", "sports-white.png", "sports-black.png", "sports-blue.png", 
        # Muscle Car
        "muscle-red.png", "muscle-orange.png", "muscle-green.png", "muscle-white.png", "muscle-black.png", "muscle-blue.png", 
        # Limo
        "limo-red.png", "limo-orange.png", "limo-green.png", "limo-white.png", "limo-black.png", "limo-blue.png", 
        # Lorry
        "lorry-red.png", "lorry-orange.png", "lorry-green.png", "lorry-white.png", "lorry-black.png", "lorry-blue.png", 
        # Limo
        "limo-red.png", "limo-orange.png", "limo-green.png", "limo-white.png", "limo-black.png", "limo-blue.png", 
        # Hatchback
        "hatchback-red.png", "hatchback-orange.png", "hatchback-green.png", "hatchback-white.png", "hatchback-black.png", "hatchback-blue.png",
        # Rally Car
        "rally-red.png", "rally-orange.png", "rally-green.png", "rally-white.png", "rally-black.png", "rally-blue.png",
        # Track Textures
        "sand_track.png", "grass_track.png", "snow_track.png", "forest_track.png",
        "savannah_track.png", "lake_track.png",
        # Track Detail Textures
        "rock-sand.png", "cactus-sand.png", "tree-grass.png", "thintree-grass.png", "rock-grass.png", "grass-grass_track.png", "tree-snow.png", 
        "thintree-snow.png", "rock-snow.png", "tree-forest.png", "thintree-forest.png", "rock-savannah.png", "tree-savannah.png", 
        "tree-lake.png", "rock-lake.png", "grass-lake.png", "thintree-lake.png", "bigrock-lake.png",
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
car.sports_car()

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
sun = SunLight(direction = (-0.7, -0.9, 0.5), resolution = 3072, car = car)
ambient = AmbientLight(color = Vec4(0.5, 0.55, 0.66, 0) * 0.75)

render.setShaderAuto()

main_menu.sun = sun

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
        multiplayer.client.send_message("MyCosmetic", str(car.current_cosmetic))
        multiplayer.client.send_message("MyModel", str(car.model_path))

app.run()