from UrsinaAchievements import create_achievement

class RallyAchievements():
    def __init__(self, car, main_menu, sand_track, grass_track, snow_track, forest_track, savannah_track):
        self.car = car
        self.main_menu = main_menu
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forest_track = forest_track
        self.savannah_track = savannah_track
        
        self.time_spent = 0

        create_achievement("Play the game!", self.play_the_game, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Sand Track for the first time!", self.play_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Grass Track for the first time!", self.play_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Snow Track for the first time!", self.play_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Plains Track for the first time!", self.play_forest_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race on Savannah Track for the first time!", self.play_savannah_track, icon = "confetti.png", ringtone = None)
        create_achievement("Race against AI!", self.race_against_ai, icon = "confetti.png", ringtone = None)
        create_achievement("Play Multiplayer!", self.play_multiplayer, icon = "confetti.png", ringtone = None)
        create_achievement("Go to the Garage!", self.garage, icon = "confetti.png", ringtone = None)
        create_achievement("Play Time Trial!", self.time_trial, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 20s on Sand Track!", self.twenty_seconds_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 17s on Sand Track!", self.sixteen_seconds_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 15s on Sand Track!", self.fifteen_seconds_sand_track, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 22s on Grass Track!", self.twentytwo_seconds_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 20s on Grass Track!", self.twenty_seconds_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 18s on Grass Track!", self.eighteen_seconds_grass_track, icon = "confetti.png", ringtone = None)
        
        create_achievement("Get under 40s on Snow Track!", self.fourty_seconds_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 35s on Snow Track!", self.thirtyfive_seconds_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 30s on Snow Track!", self.thirtytwo_seconds_snow_track, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 30s on Forest Track!", self.thirty_seconds_forest_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 28s on Forest Track!", self.twentyeight_seconds_forest_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 26s on Forest Track!", self.twentysix_seconds_forest_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 25s on Forest Track!", self.twentyfive_seconds_forest_track, icon = "confetti.png", ringtone = None)

        create_achievement("Get under 20s on Savannah Track!", self.twenty_seconds_savannah_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 18s on Savannah Track!", self.eighteen_seconds_savannah_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 17s on Savannah Track!", self.seventeen_seconds_savannah_track, icon = "confetti.png", ringtone = None)
        create_achievement("Get under 16s on Savannah Track!", self.sixteen_seconds_savannah_track, icon = "confetti.png", ringtone = None)

        create_achievement("Beat Mandaw in Sand Track!", self.beat_mandaw_in_sand_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Grass Track!", self.beat_mandaw_in_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Snow Track!", self.beat_mandaw_in_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Forest Track!", self.beat_mandaw_in_forest_track, icon = "confetti.png", ringtone = None)
        create_achievement("Beat Mandaw in Savannah Track!", self.beat_mandaw_in_savannah_track, icon = "confetti.png", ringtone = None)
        
        create_achievement("Beat Mandaw in Every Track!", self.beat_mandaw_in_everything, icon = "confetti.png", ringtone = None)

        create_achievement("Unlock Grass Track!", self.unlock_grass_track, icon = "confetti.png", ringtone = None)
        create_achievement("Unlock Snow Track!", self.unlock_snow_track, icon = "confetti.png", ringtone = None)
        create_achievement("Unlock Forest Track!", self.unlock_forest_track, icon = "confetti.png", ringtone = None)
        create_achievement("Unlock Savannah Track!", self.unlock_savannah_track, icon = "confetti.png", ringtone = None)
    
    # Play the game for more than 3 seconds
    def play_the_game(self):
        return self.time_spent > 3

    def play_sand_track(self):
        return self.sand_track.played
    
    def play_grass_track(self):
        return self.grass_track.played

    def play_snow_track(self):
        return self.snow_track.played

    def play_forest_track(self):
        return self.forest_track.played
    
    def play_savannah_track(self):
        return self.savannah_track.played

    def race_against_ai(self):
        return self.car.ai_list[0].enabled

    def play_multiplayer(self):
        return self.car.multiplayer_update

    def garage(self):
        return self.main_menu.garage_menu.enabled

    def time_trial(self):
        return self.car.time_trial

    def unlock_grass_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.sand_track.enabled and self.sand_track.unlocked:
                        if self.car.last_count <= 17:
                            self.grass_track.unlocked = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 17
    
    def unlock_snow_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.grass_track.enabled and self.grass_track.unlocked:
                        if self.car.last_count <= 19:
                            # Unlock Snow Track and Green Texture
                            self.snow_track.unlocked = True
                            self.car.green_unlocked = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 19

    def unlock_forest_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.snow_track.enabled and self.snow_track.unlocked:
                        if self.car.last_count <= 33:
                            # Unlock Plains Track and White Texture
                            self.forest_track.unlocked = True
                            self.car.white_unlocked = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 33

    def unlock_savannah_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.forest_track.enabled and self.forest_track.unlocked:
                        if self.car.last_count <= 26:
                            self.savannah_track.unlocked = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 26

    def twenty_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        return self.car.last_count <= 20

    def sixteen_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 16:
                            # Unlock Orange Texture
                            self.car.orange_unlocked = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 16

    def fifteen_seconds_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 15:
                            # Unlock Viking Helmet
                            self.car.viking_helmet_unlocked = True
                            self.car.save_unlocked()
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

    def thirtytwo_seconds_snow_track(self):
        if self.snow_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 32

    def thirty_seconds_forest_track(self):
        if self.forest_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 30

    def twentyeight_seconds_forest_track(self):
        if self.forest_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 28

    def twentysix_seconds_forest_track(self):
        if self.forest_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 26

    def twentyfive_seconds_forest_track(self):
        if self.forest_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 25:
                                # Unlock Duck
                                self.car.duck_unlocked = True
                                self.car.save_unlocked()
                            return self.car.last_count <= 25

    def twenty_seconds_savannah_track(self):
        if self.savannah_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 20

    def eighteen_seconds_savannah_track(self):
        if self.savannah_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 18

    def seventeen_seconds_savannah_track(self):
        if self.savannah_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 17

    def sixteen_seconds_savannah_track(self):
        if self.savannah_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 16:
                                # Unlock Black Texture
                                self.car.black_unlocked = True
                                self.car.save_unlocked()
                            return self.car.last_count <= 16

    def beat_mandaw_in_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 14.49:
                            self.car.beat_mandaw_sand_track = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 14.49

    def beat_mandaw_in_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 17.78:
                            # Unlock Banana
                            self.car.beat_mandaw_grass_track = True
                            self.car.banana_unlocked = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 17.78
    
    def beat_mandaw_in_snow_track(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 31.45:
                            self.car.beat_mandaw_snow_track = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 31.45

    def beat_mandaw_in_forest_track(self):
        if self.forest_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 24.28:
                            self.car.beat_mandaw_forest_track = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 24.28

    def beat_mandaw_in_savannah_track(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 14.13:
                            self.car.beat_mandaw_savannah_track = True
                            self.car.save_unlocked()
                        return self.car.last_count <= 14.13

    def beat_mandaw_in_everything(self):
        if self.car.beat_mandaw_sand_track and self.car.beat_mandaw_grass_track \
            and self.car.beat_mandaw_snow_track and self.car.beat_mandaw_forest_track \
                and self.car.beat_mandaw_savannah_track:
                # Unlock Surfin Bird
                self.car.bird_unlocked = True
                self.car.save_unlocked()
        return(self.car.beat_mandaw_sand_track and self.car.beat_mandaw_grass_track and \
            self.car.beat_mandaw_snow_track and self.car.beat_mandaw_forest_track and self.car.beat_mandaw_savannah_track)