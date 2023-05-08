from time import sleep
import requests
import json
import zones
from operator import add, itemgetter

SAMPLE = "src/ffsrc/sample.json"
DB = "src/ffsrc/db.json"


def calculateScore(x, y):
    x += 1
    y = y / 100

    return (1 / x) * (1 - y)


def getData(obj, k):
    response = requests.post("https://api.worldofdefish.com/zones/select", json=obj)
    response = response.json()
    with open(SAMPLE, "a") as writeMembers:
        json.dump(response, writeMembers, indent=2)
        if k == 5:
            writeMembers.write("\n")
        else:
            writeMembers.write(",\n")


def sortData():
    with open(SAMPLE, "r") as readData:
        readData = json.load(readData)
        y = 0
        for item in readData:
            objZones = []
            sortedList = []
            zones = item["items"]
            for zone in zones:
                zoneNum = zone["_id"]
                fee = zone["fee"]
                wodRate = zone["wod_rate"] * 3600
                agents = zone["fishing_pool"]["agents_amount"]
                obj = {
                    "score": calculateScore(agents, fee),
                    "zone": zoneNum,
                    "fee": fee,
                    "players": agents,
                    "wod": wodRate,
                }
                objZones.append(obj)
            sortedList = sorted(objZones, key=itemgetter("score"), reverse=True)
            with open(DB, "a") as addToDB:
                k = 0
                addToDB.write("[\n")
                for item in sortedList:
                    json.dump(item, addToDB, indent=2)
                    if k == len(sortedList) - 1:
                        addToDB.write("\n")
                    else:
                        addToDB.write(",\n")
                    k += 1
                if y == 5:
                    addToDB.write("]\n")
                else:
                    addToDB.write("],\n")
            y += 1


def Main():
    k = 0
    for Zone in zones.zone:
        myObj = {
            "take": len(Zone),
            "sort": {"sort_by": "tier", "sort_dir": "DESC"},
            "filters": {
                "fee": {"min": 0, "max": 80},
                # "tier": [1, 2, 3, 4, 5, 6],
                "id": Zone,
            },
        }
        getData(obj=myObj, k=k)
        k += 1


if __name__ == "__main__":
    x = 1
    while True:
        try:
            print("Searching...")
            open(SAMPLE, "w").close()
            open(DB, "w").close()

            with open(SAMPLE, "a") as writeJson:
                writeJson.write("[\n")
            Main()
            with open(SAMPLE, "a") as writeJson:
                writeJson.write("]")
            with open(DB, "a") as writeJson:
                writeJson.write("[\n")
            sortData()
            with open(DB, "a") as writeJson:
                writeJson.write("]")
            print(f"Search Done: {x}")
            sleep(60)
            x += 1
        except:
            pass
