from ursina import *
from direct.stdpy import thread
# from direct.actor.Actor import Actor

from car import Car

from main_menu import MainMenu

from tracks.sand_track import SandTrack
from tracks.grass_track import GrassTrack
from tracks.snow_track import SnowTrack

app = Ursina()
window.borderless = False
window.fullscreen = True
window.cog_button.disable()
window.show_ursina_splash = True

# Loading car textures

def load_car_textures():
    for car_texture in ("black", "blue", "green", "orange", "red", "white"):
        load_texture(f"assets/garage/car-{car_texture}.png")

try:
    thread.start_new_thread(function = load_car_textures, args = "")
except Exception as e:
    print("error starting thread", e)

car = Car((0, 0, 4), topspeed = 30)
car.disable()

sand_track = SandTrack(car)
grass_track = GrassTrack(car)
snow_track = SnowTrack(car)

car.sand_track = sand_track
car.grass_track = grass_track
car.snow_track = snow_track

main_menu = MainMenu(car, sand_track, grass_track, snow_track)

# ai_car = Entity(position = (0, 0, 0), rotation = (0, 0, 0), scale = (1, 1, 1))
# actor = Actor("./assets/ai/ai_car.gltf", {"drive": "./assets/ai/ai_car.gltf"})
# actor.reparentTo(ai_car)
# actor.loop("drive")

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def input(key):
    if main_menu.main_menu.enabled == False and main_menu.settings_menu.enabled == False and main_menu.maps_menu.enabled == False and main_menu.garage_menu.enabled == False and main_menu.controls_menu.enabled == False:
        if key == "escape":
            main_menu.pause_menu.enabled = not main_menu.pause_menu.enabled
            mouse.locked = not mouse.locked

app.run()