from ursina import *
from car import Car

app = Ursina()

car = Car((0, 10, 4), topspeed = 30)

sand_track = Entity(model = "sand_track.obj", texture = "sand_track.png", position = (-80, -50, -75), scale = (10, 10, 10), collider = "mesh")
sand_track.finish_line = Entity(position = (24, -43.5, 7), collider = "box", rotation = (0, -251, 0), scale = (20, 5, 3), visible = False)
sand_track.boundaries = Entity(model = "sand_track_bounds.obj", collider = "mesh", position = (-80, -50, -75), scale = (10, 10, 10), visible = False)

car.sand_track = sand_track

PointLight(parent = camera, color = color.white, position = (0, 10, -1.5))
AmbientLight(color = color.rgba(100, 100, 100, 0.1))

Sky()

def update():
    if car.intersects(sand_track.finish_line):
        car.timer_running = True
        car.last_count = car.count
        car.reset_count = 0.0
        car.timer.disable()
        car.reset_count_timer.enable()

        if car.last_count <= car.highscore_count and car.last_count >= 10:
            car.highscore_count = car.last_count
        if car.highscore_count <= 13:
            car.highscore_count = car.last_count

        with open("highscore.txt", "w") as highscore:
            highscore.write(str(car.highscore_count))

        invoke(car.reset_timer, delay = 3)

    if car.intersects(sand_track.boundaries):
        car.speed = 10

app.run()