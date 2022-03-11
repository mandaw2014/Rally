from ursina import *
from car import Car

app = Ursina()

car = Car((0, 10, 4), topspeed = 30)

track = Entity(model = "sand_track.obj", texture = "sand_track.png", position = (-80, -50, -75), scale = (10, 10, 10), collider = "mesh")
finish_line = Entity(position = (24, -44.5, 7), collider = "box", rotation = (0, -251, 0), scale = (15, 1, 1))

# EditorCamera()

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def update():
    if car.intersects(finish_line):
        car.timer_running = not car.timer_running
        return

app.run()