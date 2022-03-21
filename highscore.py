import json

def set_highscore(sect:str, value):
    with open("highscore.json", "r+") as gd:
        gdj = json.load(gd)
        gdj[str(sect)] = value
        gd.seek(0)
        json.dump(gdj, gd, indent = 4)
        gd.truncate()

def load_highscore(sect:str):
    with open("highscore.json", "r") as gd:
        gdj = json.load(gd)
        return gdj[sect]