# wip

"""
TowerScheduleExcelConfigData.json

input => scheduleId

"descTextMapHash": 745916560,
"buffnameTextMapHash": 4221605071,
"icon": "UI_TowerBlessing_57"

"schedules": [
    {
        "floorList": [ floorId, floorId, floorId... => 9, 10, 11, 12


TowerFloorExcelConfigData.json

input => floorId

"floorIndex": 12,
"levelGroupId": 53,
"overrideMonsterLevel": 95,


TowerLevelExcelConfigData.json

input => levelGroupId

floorIndex - levelIndex
12-1 
    "dungeonId": 3206, => don't need?
    "conds": 180 300 420
    "monsterLevel": 97, -> + 1
    "firstMonsterList": [
        54102,
        40401,
        40402,
        40403
    ],
    "secondMonsterList": [
        20601
    ]

12-2
12-3


MonsterExcelConfigData.json


"""