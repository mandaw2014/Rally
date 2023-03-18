from ursina import *

class Menu(Entity):
    def __init__(self, parent_menu = None, **kwargs):
        super().__init__(**kwargs)
        self.parent_menu = parent_menu

    def on_toggle(self):
        pass

    def toggle(self):
        self.enabled = not self.enabled
        self.on_toggle()
        self.parent_menu.enabled = not self.parent_menu.enabled

