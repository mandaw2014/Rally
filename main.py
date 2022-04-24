from ursina import *
from ursinanetworking import *
from direct.stdpy import thread

from car import Car

from multiplayer import Multiplayer

from main_menu import MainMenu

from tracks.sand_track import SandTrack
from tracks.grass_track import GrassTrack
from tracks.snow_track import SnowTrack

application.development_mode = False
Text.default_resolution = 1080 * Text.size

app = Ursina()
window.borderless = False
window.fullscreen = True
window.show_ursina_splash = True

# Loading car textures

def load_car_textures():
    for car_texture in ("black", "blue", "green", "orange", "red", "white"):
        load_texture(f"assets/garage/car-{car_texture}.png")

try:
    thread.start_new_thread(function = load_car_textures, args = "")
except Exception as e:
    print("error starting thread", e)

car = Car((0, 0, 4), (0, 0, 0), topspeed = 30)
car.disable()

sand_track = SandTrack(car)
grass_track = GrassTrack(car)
snow_track = SnowTrack(car)

car.sand_track = sand_track
car.grass_track = grass_track
car.snow_track = snow_track

main_menu = MainMenu(car, sand_track, grass_track, snow_track)

car.multiplayer = False
car.multiplayer_update = False

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def update():
    if car.multiplayer == True:
        global multiplayer
        multiplayer = Multiplayer(car)
        car.multiplayer_update = True
        car.multiplayer = False

    if car.multiplayer_update:
        multiplayer.update_multiplayer()

def input(key):
    if main_menu.main_menu.enabled == False and main_menu.server_menu.enabled == False and main_menu.settings_menu.enabled == False and main_menu.maps_menu.enabled == False and main_menu.garage_menu.enabled == False and main_menu.controls_menu.enabled == False:
        if key == "escape":
            main_menu.pause_menu.enabled = not main_menu.pause_menu.enabled
            mouse.locked = not mouse.locked

    if car.multiplayer_update:
        multiplayer.client.send_message("MyPosition", tuple(multiplayer.car.position))
        multiplayer.client.send_message("MyRotation", tuple(multiplayer.car.rotation))
        multiplayer.client.send_message("MyTexture", str(multiplayer.car.texture))
        multiplayer.client.send_message("MyUsername", str(multiplayer.car.username_text))
        multiplayer.client.send_message("MyHighscore", str(round(multiplayer.car.highscore_count, 2)))

app.run()