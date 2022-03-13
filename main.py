from ursina import *
from car import Car

app = Ursina()

car = Car((0, 10, 4), topspeed = 30)

sand_track = Entity(model = "sand_track.obj", texture = "sand_track.png", position = (-80, -50, -75), scale = (10, 10, 10), collider = "mesh")
finish_line = Entity(position = (24, -43.5, 7), collider = "box", rotation = (0, -251, 0), scale = (20, 5, 3))

car.sand_track = sand_track

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def update():
    if car.intersects(finish_line):
        car.timer_running = True
        car.last_count = car.count
        car.reset_count = 0.0
        car.timer.disable()
        car.reset_count_timer.enable()
        invoke(car.reset_timer, delay = 3)

app.run()