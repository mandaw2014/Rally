from UrsinaAchievements import create_achievement

class RallyAchievements():
    def __init__(self, car, main_menu, sand_track, grass_track, snow_track, plains_track):
        self.car = car
        self.main_menu = main_menu
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.plains_track = plains_track
        
        self.time_spent = 0

        create_achievement("Play the game!", self.play_the_game, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Sand Track for the first time!", self.play_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Grass Track for the first time!", self.play_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Snow Track for the first time!", self.play_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Plains Track for the first time!", self.play_plains_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race against AI!", self.race_against_ai, icon = "confetti.png", ringtone = None)
        create_achievement("Play Multiplayer!", self.play_multiplayer, icon = "confetti.png", ringtone = None)
        create_achievement("Go to the Garage!", self.garage, icon = "confetti.png", ringtone = None)
        create_achievement("Play Time Trial!", self.time_trial, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 20s on Sand Track!", self.twenty_seconds_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 17s on Sand Track!", self.seventeen_seconds_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 16s on Sand Track!", self.sixteen_seconds_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 15s on Sand Track!", self.fifteen_seconds_sand_track, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 22s on Grass Track!", self.twentytwo_seconds_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 20s on Grass Track!", self.twenty_seconds_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 19s on Grass Track!", self.nineteen_seconds_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 18s on Grass Track!", self.eighteen_seconds_grass_track, icon = "confetti.png", ringtone = None)
        
        create_achievement("Get under 40s on Snow Track!", self.fourty_seconds_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 35s on Snow Track!", self.thirtyfive_seconds_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 33s on Snow Track!", self.thirtythree_seconds_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 30s on Snow Track!", self.thirty_seconds_snow_track, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 30s on Plains Track!", self.thirty_seconds_plains_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 28s on Plains Track!", self.twentyeight_seconds_plains_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 26s on Plains Track!", self.twentysix_seconds_plains_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 24s on Plains Track!", self.twentyfour_seconds_plains_track, icon = "confetti.png", ringtone = None)

        create_achievement("Beat Mandaw in Sand Track!", self.beat_mandaw_in_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Grass Track!", self.beat_mandaw_in_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Snow Track!", self.beat_mandaw_in_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Plains Track!", self.beat_mandaw_in_plains_track, icon = "confetti.png", ringtone = None)

    def play_the_game(self):
        return self.time_spent > 3

    def play_sand_track(self):
        return self.sand_track.played
    
    def play_grass_track(self):
        return self.grass_track.played

    def play_snow_track(self):
        return self.snow_track.played

    def play_plains_track(self):
        return self.plains_track.played

    def race_against_ai(self):
        return self.car.ai_list[0].enabled

    def play_multiplayer(self):
        return self.car.multiplayer_update

    def garage(self):
        return self.main_menu.garage_menu.enabled

    def time_trial(self):
        return self.car.time_trial

    def twenty_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 20

    def seventeen_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 17

    def sixteen_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 16

    def fifteen_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 15

    def twentytwo_seconds_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 22

    def twenty_seconds_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 20

    def nineteen_seconds_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 19

    def eighteen_seconds_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 18

    def fourty_seconds_snow_track(self):
        if self.snow_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 40

    def thirtyfive_seconds_snow_track(self):
        if self.snow_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 35

    def thirtythree_seconds_snow_track(self):
        if self.snow_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 33

    def thirty_seconds_snow_track(self):
        if self.snow_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 30

    def thirty_seconds_plains_track(self):
        if self.plains_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 30

    def twentyeight_seconds_plains_track(self):
        if self.plains_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 28

    def twentysix_seconds_plains_track(self):
        if self.plains_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 26

    def twentyfour_seconds_plains_track(self):
        if self.plains_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 24

    def beat_mandaw_in_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 14.49

    def beat_mandaw_in_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 17.79
    
    def beat_mandaw_in_snow_track(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 31.45

    def beat_mandaw_in_plains_track(self):
        if self.plains_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 24.66