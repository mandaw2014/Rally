from ursina import *
from ursinanetworking import *
from direct.stdpy import thread

from car import Car, CarRepresentation

from main_menu import MainMenu

from tracks.sand_track import SandTrack
from tracks.grass_track import GrassTrack
from tracks.snow_track import SnowTrack

# application.development_mode = False

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

car.multiplayer = True

main_menu = MainMenu(car, sand_track, grass_track, snow_track)

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

if car.multiplayer == True:
    client = UrsinaNetworkingClient("localhost", 25565)
    easy = EasyUrsinaNetworkingClient(client)

    players = {}
    players_target_pos = {}
    players_target_rot = {}

    selfId = -1

    @client.event
    def GetId(id):
        global selfId
        selfId = id
        print(f"My ID is : {selfId}")

    @easy.event
    def onReplicatedVariableCreated(variable):
        global client
        variable_name = variable.name
        variable_type = variable.content["type"]

        if variable_type == "player":
            players_target_pos[variable_name] = Vec3(-80, -30, 15)
            players_target_rot[variable_name] = Vec3(0, 90, 0)
            players[variable_name] = CarRepresentation((-80, -30, 15), (0, 90, 0))

            if selfId == int(variable.content["id"]):
                players[variable_name].color = color.red
                players[variable_name].visible = False

    @easy.event
    def onReplicatedVariableUpdated(variable):
        players_target_pos[variable.name] = variable.content["position"]
        players_target_rot[variable.name] = variable.content["rotation"]

    @easy.event
    def onReplicatedVariableRemoved(variable):
        variable_name = variable.name
        variable_type = variable.content["type"]
        
        if variable_type == "player":
            destroy(players[variable_name])
            del players[variable_name]

def update():
    if car.multiplayer == True:
        for p in players:
            players[p].position += (Vec3(players_target_pos[p]) - players[p].position) / 25
            players[p].rotation += (Vec3(players_target_rot[p]) - players[p].rotation) / 25

        easy.process_net_events()

def input(key):
    if car.multiplayer == True:
        client.send_message("MyPosition", tuple(car.position))
        client.send_message("MyRotation", tuple(car.rotation))
    
    if main_menu.main_menu.enabled == False and main_menu.settings_menu.enabled == False and main_menu.maps_menu.enabled == False and main_menu.garage_menu.enabled == False and main_menu.controls_menu.enabled == False:
        if key == "escape":
            main_menu.pause_menu.enabled = not main_menu.pause_menu.enabled
            mouse.locked = not mouse.locked

app.run()