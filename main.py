from ursina import *
from ursinanetworking import *
from direct.stdpy import thread

from car import Car
from ai import AICar

from multiplayer import Multiplayer
from main_menu import MainMenu

from sun import SunLight

from tracks.sand_track import SandTrack
from tracks.grass_track import GrassTrack
from tracks.snow_track import SnowTrack
from tracks.plains_track import PlainsTrack

Text.default_resolution = 1080 * Text.size

# Window

app = Ursina()
window.title = "Rally"
window.borderless = False
window.fullscreen = True
window.show_ursina_splash = True
window.cog_button.disable()
window.fps_counter.disable()

# Starting new thread for loading textures

def load_car_textures():
    for car_texture in ("black", "blue", "green", "orange", "red", "white"):
        load_texture(f"assets/garage/car-{car_texture}.png")

try:
    thread.start_new_thread(function = load_car_textures, args = "")
except Exception as e:
    print("error starting thread", e)

# Car

car = Car((0, 0, 4), (0, 0, 0), topspeed = 30)
car.disable()

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

# Main menu

main_menu = MainMenu(car, ai_list, sand_track, grass_track, snow_track, plains_track)

car.multiplayer = False
car.multiplayer_update = False

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

def input(key):
    # Pause menu
    if main_menu.main_menu.enabled == False and main_menu.start_menu.enabled == False and main_menu.server_menu.enabled == False and main_menu.settings_menu.enabled == False and main_menu.maps_menu.enabled == False and main_menu.garage_menu.enabled == False and main_menu.controls_menu.enabled == False and main_menu.host_menu.enabled == False and main_menu.created_server_menu.enabled == False and main_menu.video_menu.enabled == False and main_menu.gameplay_menu.enabled == False:
        if key == "escape":
            main_menu.pause_menu.enabled = not main_menu.pause_menu.enabled
            mouse.locked = not mouse.locked

        if car.reset_count_timer.enabled == False:
            car.timer.enable()
        else:
            car.timer.disable()
            
        car.highscore.enable()
    
    else:
        car.timer.disable()
        car.highscore.disable()

    # If multiplayer, send the client's position, rotation, texture, username and highscore to the server
    if car.multiplayer_update:
        multiplayer.client.send_message("MyPosition", tuple(multiplayer.car.position))
        multiplayer.client.send_message("MyRotation", tuple(multiplayer.car.rotation))
        multiplayer.client.send_message("MyTexture", str(multiplayer.car.texture))
        multiplayer.client.send_message("MyUsername", str(multiplayer.car.username_text))
        multiplayer.client.send_message("MyHighscore", str(round(multiplayer.car.highscore_count, 2)))

app.run()