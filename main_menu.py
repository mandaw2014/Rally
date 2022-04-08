from ursina import *
import os

class MainMenu(Entity):
    def __init__(self, car):
        super().__init__(
            parent = camera.ui
        )

        self.main_menu = Entity(parent = self, enabled = True)
        self.pause_menu = Entity(parent = self, enabled = False)
        self.car = car

        def start():
            self.car.enable()
            mouse.locked = True
            self.main_menu.disable()

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

        def respawn():
            self.car.position = (0, -40, 4)
            self.car.rotation = (0, 65, 0)
            self.car.speed = 0
            self.car.count = 0.0
            self.car.reset_count = 0.0
            self.car.timer_running = False
            self.car.anti_cheat = 1

        def reset_highscore():
            path = os.path.dirname(os.path.abspath(__file__))
            highscore = os.path.join(path, "./highscore.txt")

            with open(highscore, "w") as hs:
                hs.write(str(0.0))

            path = os.path.dirname(os.path.abspath(__file__))
            highscore = os.path.join(path, "./highscore.txt")

            with open(highscore, "r") as hs:
                self.car.highscore_count = hs.read()

            self.car.highscore_count = float(self.car.highscore_count)

        title = Entity(model = "quad", scale = (0.5, 0.2, 0.2), texture = "rally-logo", parent = self.main_menu, y = 0.3)

        start_button = Button(text = "S t a r t - G a m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.02, parent = self.main_menu)
        reset_highsore_button = Button(text = "R e s e t - H i g h s c o r e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.1, parent = self.main_menu)
        quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.22, parent = self.main_menu)
        quit_button.on_click = application.quit
        start_button.on_click = Func(start)
        reset_highsore_button.on_click = Func(reset_highscore)

        p_resume_button = Button(text = "R e s u m e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.23, parent = self.pause_menu)
        p_respawn_button = Button(text = "R e s p a w n", color = color.black, scale_y = 0.1, scale_x = 0.3, y = 0.11, parent = self.pause_menu)
        p_reset_highsore_button = Button(text = "R e s e t - H i g h s c o r e", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.01, parent = self.pause_menu)
        p_quit_button = Button(text = "Q u i t", color = color.black, scale_y = 0.1, scale_x = 0.3, y = -0.13, parent = self.pause_menu)
        p_quit_button.on_click = application.quit
        p_reset_highsore_button.on_click = Func(reset_highscore)
        p_respawn_button.on_click = Func(respawn)
        p_resume_button.on_click = Func(resume)