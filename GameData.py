import json

def WriteGameData(Sect:str, Value):
    with open("GameData.json", "r+") as gd:
        gdj = json.load(gd)
        gdj[str(Sect)] = Value
        gd.seek(0)
        json.dump(gdj, gd, indent=4)
        gd.truncate()

def LoadGameData(Sect:str):
    with open("GameData.json", "r") as gd:
        gdj = json.load(gd)
        return gdj[Sect]