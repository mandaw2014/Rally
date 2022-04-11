from ursina import *
from car import Car

from main_menu import MainMenu

from sand_track import SandTrack
from grass_track import GrassTrack

app = Ursina()
window.borderless = False
window.fullscreen = True
window.cog_button.disable()
window.show_ursina_splash = True

car = Car((0, 0, 4), topspeed = 30)
car.disable()

sand_track = SandTrack(car)
grass_track = GrassTrack(car)

garage = Entity(model = "cube", color = color.white, position = (car.x, car.y - 2, car.z), rotation_y = 45, scale = (10, 1, 10))
garage.disable()

car.sand_track = sand_track
car.grass_track = grass_track

# camera.clip_plane_far = 250

main_menu = MainMenu(car, sand_track, grass_track, garage)

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def input(key):
    if main_menu.main_menu.enabled == False:
        if key == "escape":
            main_menu.pause_menu.enabled = not main_menu.pause_menu.enabled
            mouse.locked = not mouse.locked  

app.run()