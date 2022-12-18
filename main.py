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

def DumpAvatarTalent():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarTalentExcelConfigData.bin', './ksy/avatar_talent.ksy']

    with open('./json/Dump_AvatarTalentExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)
        
def ParseAvatarTalent():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarTalentExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            output_block["talentId"] = block["talent_id"]["value"]
            output_block["nameTextMapHash"] = block["name"]["value"]
            output_block["descTextMapHash"] = block["desc"]["value"]
            output_block["icon"] = block["icon"]["data"]
            
            if block["has_field_prev_talent"]:
                output_block["prevTalent"] = block["prev_talent"]["value"]

            output_block["mainCostItemId"] = block["main_cost_item_id"]["value"]
            output_block["mainCostItemCount"] = block["main_cost_item_count"]["value"]
            output_block["openConfig"] = block["open_config"]["data"]
            output_block["addProps"] = [{}, {}]
            output_block["paramList"] = block["param_list"]["data"]
            
            output.append(output_block)

    with open('./json/AvatarTalentExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)

def DumpAvatarPromote():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/AvatarPromoteExcelConfigData.bin', './ksy/avatar_promote.ksy']

    with open('./json/Dump_AvatarPromoteExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)

def ParseAvatarPromote():
    ksy = {}
    output = []

    with open('./json/Dump_AvatarPromoteExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            output_block["avatarPromoteId"] = block["avatar_promote_id"]["value"]
            
            if block["has_field_promote_level"]:
                output_block["promoteLevel"] = block["promote_level"]["value"]
                
            if block["has_field_promote_audio"]:
                output_block["promoteAudio"] = block["promote_audio"]["data"]
                
            if block["has_field_scoin_cost"]:
                output_block["scoinCost"] = block["scoin_cost"]["value"]

            cost_items = []
            for i in block["cost_items"]["data"]:
                cost_item = dict()
                if i["has_field_id"]:
                    cost_item["id"] = i["id"]["value"]
                if i["has_field_count"]:
                    cost_item["count"] = i["count"]["value"]
                cost_items.append(cost_item)
            output_block["costItems"] = cost_items

            output_block["unlockMaxLevel"] = block["unlock_max_level"]["value"]

            add_props = []
            for i in block["add_props"]["data"]:
                add_prop = dict()
                if i["has_field_prop_type"]:
                    add_prop["propType"] = i["prop_type"]["value"]
                if i["has_field_value"]:
                    add_prop["value"] = i["value"]
                add_props.append(cost_item)
            output_block["addProps"] = add_props

            if block["has_field_required_player_level"]:
                output_block["requiredPlayerLevel"] = block["required_player_level"]["value"]


            output.append(output_block)

    with open('./json/AvatarPromoteExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)  

def DumpProudSkill():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/ProudSkillExcelConfigData.bin', './ksy/proud_skill.ksy']

    with open('./json/Dump_ProudSkillExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)
        
def ParseProudSkill():
    ksy = {}
    output = []

    with open('./json/Dump_ProudSkillExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            output_block["proudSkillId"] = block["proud_skill_id"]["value"]
            output_block["proudSkillGroupId"] = block["proud_skill_group_id"]["value"]
            output_block["level"] = block["level"]["value"]
            output_block["proudSkillType"] = block["proud_skill_type"]["value"]
            output_block["nameTextMapHash"] = block["name"]["value"]
            output_block["descTextMapHash"] = block["desc"]["value"]
            output_block["unlockDescTextMapHash"] = block["unlock_desc"]["value"]
            output_block["icon"] = block["icon"]["data"]

            if block["has_field_coin_cost"]:
                output_block["coinCost"] = block["coin_cost"]["value"]
            
            cost_items = []
            for i in block["cost_items"]["data"]:
                cost_item = dict()
                if i["has_field_id"]:
                    cost_item["id"] = i["id"]["value"]
                if i["has_field_count"]:
                    cost_item["count"] = i["count"]["value"]
                cost_items.append(cost_item)
            output_block["costItems"] = cost_items
            
            output_block["filterConds"] = [i["value"][19:].upper() for i in block["filter_conds"]["data"]]

            if block["has_field_break_level"]:
                output_block["breakLevel"] = block["break_level"]["value"]

            output_block["paramDescList"] = [i["value"] for i in block["param_desc_list"]["data"]]
            
            
            if block["has_field_life_effect_type"]:
                output_block["lifeEffectType"] = block["life_effect_type"]["data"]
            
            output_block["lifeEffectParams"] = [i["data"] for i in block["life_effect_params"]["data"]]

            if block["has_field_effective_for_team"]:
                output_block["effectiveForTeam"] = block["effective_for_team"]
            
            output_block["openConfig"] = block["open_config"]["data"]
            output_block["addProps"] = [{}, {}]
            output_block["paramList"] = block["param_list"]["data"]

            output.append(output_block)

    with open('./json/ProudSkillExcelConfigData.json', 'w') as json_file:
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
    global ParseCharacterID, TextMapLanguage

    with open("./json/TextMap_" + TextMapLanguage + ".json", "r", encoding='utf-8') as dump:
        textMap = json.load(dump)

    with open('./json/AvatarExcelConfigData.json', 'r') as dump:
        AvatarExcelConfigData = json.load(dump)

    with open('./json/AvatarSkillExcelConfigData.json', 'r') as dump:
        AvatarSkillExcelConfigData = json.load(dump)

    with open('./json/AvatarSkillDepotExcelConfigData.json', 'r') as dump:
        AvatarSkillDepotExcelConfigData = json.load(dump)

    with open('./json/AvatarTalentExcelConfigData.json', 'r') as dump:
        AvatarTalentExcelConfigData = json.load(dump)

    with open('./json/AvatarPromoteExcelConfigData.json', 'r') as dump:
        AvatarPromoteExcelConfigData = json.load(dump)

    with open('./json/FetterInfoExcelConfigData.json', 'r') as dump:
        FetterInfoExcelConfigData = json.load(dump)

    with open('./json/ProudSkillExcelConfigData.json', 'r') as dump:
        ProudSkillExcelConfigData = json.load(dump)

    """ (tsv format)
    Character Name
    Rarity
    Weapon
    baseHP (Lv 90) # baseHP * FetterInfoExcelConfigData[CurrentLevel] + AvatarPromoteExcelConfigData[CurrentPromoteLevel]
    baseATK (Lv 90)
    baseDEF (Lv 90)
    bonusStat

    Promote Cost
    1 ~~~ x1, ~~~ x3, ~~~x5
    2 ~~~ x1, ~~~ x3, ~~~x5
    ...
    6 ~~~ x1, ~~~ x3, ~~~x5

    Skill Upgrade Cost
    2 ~~~ x1, ~~~ x3, ~~~x5
    3 ~~~ x1, ~~~ x3, ~~~x5
    ...
    10 ~~~ x1, ~~~ x3, ~~~x5

    Constellations
    Name Description

    Passives
    Name Description

    Normal Attack
    Name
    Description
    Modifier Lv.1 Lv.2 ... Lv.10
    Multiplier a b c ...

    Elemental Skill

    Elemental Burst

    """

# GetAllTextmaps()

# DumpAvatarExcel()
# ParseAvatarExcel()

# DumpAvatarSkillDepot()
# ParseAvatarSkillDepot()

# DumpAvatarSkill()
# ParseAvatarSkill()

# DumpAvatarTalent()
# ParseAvatarTalent()

# DumpAvatarPromote()
# ParseAvatarPromote()

# DumpFetterInfo()
# ParseFetterInfo()

# DumpProudSkill()
# ParseProudSkill()

PrettyView()