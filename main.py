from kaitaistruct import KaitaiStream
from io import BytesIO
import glob, os, sys, json
import subprocess

sys.path.append("./py")
from textmap import Textmap

# Change CharacterID
ParseCharacterID = 10000030

# Change TextMapLanguage
TextMapLanguage = "KR"
'''
    01/26692920 => 
    02/27251172 => 
    03/25181351 => 
    04/25776943 => EN
    05/20618174 => 
    06/25555476 => 
    07/30460104 => 
    08/32244380 => 
    09/22299426 => KR
    10/23331191 => 
    11/21030516 => 
    12/32056053 => 
    13/34382464 => 
'''

def GetAllTextmaps():
    global TextMapLanguage
    output = dict()

    total = len(glob.glob('./bin/TextMap_' + TextMapLanguage + '/*.bin'))
    cnt = 0

    for file in glob.glob('./bin/TextMap_' + TextMapLanguage + '/*.bin'):

        cnt += 1
        print("Parsing in progress [" + str(cnt) + "/" + str(total) + "]")

        with open(file, 'rb') as f:
            stream = KaitaiStream(BytesIO(f.read()))
            obj = Textmap(stream)

            for block in obj.textmap:
                output[str(block.hash.value)] = block.string.data

    with open("./json/TextMap_" + TextMapLanguage + ".json", "w", encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)

def DumpAvatarExcel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarExcelConfigData.bin', './ksy/avatar_excel.ksy']

    with open('./json/Dump_AvatarExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def ParseAvatarExcel():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            if block["has_field_use_type"]:
                output_block["useType"] = block["use_type"]["value"][16:].upper()
            
            output_block["bodyType"] = block["body_type"]["value"][10:].upper()
            output_block["iconName"] = block["icon_name"]["data"]
            output_block["sideIconName"] = block["side_icon_name"]["data"]
            output_block["qualityType"] = block["quality_type"]["value"][13:].upper()
            output_block["chargeEfficiency"] = block["charge_efficiency"]

            if block["has_field_is_range_attack"]:
                output_block["isRangeAttack"] = block["is_range_attack"]

            output_block["initialWeapon"] = block["initial_weapon"]["value"]
            output_block["weaponType"] = block["weapon_type"]["value"][12:].upper()
            output_block["imageName"] = block["image_name"]["data"]
            output_block["cutsceneShow"] = block["cutscene_show"]["data"]
            output_block["skillDepotId"] = block["skill_depot_id"]["value"]
            output_block["staminaRecoverSpeed"] = block["stamina_recover_speed"]
            output_block["candSkillDepotIds"] = [i["value"] for i in block["cand_skill_depot_ids"]["data"]]
            output_block["manekinMotionConfig"] = block["manekin_motion_config"]["value"]
            output_block["descTextMapHash"] = block["desc"]["value"]

            if block["has_field_avatar_identity_type"]:
                output_block["avatarIdentityType"] = block["avatar_identity_type"]["value"][21:].upper()
            
            output_block["avatarPromoteId"] = block["avatar_promote_id"]["value"]
            output_block["avatarPromoteRewardLevelList"] = [i["value"] for i in block["avatar_promote_reward_level_list"]["data"]]
            output_block["avatarPromoteRewardIdList"] = [i["value"] for i in block["avatar_promote_reward_id_list"]["data"]]
            output_block["featureTagGroupID"] = block["feature_tag_group_id"]["value"]
            output_block["infoDescTextMapHash"] = block["info_desc"]["value"]
            output_block["hpBase"] = block["hp_base"]
            output_block["attackBase"] = block["attack_base"]
            output_block["defenseBase"] = block["defense_base"]
            output_block["critical"] = block["critical"]
            output_block["criticalHurt"] = block["critical_hurt"]

            prop_grow_curves = []
            for i in block["prop_grow_curves"]["data"]:
                prop_grow = dict()
                prop_grow["type"] = i["type"]["value"][16:].upper()
                prop_grow["growCurve"] = i["grow_curve"]["value"][16:].upper()
                prop_grow_curves.append(prop_grow)
            output_block["propGrowCurves"] = prop_grow_curves

            output_block["id"] = block["id"]["value"]
            output_block["nameTextMapHash"] = block["name"]["value"]
            output_block["LODPatternName"] = block["lod_pattern_name"]["data"]

            output.append(output_block)

    with open('./json/AvatarExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)

def DumpAvatarSkillDepot():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarSkillDepotExcelConfigData.bin', './ksy/avatar_skill_depot.ksy']

    with open('./json/Dump_AvatarSkillDepotExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def ParseAvatarSkillDepot():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarSkillDepotExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()
            output_block["id"] = block["id"]["value"]

            if block["has_field_energy_skill"]:
                output_block["energySkill"] = block["energy_skill"]["value"]

            output_block["skills"] = [i["value"] for i in block["skills"]["data"]]
            output_block["subSkills"] = [i["value"] for i in block["sub_skills"]["data"]]
            
            if block["has_field_attack_mode_skill"]:
                output_block["attackModeSkill"] = block["attack_mode_skill"]["value"]
            
            output_block["extraAbilities"] = [i["data"] for i in block["extra_abilities"]["data"]]
            output_block["talents"] = [i["value"] for i in block["talents"]["data"]]
            output_block["talentStarName"] = block["talent_star_name"]["data"]

            inherent_proud_skill_opens = []
            for i in block["inherent_proud_skill_opens"]["data"]:
                prop_proud = dict()
                if i["has_field_proud_skill_group_id"]:
                    prop_proud["proudSkillGroupId"] = i["proud_skill_group_id"]["value"]
                
                if i["has_field_need_avatar_promote_level"]:
                    prop_proud["needAvatarPromoteLevel"] = i["need_avatar_promote_level"]["value"]
                inherent_proud_skill_opens.append(prop_proud)
            output_block["inherentProudSkillOpens"] = inherent_proud_skill_opens

            output_block["skillDepotAbilityGroup"] = block["skill_depot_ability_group"]["data"]

            output.append(output_block)

    with open('./json/AvatarSkillDepotExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)

def DumpAvatarSkill():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarSkillExcelConfigData.bin', './ksy/avatar_skill.ksy']

    with open('./json/Dump_AvatarSkillExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def ParseAvatarSkill():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarSkillExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()
            output_block["id"] = block["id"]["value"]
            output_block["nameTextMapHash"] = block["name"]["value"]
            output_block["abilityName"] = block["ability_name"]["data"]
            output_block["descTextMapHash"] = block["desc"]["value"]
            output_block["skillIcon"] = block["skill_icon"]["data"]
            
            if block["has_field_cd_time"]:
                output_block["cdTime"] = block["cd_time"]

            if block["has_field_cost_elem_type"]:
                output_block["costElemType"] = block["cost_elem_type"]["value"][13:].title()
            if block["has_field_cost_elem_val"]:
                output_block["costElemVal"] = block["cost_elem_val"]

            if block["has_field_cost_stamina"]:
                output_block["costStamina"] = block["cost_stamina"]
            
            output_block["maxChargeNum"] = block["max_charge_num"]["value"]
            
            if block["has_field_trigger_id"]:
                output_block["triggerID"] = block["trigger_id"]["value"]
            
            output_block["lockShape"] = block["lock_shape"]["data"]
            output_block["lockWeightParams"] = block["lock_weight_params"]["data"]
            
            if block["has_field_is_attack_camera_lock"]:
                output_block["isAttackCameraLock"] = bool(block["is_attack_camera_lock"])
            
            output_block["buffIcon"] = block["buff_icon"]["data"]

            if block["has_field_proud_skill_group_id"]:
                output_block["proudSkillGroupId"] = block["proud_skill_group_id"]["value"]
            
            output_block["globalValueKey"] = block["global_value_key"]["data"]

            output.append(output_block)

    with open('./json/AvatarSkillExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)

def DumpFetterInfo():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/FetterInfoExcelConfigData.bin', './ksy/fetter_info.ksy']

    with open('./json/Dump_FetterInfoExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)
        
def ParseFetterInfo():
    ksy = {}
    output = []

    with open('./json/Dump_FetterInfoExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            # parse contents
            if block["has_field_info_birth_month"]:
                output_block["infoBirthMonth"] = block["info_birth_month"]["value"]
            
            if block["has_field_info_birth_day"]:
                output_block["infoBirthDay"] = block["info_birth_day"]["value"]
            
            output_block["avatarNativeTextMapHash"] = block["avatar_native"]["value"]
            output_block["avatarVisionBeforTextMapHash"] = block["avatar_vision_befor"]["value"]
            output_block["avatarConstellationBeforTextMapHash"] = block["avatar_constellation_befor"]["value"]
            output_block["avatarTitleTextMapHash"] = block["avatar_title"]["value"]
            output_block["avatarDetailTextMapHash"] = block["avatar_detail"]["value"]
            output_block["avatarAssocType"] = str(block["avatar_assoc_type"]["value"])[11:].upper()
            output_block["cvChineseTextMapHash"] = block["cv_chinese"]["value"]
            output_block["cvJapaneseTextMapHash"] = block["cv_japanese"]["value"]
            output_block["cvEnglishTextMapHash"] = block["cv_english"]["value"]
            output_block["cvKoreanTextMapHash"] = block["cv_korean"]["value"]
            output_block["avatarVisionAfterTextMapHash"] = block["avatar_vision_after"]["value"]
            output_block["avatarConstellationAfterTextMapHash"] = block["avatar_constellation_after"]["value"]
            output_block["fetterId"] = block["fetter_id"]["value"]
            output_block["avatarId"] = block["avatar_id"]["value"]

            output.append(output_block)

    with open('./json/FetterInfoExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)        


"""
def DumpAvatarSkillExcel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarSkillExcelConfigData.bin', './ksy/avatar_skill.ksy']

    with open('./json/Dump_AvatarSkillExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)
        
def ParseAvatarSkillExcel():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarSkillExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            # parse contents

            output.append(output_block)

    with open('./json/AvatarSkillExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)        
"""

def PrettyView():
    global ParseCharacterID

    with open("./json/TextMap_" + TextMapLanguage + ".json", "r", encoding='utf-8') as dump:
        textMap = json.load(dump)

        with open('./json/AvatarExcelConfigData.json', 'r') as dump:
            ksy = json.load(dump)

            for block in ksy:
                if block["id"] == ParseCharacterID:
                    print(textMap[str(block["nameTextMapHash"])])
                    print(textMap[str(block["descTextMapHash"])])

                    print(block["weaponType"])

                    print(block["hpBase"])
                    print(block["attackBase"])
                    print(block["defenseBase"])
                    print(block["critical"])
                    print(block["criticalHurt"])


# To-Do
# AvatarPromoteExcelConfigData.json
# AvatarTalentExcelConfigData.json

# Calculation
# baseHP * FetterInfoExcelConfigData[CurrentLevel] + AvatarPromoteExcelConfigData[CurrentPromoteLevel]


# GetAllTextmaps()

# DumpAvatarExcel()
# ParseAvatarExcel()

# DumpAvatarSkillDepot()
# ParseAvatarSkillDepot()

# DumpAvatarSkill()
# ParseAvatarSkill()

# DumpFetterInfo()
# ParseFetterInfo()

# PrettyView()