from ursina import *
from car import Car

app = Ursina()

car = Car((0, 30, 0), topspeed = 30)

# ground = Entity(model = "cube", scale = (10, 1, 10), position = (0, -15, 0), collider = "box")

track = Entity(model = "sand_track.obj", texture = "track1(1).png", position = (-80, -50, -75), scale = (10, 10, 10), collider = "mesh")
# track = Entity(model = "track.obj", texture = "mountain_track_road.png", position = (-80, -50, 0), scale = (15, 15, 15), collider = "mesh")

# EditorCamera()

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def update():
    print(car.rotation_y)
    pass

app.run()