from ursinanetworking import *

print("\nHello from the Rally Server!\n")

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.start_server = False
        self.server_update = False

    def update_server(self):
        if self.start_server:
            self.server = UrsinaNetworkingServer(self.ip.text, int(self.port.text))
            self.easy = EasyUrsinaNetworkingServer(self.server)
            
            @self.server.event
            def onClientConnected(client):
                self.easy.create_replicated_variable(
                    f"player_{client.id}",
                    { "type" : "player", "id" : client.id, "username": "Guest", "position": (0, 0, 0), "rotation" : (0, 0, 0), "model" : "sports-car.obj", "texture" : "sports-red.png", "highscore": 0.0, "cosmetic": "none"}
                )
                print(f"{client} connected!")
                client.send_message("GetId", client.id)

            @self.server.event
            def onClientDisconnected(client):
                self.easy.remove_replicated_variable_by_name(f"player_{client.id}")
                
            @self.server.event
            def MyPosition(client, newpos):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "position", newpos)

            @self.server.event
            def MyRotation(client, newrot):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "rotation", newrot)

            @self.server.event
            def MyModel(client, newmodel):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "model", newmodel)

            @self.server.event
            def MyTexture(client, newtex):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "texture", newtex)

            @self.server.event
            def MyUsername(client, newuser):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "username", newuser)
        
            @self.server.event
            def MyHighscore(client, newscore):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "highscore", newscore)

            @self.server.event
            def MyCosmetic(client, newcos):
                self.easy.update_replicated_variable_by_name(f"player_{client.id}", "cosmetic", newcos)

            self.server_update = True
            self.start_server = False

if __name__ == "__main__":
    from ursina import *

    app = Ursina()
    window.title = "Rally"
    window.borderless = False

    ip = InputField(default_value = "IP", limit_content_to = "0123456789.localhost", color = color.black, alpha = 100, y = 0.1, parent = camera.ui)
    port = InputField(default_value = "PORT", limit_content_to = "0123456789", color = color.black, alpha = 100, y = 0.02, parent = camera.ui)

    server = Server(ip, port)

    Sky()

    def create_server():
        server.start_server = True
        running = Text(text = "Running server...", scale = 1.5, line_height = 2, x = 0, origin = 0, y = 0, parent = camera.ui)
        create_server_button.disable()
        ip.disable()
        port.disable()
        stop_button.enable()

    def stop_server():
        import os
        os._exit(0)

    create_server_button = Button(text = "C r e a t e", color = color.hex("F58300"), highlight_color = color.gray, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = camera.ui)
    create_server_button.on_click = Func(create_server)

    stop_button = Button(text = "S t o p", color = color.hex("D22828"), scale_y = 0.1, scale_x = 0.3, y = -0.2, parent = camera.ui)
    stop_button.disable()
    stop_button.on_click = Func(stop_server)
    
    def update():
        server.update_server()
        if server.server_update == True:
            server.easy.process_net_events()

    app.run()