from UrsinaAchievements import create_achievement

class RallyAchievements():
    def __init__(self, car, main_menu, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track):
        self.car = car
        self.main_menu = main_menu
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forest_track = forest_track
        self.savannah_track = savannah_track
        self.lake_track = lake_track
        
        self.time_spent = 0

        sand_achievements = SandTrackAchievements(self.car, self.main_menu, self.sand_track)
        grass_achievements = GrassTrackAchievements(self.car, self.main_menu, self.grass_track)
        snow_achievements = SnowTrackAchievements(self.car, self.main_menu, self.snow_track)
        forest_achievements = ForestTrackAchievements(self.car, self.main_menu, self.forest_track)
        savannah_achievements = SavannahTrackAchievements(self.car, self.main_menu, self.savannah_track)
        lake_achievements = LakeTrackAchievements(self.car, self.main_menu, self.lake_track)
        car_achievements = CarAchievements(self.car, self.main_menu, self.sand_track, self.grass_track, self.snow_track, self.forest_track, self.savannah_track, self.lake_track)

        create_achievement("Play the game!", self.play_the_game, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race on Sand Track for the first time!", sand_achievements.play_sand_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race on Grass Track for the first time!", grass_achievements.play_grass_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race on Snow Track for the first time!", snow_achievements.play_snow_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race on Forest Track for the first time!", forest_achievements.play_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race on Savannah Track for the first time!", savannah_achievements.play_savannah_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race on Lake Track for the first time!", lake_achievements.play_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Race against AI!", self.race_against_ai, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Play Multiplayer!", self.play_multiplayer, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Go to the Garage!", self.garage, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Play Time Trial!", self.time_trial, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Drift Gamemode!", self.unlock_drift, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Get under 20s on Sand Track!", sand_achievements.twenty_seconds_sand_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 17s on Sand Track!", sand_achievements.seventeen_seconds_sand_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 15s on Sand Track!", sand_achievements.fifteen_seconds_sand_track, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Get under 22s on Grass Track!", grass_achievements.twentytwo_seconds_grass_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 20s on Grass Track!", grass_achievements.twenty_seconds_grass_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 18s on Grass Track!", grass_achievements.eighteen_seconds_grass_track, icon = "confetti.png", ringtone = "unlock.mp3")
        
        create_achievement("Get under 40s on Snow Track!", snow_achievements.fourty_seconds_snow_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 36s on Snow Track!", snow_achievements.thirtysix_seconds_snow_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 33s on Snow Track!", snow_achievements.thirtythree_seconds_snow_track, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Get under 30s on Forest Track!", forest_achievements.thirty_seconds_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 28s on Forest Track!", forest_achievements.twentyeight_seconds_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 26s on Forest Track!", forest_achievements.twentysix_seconds_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 25s on Forest Track!", forest_achievements.twentyfive_seconds_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Get under 20s on Savannah Track!", savannah_achievements.twenty_seconds_savannah_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 18s on Savannah Track!", savannah_achievements.eighteen_seconds_savannah_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 16s on Savannah Track!", savannah_achievements.sixteen_seconds_savannah_track, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Get under 60s on Lake Track!", lake_achievements.sixty_seconds_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 55s on Lake Track!", lake_achievements.fiftyfive_seconds_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 50s on Lake Track!", lake_achievements.fifty_seconds_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Get under 47s on Lake Track!", lake_achievements.fourtyseven_seconds_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Muscle Car!", car_achievements.unlock_muscle_car, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Limo!", car_achievements.unlock_limo, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Lorry!", car_achievements.unlock_lorry, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Hatchback!", car_achievements.unlock_hatchback, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Rally Car!", car_achievements.unlock_rally, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Sports Car Green!", car_achievements.sports_green, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Sports Car Orange!", car_achievements.sports_orange, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Sports Car White!", car_achievements.sports_white, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Sports Car Black!", car_achievements.sports_black, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Muscle Car Red!", car_achievements.muscle_red, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Muscle Car Blue!", car_achievements.muscle_blue, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Muscle Car Green!", car_achievements.muscle_green, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Muscle Car White!", car_achievements.muscle_white, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Muscle Car Black!", car_achievements.muscle_black, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Limo Red!", car_achievements.limo_red, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Limo Blue!", car_achievements.limo_blue, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Limo Green!", car_achievements.limo_green, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Limo White!", car_achievements.limo_white, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Limo Orange!", car_achievements.limo_orange, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Lorry Red!", car_achievements.lorry_red, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Lorry Blue!", car_achievements.lorry_blue, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Lorry Green!", car_achievements.lorry_green, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Lorry Orange!", car_achievements.lorry_orange, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Lorry Black!", car_achievements.lorry_black, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Hatchback Red!", car_achievements.hatchback_red, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Hatchback Blue!", car_achievements.hatchback_blue, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Hatchback White!", car_achievements.hatchback_white, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Hatchback Orange!", car_achievements.hatchback_orange, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Hatchback Black!", car_achievements.hatchback_black, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Rally Car White!", car_achievements.rally_white, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Rally Car Blue!", car_achievements.rally_blue, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Rally Car Green!", car_achievements.rally_green, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Rally Car Orange!", car_achievements.rally_orange, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Rally Car Black!", car_achievements.rally_black, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Beat Mandaw in Sand Track!", self.beat_mandaw_in_sand_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Beat Mandaw in Grass Track!", self.beat_mandaw_in_grass_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Beat Mandaw in Snow Track!", self.beat_mandaw_in_snow_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Beat Mandaw in Forest Track!", self.beat_mandaw_in_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Beat Mandaw in Savannah Track!", self.beat_mandaw_in_savannah_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Beat Mandaw in Lake Track!", self.beat_mandaw_in_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")
        
        create_achievement("Beat Mandaw in Every Track!", self.beat_mandaw_in_everything, icon = "confetti.png", ringtone = "unlock.mp3")

        create_achievement("Unlock Grass Track!", self.unlock_grass_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Snow Track!", self.unlock_snow_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Forest Track!", self.unlock_forest_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Savannah Track!", self.unlock_savannah_track, icon = "confetti.png", ringtone = "unlock.mp3")
        create_achievement("Unlock Lake Track!", self.unlock_lake_track, icon = "confetti.png", ringtone = "unlock.mp3")
    
    # Play the game for more than 3 seconds
    def play_the_game(self):
        return self.time_spent > 3

    def race_against_ai(self):
        return self.car.ai_list[0].enabled

    def play_multiplayer(self):
        return self.car.multiplayer_update

    def garage(self):
        return self.main_menu.garage_menu.enabled

    def time_trial(self):
        return self.car.gamemode == "time trial"

    def unlock_drift(self):
        if self.sand_track.unlocked and self.grass_track.unlocked and \
            self.snow_track.unlocked and self.forest_track.unlocked and \
                self.savannah_track.unlocked and self.lake_track.unlocked:
                self.car.drift_unlocked = True
                self.car.save_unlocked()
                return True

    def unlock_grass_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.sand_track.enabled and self.sand_track.unlocked:
                        if self.car.last_count <= 22:
                            # Unlock Grass Track
                            self.grass_track.unlocked = True
                            self.car.save_unlocked()
                            return True
    
    def unlock_snow_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.grass_track.enabled and self.grass_track.unlocked:
                        if self.car.last_count <= 23:
                            # Unlock Snow Track
                            self.snow_track.unlocked = True
                            self.car.save_unlocked()
                            return True

    def unlock_forest_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.snow_track.enabled and self.snow_track.unlocked:
                        if self.car.last_count <= 40:
                            # Unlock Forest Track
                            self.forest_track.unlocked = True
                            self.car.save_unlocked()
                            return True

    def unlock_savannah_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.forest_track.enabled and self.forest_track.unlocked:
                        if self.car.last_count <= 32:
                            # Unlock Savannah Track
                            self.savannah_track.unlocked = True
                            self.car.save_unlocked()
                            return True

    def unlock_lake_track(self):
        for menu in self.main_menu.menus:
            if menu.enabled == False:
                if self.car.enabled and self.car.last_count != 0:
                    if self.savannah_track.enabled and self.savannah_track.unlocked:
                        if self.car.last_count <= 20:
                            # Unlock Lake Track
                            self.lake_track.unlocked = True
                            self.car.save_unlocked()
                            return True

    def beat_mandaw_in_sand_track(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 13.09:
                            self.car.beat_mandaw_sand_track = True
                            self.car.save_unlocked()
                            return True

    def beat_mandaw_in_grass_track(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 15.55:
                            # Unlock Banana
                            self.car.beat_mandaw_grass_track = True
                            self.car.banana_unlocked = True
                            self.car.save_unlocked()
                            return True
    
    def beat_mandaw_in_snow_track(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 27.41:
                            self.car.beat_mandaw_snow_track = True
                            self.car.save_unlocked()
                            return True

    def beat_mandaw_in_forest_track(self):
        if self.forest_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 21.73:
                            self.car.beat_mandaw_forest_track = True
                            self.car.save_unlocked()
                            return True

    def beat_mandaw_in_savannah_track(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 12.31:
                            self.car.beat_mandaw_savannah_track = True
                            self.car.save_unlocked()
                            return True

    def beat_mandaw_in_lake_track(self):
        if self.lake_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.last_count != 0:
                        if self.car.last_count <= 39.45:
                            self.car.beat_mandaw_lake_track = True
                            self.car.save_unlocked()
                            return True

    def beat_mandaw_in_everything(self):
        if self.car.beat_mandaw_sand_track and self.car.beat_mandaw_grass_track \
            and self.car.beat_mandaw_snow_track and self.car.beat_mandaw_forest_track \
                and self.car.beat_mandaw_savannah_track and self.car.beat_mandaw_lake_track:
                # Unlock Surfin Bird
                self.car.surfinbird_unlocked = True
                self.car.save_unlocked()
                return True

"""
Sand Track Achievements
"""
class SandTrackAchievements():
    def __init__(self, car, main_menu, sand_track):
        self.car = car
        self.main_menu = main_menu
        self.sand_track = sand_track

    def play_sand_track(self):
        return self.sand_track.played

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

"""
Grass Track Achievements
"""
class GrassTrackAchievements():
    def __init__(self, car, main_menu, grass_track):
        self.car = car
        self.main_menu = main_menu
        self.grass_track = grass_track

    def play_grass_track(self):
        return self.grass_track.played

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

"""
Snow Track Achievements
"""
class SnowTrackAchievements():
    def __init__(self, car, main_menu, snow_track):
        self.car = car
        self.main_menu = main_menu
        self.snow_track = snow_track

    def play_snow_track(self):
        return self.snow_track.played

    def fourty_seconds_snow_track(self):
        if self.snow_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 40

    def thirtysix_seconds_snow_track(self):
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
                            return self.car.last_count <= 32

"""
Forest Track Achievements
"""
class ForestTrackAchievements():
    def __init__(self, car, main_menu, forest_track):
        self.car = car
        self.main_menu = main_menu
        self.forest_track = forest_track

    def play_forest_track(self):
        return self.forest_track.played

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

"""
Savannah Track Achievements
"""
class SavannahTrackAchievements():
    def __init__(self, car, main_menu, savannah_track):
        self.car = car
        self.main_menu = main_menu
        self.savannah_track = savannah_track

    def play_savannah_track(self):
        return self.savannah_track.played

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

    def sixteen_seconds_savannah_track(self):
        if self.savannah_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 17

"""
Lake Track Achievements
"""
class LakeTrackAchievements():
    def __init__(self, car, main_menu, lake_track):
        self.car = car
        self.main_menu = main_menu
        self.lake_track = lake_track

    def play_lake_track(self):
        return self.lake_track.played
    
    def sixty_seconds_lake_track(self):
        if self.lake_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 60

    def fiftyfive_seconds_lake_track(self):
        if self.lake_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 55

    def fifty_seconds_lake_track(self):
        if self.lake_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 50

    def fourtyseven_seconds_lake_track(self):
        if self.lake_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if menu.enabled == False:
                        if self.car.last_count != 0:
                            return self.car.last_count <= 47

"""
Car Achievements
"""
class CarAchievements():
    def __init__(self, car, main_menu, sand_track, grass_track, snow_track, forest_track, savannah_track, lake_track):
        self.car = car
        self.main_menu = main_menu
        self.sand_track = sand_track
        self.grass_track = grass_track
        self.snow_track = snow_track
        self.forest_track = forest_track
        self.savannah_track = savannah_track
        self.lake_track = lake_track

    def unlock_muscle_car(self):
        if self.savannah_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if not menu.enabled:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 18:
                                self.car.muscle_unlocked = True
                                self.car.save_unlocked()
                                return True

    def unlock_limo(self):
        if self.grass_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if not menu.enabled:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 20:
                                self.car.limo_unlocked = True
                                self.car.save_unlocked()
                                return True

    def unlock_lorry(self):
        if self.forest_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if not menu.enabled:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 28:
                                self.car.lorry_unlocked = True
                                self.car.save_unlocked()
                                return True

    def unlock_hatchback(self):
        if self.sand_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if not menu.enabled:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 20:
                                self.car.hatchback_unlocked = True
                                self.car.save_unlocked()
                                return True

    def unlock_rally(self):
        if self.lake_track.enabled:
            if self.car.enabled:
                for menu in self.main_menu.menus:
                    if not menu.enabled:
                        if self.car.last_count != 0:
                            if self.car.last_count <= 60:
                                self.car.rally_unlocked = True
                                self.car.save_unlocked()
                                return True

    """
    Sports Car Textures
    """
    def sports_green(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "sports":
                        if self.car.last_count <= 22 and self.car.last_count != 0:
                            # Unlock Sports Car Green Colour
                            self.car.sports_green_unlocked = True
                            self.car.save_unlocked()
                            return True

    def sports_orange(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "sports":
                        if self.car.last_count <= 18 and self.car.last_count != 0:
                            # Unlock Sports Car Orange Colour
                            self.car.sports_orange_unlocked = True
                            self.car.save_unlocked()
                            return True

    def sports_white(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "sports":
                        if self.car.last_count <= 37 and self.car.last_count != 0:
                            # Unlock Sports Car White Colour
                            self.car.sports_white_unlocked = True
                            self.car.save_unlocked()
                            return True

    def sports_black(self):
        if self.forest_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "sports":
                        if self.car.last_count <= 29 and self.car.last_count != 0:
                            # Unlock Sports Car Black Colour
                            self.car.sports_black_unlocked = True
                            self.car.save_unlocked()
                            return True

    """
    Muscle Car Textures
    """
    def muscle_red(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "muscle":
                        if self.car.last_count <= 17 and self.car.last_count != 0:
                            # Unlock Muscle Car Red Colour
                            self.car.muscle_red_unlocked = True
                            self.car.save_unlocked()
                            return True

    def muscle_blue(self):
        if self.lake_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "muscle":
                        if self.car.last_count <= 52 and self.car.last_count != 0:
                            # Unlock Muscle Car Blue Colour
                            self.car.muscle_blue_unlocked = True
                            self.car.save_unlocked()
                            return True

    def muscle_green(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "muscle":
                        if self.car.last_count <= 20 and self.car.last_count != 0:
                            # Unlock Muscle Car Green Colour
                            self.car.muscle_green_unlocked = True
                            self.car.save_unlocked()
                            return True

    def muscle_white(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "muscle":
                        if self.car.last_count <= 38 and self.car.last_count != 0:
                            # Unlock Muscle Car White Colour
                            self.car.muscle_white_unlocked = True
                            self.car.save_unlocked()
                            return True

    def muscle_black(self):
        if self.forest_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "muscle":
                        if self.car.last_count <= 28 and self.car.last_count != 0:
                            # Unlock Muscle Car Black Colour
                            self.car.muscle_black_unlocked = True
                            self.car.save_unlocked()
                            return True

    """
    Limo Textures
    """
    def limo_red(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "limo":
                        if self.car.last_count <= 19 and self.car.last_count != 0:
                            # Unlock Limo Red Colour
                            self.car.limo_red_unlocked = True
                            self.car.save_unlocked()
                            return True

    def limo_blue(self):
        if self.lake_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "limo":
                        if self.car.last_count <= 60 and self.car.last_count != 0:
                            # Unlock Limo Blue Colour
                            self.car.limo_blue_unlocked = True
                            self.car.save_unlocked()
                            return True

    def limo_green(self):
        if self.forest_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "limo":
                        if self.car.last_count <= 28 and self.car.last_count != 0:
                            # Unlock Limo Green Colour
                            self.car.limo_green_unlocked = True
                            self.car.save_unlocked()
                            return True

    def limo_white(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "limo":
                        if self.car.last_count <= 38 and self.car.last_count != 0:
                            # Unlock Limo White Colour
                            self.car.limo_white_unlocked = True
                            self.car.save_unlocked()
                            return True

    def limo_orange(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "limo":
                        if self.car.last_count <= 18 and self.car.last_count != 0:
                            # Unlock Limo Orange Colour
                            self.car.limo_orange_unlocked = True
                            self.car.save_unlocked()
                            return True

    """
    Lorry Textures
    """
    def lorry_red(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "lorry":
                        if self.car.last_count <= 20 and self.car.last_count != 0:
                            # Unlock Lorry Red Colour
                            self.car.lorry_red_unlocked = True
                            self.car.save_unlocked()
                            return True

    def lorry_blue(self):
        if self.lake_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "lorry":
                        if self.car.last_count <= 70 and self.car.last_count != 0:
                            # Unlock Lorry Blue Colour
                            self.car.lorry_blue_unlocked = True
                            self.car.save_unlocked()
                            return True

    def lorry_green(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "lorry":
                        if self.car.last_count <= 21 and self.car.last_count != 0:
                            # Unlock Lorry Green Colour
                            self.car.lorry_green_unlocked = True
                            self.car.save_unlocked()
                            return True

    def lorry_black(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "lorry":
                        if self.car.last_count <= 38 and self.car.last_count != 0:
                            # Unlock Lorry Black Colour
                            self.car.lorry_black_unlocked = True
                            self.car.save_unlocked()
                            return True

    def lorry_orange(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "lorry":
                        if self.car.last_count <= 19 and self.car.last_count != 0:
                            # Unlock Lorry Orange Colour
                            self.car.lorry_orange_unlocked = True
                            self.car.save_unlocked()
                            return True

    """
    Hatchback Textures
    """
    def hatchback_red(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "hatchback":
                        if self.car.last_count <= 18 and self.car.last_count != 0:
                            # Unlock Hatchback Red Colour
                            self.car.hatchback_red_unlocked = True
                            self.car.save_unlocked()
                            return True

    def hatchback_blue(self):
        if self.lake_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "hatchback":
                        if self.car.last_count <= 65 and self.car.last_count != 0:
                            # Unlock Hatchback Blue Colour
                            self.car.hatchback_blue_unlocked = True
                            self.car.save_unlocked()
                            return True

    def hatchback_white(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "hatchback":
                        if self.car.last_count <= 20 and self.car.last_count != 0:
                            # Unlock Hatchback White Colour
                            self.car.hatchback_white_unlocked = True
                            self.car.save_unlocked()
                            return True

    def hatchback_black(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "hatchback":
                        if self.car.last_count <= 37 and self.car.last_count != 0:
                            # Unlock Hatchback Black Colour
                            self.car.hatchback_black_unlocked = True
                            self.car.save_unlocked()
                            return True

    def hatchback_orange(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "hatchback":
                        if self.car.last_count <= 18 and self.car.last_count != 0:
                            # Unlock Hatchback Orange Colour
                            self.car.hatchback_orange_unlocked = True
                            self.car.save_unlocked()
                            return True

    """
    Rally Car Textures
    """
    def rally_white(self):
        if self.sand_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "rally":
                        if self.car.last_count <= 17 and self.car.last_count != 0:
                            # Unlock Rally Car White Colour
                            self.car.rally_white_unlocked = True
                            self.car.save_unlocked()
                            return True

    def rally_blue(self):
        if self.lake_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "rally":
                        if self.car.last_count <= 52 and self.car.last_count != 0:
                            # Unlock Rally Car Blue Colour
                            self.car.rally_blue_unlocked = True
                            self.car.save_unlocked()
                            return True

    def rally_green(self):
        if self.grass_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "rally":
                        if self.car.last_count <= 19 and self.car.last_count != 0:
                            # Unlock Rally Car Green Colour
                            self.car.rally_green_unlocked = True
                            self.car.save_unlocked()
                            return True

    def rally_black(self):
        if self.snow_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "rally":
                        if self.car.last_count <= 35 and self.car.last_count != 0:
                            # Unlock Rally Car Black Colour
                            self.car.rally_black_unlocked = True
                            self.car.save_unlocked()
                            return True

    def rally_orange(self):
        if self.savannah_track.enabled:
            for menu in self.main_menu.menus:
                if menu.enabled == False:
                    if self.car.car_type == "rally":
                        if self.car.last_count <= 16 and self.car.last_count != 0:
                            # Unlock Rally Car Orange Colour
                            self.car.rally_orange_unlocked = True
                            self.car.save_unlocked()
                            return True