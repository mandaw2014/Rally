from ursina import *
from car import Car

app = Ursina()

car = Car((0, 10, 4), topspeed = 30)

sand_track = Entity(model = "sand_track.obj", texture = "sand_track.png", position = (-80, -50, -75), scale = (10, 10, 10), collider = "mesh")
sand_track.finish_line = Entity(position = (24, -43.5, 7), collider = "box", rotation = (0, -251, 0), scale = (20, 5, 3), visible = False)
sand_track.boundaries = Entity(model = "sand_track_bounds.obj", collider = "mesh", position = (-80, -50, -75), scale = (10, 10, 10), visible = False)

sand_track.wall1 = Entity(model = "cube", position = (-29, 450, -39.8), rotation = (0, 313, 0), collider = "box", scale = (5, 2000, 40), visible = False)
sand_track.wall2 = Entity(model = "cube", position = (-40, 450, -71.8), rotation = (0, 325, 0), collider = "box", scale = (5, 2000, 40), visible = False)
sand_track.wall3 = Entity(model = "cube", position = (-15, 450, -69.5), rotation = (0, 566.549, 0), collider = "box", scale = (5, 2000, 40), visible = False)
sand_track.wall4 = Entity(model = "cube", position = (-43, 450, -41.6), rotation = (0, 751.312, 0), collider = "box", scale = (5, 2000, 40), visible = False)

sand_track.wall_trigger = Entity(model = "cube", position = (-72, 450, -84.9), rotation = (0, 447.72, 0), collider = "box", scale = (50, 2000, 5), visible = False)

car.sand_track = sand_track

camera.clip_plane_far = 250

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

        sand_track.wall1.enable()
        sand_track.wall2.enable()
        sand_track.wall3.disable()
        sand_track.wall4.disable()

        invoke(car.reset_timer, delay = 3)

    if car.intersects(sand_track.boundaries):
        car.speed = 10

    if car.intersects(sand_track.wall_trigger):
        sand_track.wall1.disable()
        sand_track.wall2.disable()
        sand_track.wall3.enable()
        sand_track.wall4.enable()

app.run()