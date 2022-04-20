from ursinanetworking import *
from ursina import *
from car import CarRepresentation

class Multiplayer(Entity):
    def __init__(self, car):
        self.car = car

        self.client = UrsinaNetworkingClient(self.car.ip.text, 25565)
        self.easy = EasyUrsinaNetworkingClient(self.client)

        self.players = {}
        self.players_target_pos = {}
        self.players_target_rot = {}
        self.players_target_tex = {}

        self.selfId = -1

        @self.client.event
        def GetId(id):
            self.selfId = id
            print(f"My ID is : {self.selfId}")

        @self.easy.event
        def onReplicatedVariableCreated(variable):
            variable_name = variable.name
            variable_type = variable.content["type"]

            if variable_type == "player":
                self.players_target_pos[variable_name] = Vec3(-80, -30, 15)
                self.players_target_rot[variable_name] = Vec3(0, 90, 0)
                self.players_target_tex[variable_name] = "./assets/garage/car-red.png"
                self.players[variable_name] = CarRepresentation((-80, -30, 15), (0, 90, 0))

                if self.selfId == int(variable.content["id"]):
                    self.players[variable_name].color = color.red
                    self.players[variable_name].visible = False

        @self.easy.event
        def onReplicatedVariableUpdated(variable):
            self.players_target_pos[variable.name] = variable.content["position"]
            self.players_target_rot[variable.name] = variable.content["rotation"]
            self.players_target_tex[variable.name] = variable.content["texture"]

        @self.easy.event
        def onReplicatedVariableRemoved(variable):
            variable_name = variable.name
            variable_type = variable.content["type"]
            
            if variable_type == "player":
                destroy(self.players[variable_name])
                del self.players[variable_name]

    def update_multiplayer(self):
        for p in self.players:
            self.players[p].position += (Vec3(self.players_target_pos[p]) - self.players[p].position) / 25
            self.players[p].rotation += (Vec3(self.players_target_rot[p]) - self.players[p].rotation) / 25
            self.players[p].texture = f"{self.players_target_tex[p]}"

        self.easy.process_net_events()