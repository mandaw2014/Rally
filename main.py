from ursina import *
from car import Car

app = Ursina()

car = Car((0, 30, 0), topspeed = 30)

track = Entity(model = "sand_track.obj", texture = "sand_track.png", position = (-80, -50, -75), scale = (10, 10, 10), collider = "mesh")

# EditorCamera()

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

app.run()
