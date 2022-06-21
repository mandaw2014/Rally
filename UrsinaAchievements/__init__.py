"""
Author: TheAssasin71 or megat69
Repo: https://github.com/megat69/UrsinaAchievements
Init file for UrsinaAchievements, a system allowing users in Ursina engine to receive achievements.
"""
from ursina import *
import json
import os
from direct.stdpy import thread

_path = os.path.dirname(os.path.abspath(__file__))

_achievements_list = []
try:
	with open(f"{_path}/achievements.json", "r", encoding="utf-8") as save_file:
		_achievements_got = json.load(save_file)["achievements_got_names"].copy()
except FileNotFoundError:
	with open(f"{_path}/achievements.json", "w", encoding="utf-8") as save_file:
		_achievements_got = []
		json.dump({"achievements_got_names": []}, save_file, indent=4)


def create_achievement(name:str, unlock_condition, icon:str=None, ringtone:str="clicking", importance:int=1):
	"""
	Creates a new achievement for the game.
	:param name: The name of the achievement.
	:param unlock_condition: A callback function representing whether the achievement should be unlocked.
		Unlocks the achievement if the return value is True, passes if it is either False or None.
	:param icon: The path to the image file being represented with the text, optional.
	:param ringtone: The name of the ringtone to be used to signal the achievement get ; can be "clicking",
		"subtle", "uplifting", or the path to a wav/ogg file. It can also be None, and thus won't produce a sound.
	:param importance: The higher the number is, the longer the achievement will stay on screen. Default is 1.
	"""
	_achievements_list.append(
		(name, unlock_condition, icon, ringtone, importance)
	)


def _save_achievements():
	with open(f"{_path}/achievements.json", "w", encoding="utf-8") as save_file:
		json.dump({"achievements_got_names": _achievements_got.copy()}, save_file, indent=2)


class Achievement(Entity):
	"""
	Main achievement class, the popup.
	"""
	# The different ringtones
	ringtones = {
		"clicking": Audio(f"{_path}/ringtones/clicking.ogg", autoplay=False),
		"subtle": Audio(f"{_path}/ringtones/subtle.ogg", autoplay=False),
		"uplifting": Audio(f"{_path}/ringtones/uplifting.ogg", autoplay=False)
	}
	achievement_color = (64, 64, 64)
	text_color = (255, 255, 255)
	icon_color = (255, 255, 255)

	def __init__(self, title:str, unlock_condition, icon:str=None, ringtone:str="clicking", importance:int=1):
		"""
		:param title: The name of the achievement.
		:param unlock_condition: A callback function representing whether the achievement should be unlocked.
			Unlocks the achievement if the return value is True, passes if it is either False or None.
		:param icon: The path to the image file being represented with the text, optional.
		:param ringtone: The name of the ringtone to be used to signal the achievement get ; can be "clicking",
			"subtle", "uplifting", or the path to a wav/ogg file. It can also be None, and thus won't produce a sound.
		:param importance: The higher the number is, the longer the achievement will stay on screen. Default is 1.
		"""
		super().__init__(
			parent=camera.ui,
			model="quad",
			position=((.5*window.aspect_ratio, -.5)),
			origin=(.5, -.5),
			scale=(.25, .15),
			color=color.rgba(*Achievement.achievement_color, 185),
			always_on_top=True
		)
		# Adding the title
		self.title = Text(
			parent=self,
			text=title,
			position=(-.95, .9),
			scale=(4, 5.5),
			wordwrap=15,
			color=color.rgba(*Achievement.text_color, 255)
		)
		# Adding the icon if wanted
		if icon is not None:
			self.icon = Entity(
				parent=self,
				model="quad",
				texture=icon,
				scale=(.4, .5),
				position=(-.5, .3),
			color=color.rgba(*Achievement.icon_color, 255)
			)

		# Plays a ringtone if wanted
		if ringtone is not None:
			# Plays the ringtone if the name is in the class dictionnary
			if ringtone in Achievement.ringtones.keys():
				Achievement.ringtones[ringtone].play()
			# Or locates and plays the audio file if wanted
			else:
				Audio(ringtone)

		# Creating the animation for the entering
		old_position = self.position
		self.position = self.position + Vec2(0, -.2)
		self.animate_position(old_position, duration=.4 * importance, curve=curve.out_back)
		self.animate_color(color.rgba(*Achievement.achievement_color, 0), duration=1.5 * importance, delay=2 * importance)
		self.title.animate_color(color.rgba(*Achievement.text_color, 0), duration=1.5 * importance, delay=2 * importance)
		if icon is not None:
			self.icon.animate_color(color.rgba(*Achievement.icon_color, 0), duration=1.5 * importance, delay=2 * importance)

		invoke(destroy, self, delay=5 * importance)


def _achievements_update():
	"""
	Checks if the achievement condition is met at each update.
	"""
	pop = []
	for i, achievement in enumerate(_achievements_list):
		if achievement[1]() is True and achievement[0] not in _achievements_got:
			print(f"Achievement got ! {achievement[0]}")
			# Shows the achievement pop-up
			Achievement(*achievement)
			# Adds the achievement name to the list of achievements got
			_achievements_got.append(achievement[0])
			# Removes the achievement from the list of achievements to check
			pop.append(i)
			# Saves the achievements got list (in a new thread)
			try:
				thread.start_new_thread(function=_save_achievements, args='')
			except Exception as e:
				print('error saving the achievements', e)

	for i in range(len(pop)):
		_achievements_list.pop(pop[i] - i)

Entity(update=_achievements_update)

if __name__ == "__main__":
	app = Ursina()
	Sky()
	do = False
	def cond():
		global do
		return do
	create_achievement("Bubbles.", cond, "bubbles.png", "subtle")
	def setdo():
		global do
		do = True
	invoke(setdo, delay=2)

	app.run()