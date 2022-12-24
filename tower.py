from kaitaistruct import KaitaiStream
import xlsxwriter
from io import BytesIO
import glob, os, sys, json, re
import subprocess
from multiprocessing import Process
import character

sys.path.append("./py")
from textmap import Textmap

def DumpTowerSchedule():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/TowerScheduleExcelConfigData.bin', './ksy/tower_schedule.ksy']

    with open('./json/Dump_TowerScheduleExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def DumpTowerFloor():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/TowerFloorExcelConfigData.bin', './ksy/tower_floor.ksy']

    with open('./json/Dump_TowerFloorExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def DumpTowerLevel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/TowerLevelExcelConfigData.bin', './ksy/tower_level.ksy']

    with open('./json/Dump_TowerLevelExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def DumpDungeonLevel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/DungeonLevelEntityConfigData.bin', './ksy/dungeon_level.ksy']

    with open('./json/Dump_DungeonLevelEntityConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

""" This is not needed 😢
def DumpMonsterExcel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/MonsterExcelConfigData.bin', './ksy/monster_excel.ksy']

    with open('./json/Dump_MonsterExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)
"""
def DumpMonsterDescribe():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/MonsterDescribeExcelConfigData.bin', './ksy/monster_describe.ksy']

    with open('./json/Dump_MonsterDescribeExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)


def ParseTower():
    towerSchedule, towerFloor, towerLevel, dungeonLevel, monsterDescribe = dict(), dict(), dict(), dict(), dict()
    output = dict()

    textMapLanguage = input("Type the textMap Language (Example: KR) : ")
    with open(f'./json/TextMap_{textMapLanguage}.json') as textmap_json:
        textmap = json.load(textmap_json)

    with open('./json/Dump_TowerScheduleExcelConfigData.json', 'r') as dump:
        towerSchedule = json.load(dump)
    with open('./json/Dump_TowerFloorExcelConfigData.json', 'r') as dump:
        towerFloor = json.load(dump)
    with open('./json/Dump_TowerLevelExcelConfigData.json', 'r') as dump:
        towerLevel = json.load(dump)
    with open('./json/Dump_DungeonLevelEntityConfigData.json', 'r') as dump:
        dungeonLevel = json.load(dump)
    with open('./json/Dump_MonsterDescribeExcelConfigData.json', 'r') as dump:
        monsterDescribe = json.load(dump)
    
    print("Last 5 abyss schedule_id:", ", ".join([str(i["schedule_id"]["value"]) for i in towerSchedule["block"][-5:]]))
    scheduleId = int(input("Type abyss schedule_id: "))
    print("")
    print("===")

    for i in towerSchedule["block"]:
        if i["schedule_id"]["value"] == scheduleId:
            print("floorList: " + str([i["value"] for i in i["schedules"]["data"][0]["floor_list"]["data"]]))
            output["floorList"] = [i["value"] for i in i["schedules"]["data"][0]["floor_list"]["data"]]

            print("openTime: " + i["schedules"]["data"][0]["open_time"]["data"])
            print("closeTime: " + i["close_time"]["data"])

            print("buffname: " + textmap[str(i["buffname"]["value"])])

            for j in dungeonLevel["block"]:
                if j["id"]["value"] == i["monthly_level_config_id"]["value"]:
                    print("Monthly Buff: " + ConvertText(textmap[str(j["desc"]["value"])]))

            print("icon: " + i["icon"]["data"])
    
    print("===")
    print("")

    for i in towerFloor["block"]:
        if i["floor_id"]["value"] in output["floorList"]:
            print("===")
            print("Floor id: " + str(i["floor_id"]["value"]))
            print("Floor index: " + str(i["floor_index"]["value"]))
            print("levelGroupId: " + str(i["level_group_id"]["value"]))

            for j in dungeonLevel["block"]:
                if j["id"]["value"] == i["floor_level_config_id"]["value"]:
                    print("Floor Buff: " + textmap[str(j["desc"]["value"])])

            for j in towerLevel["block"]:
                if j["level_group_id"]["value"] == i["level_group_id"]["value"]:
                    print("")
                    print("Level index: " + str(j["level_index"]["value"]))
                    print("Monster Level: " + str(j["monster_level"]["value"]+1))

                    print("Conds 1st: " + "/".join([str(conds["argument_list_upper"]["data"][1]["value"]) for conds in j["conds"]["data"]]))
                    print("Conds 2nd: " + "/".join([str(conds["argument_list"]["data"][1]["value"]) for conds in j["conds"]["data"]]))
                    
                    print("First monster list: " + ", ".join([textmap[str(ConvertDescribeId(monster["value"], monsterDescribe))] for monster in j["first_monster_list"]["data"]]))
                    print("Second monster list: " + ", ".join([textmap[str(ConvertDescribeId(monster["value"], monsterDescribe))] for monster in j["second_monster_list"]["data"]]))
                    

            print("===\n")
    
def ConvertDescribeId(value, monsterDescribe):
    for i in monsterDescribe["block"]:
        if i["id"]["value"] == value:
            return i["name"]["value"]

def ConvertText(desc):
    pattern = "<color.*?>(.+?)</color>"
    desc_parsed = re.split(pattern, desc)
    
    return "".join(desc_parsed)


ParseTower()
