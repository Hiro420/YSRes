from kaitaistruct import KaitaiStream
import xlsxwriter
from io import BytesIO
import glob, os, sys, json, re
import subprocess
from multiprocessing import Process
import character

sys.path.append("./py")
from textmap import Textmap

'''
    01/26692920 => CHS
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
    global textMapLanguage
    output = dict()

    total = len(glob.glob('./bin/TextMap_' + textMapLanguage + '/*.bin'))
    cnt = 0

    for file in glob.glob('./bin/TextMap_' + textMapLanguage + '/*.bin'):

        cnt += 1
        print("Parsing textMap in progress [" + str(cnt) + "/" + str(total) + "]", end='\r')

        with open(file, 'rb') as f:
            stream = KaitaiStream(BytesIO(f.read()))
            obj = Textmap(stream)

            for block in obj.textmap:
                output[str(block.hash.value)] = block.string.data

    with open("./json/TextMap_" + textMapLanguage + ".json", "w", encoding='utf-8') as json_file:
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
                    add_prop["propType"] = i["prop_type"]["value"][16:].upper()
                if i["has_field_value"]:
                    add_prop["value"] = i["value"]
                add_props.append(add_prop)
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

def DumpMaterialExcel():
    cmd = ['ksdump', '-f', 'json', './bin/ExcelBinOutput/MaterialExcelConfigData.bin', './ksy/material_excel.ksy']

    with open('./json/Dump_MaterialExcelConfigData.json', 'w') as out:
        return_code = subprocess.call(cmd, stdout=out)
        
def ParseMaterialExcel():
    ksy = {}
    output = []

    with open('./json/Dump_MaterialExcelConfigData.json', 'r') as dump:
        ksy = json.load(dump)

        for block in ksy["block"]:

            output_block = dict()

            # parse only needed, don't use this generated in ps resources
            output_block["id"] = block["id"]["value"]
            output_block["nameTextMapHash"] = block["name"]["value"]
            output_block["descTextMapHash"] = block["desc"]["value"]
            output_block["icon"] = block["icon"]["data"]

            output.append(output_block)

    with open('./json/MaterialExcelConfigData.json', 'w') as json_file:
        json.dump(output, json_file, indent=4)        

def GenerateRes(parseCharacterID, textMapLanguage):
    with open(os.path.join(os.path.dirname(__file__), f'json/TextMap_{textMapLanguage}.json')) as textmap_json:
        textmap = json.load(textmap_json)

    character.characterExtraction(textmap, parseCharacterID)

    with open(os.path.join(os.path.dirname(__file__), f'res/{parseCharacterID}.json')) as dump:
        res = json.load(dump)
    
        wb = xlsxwriter.Workbook(f'./res/{parseCharacterID}.xlsx')
        ws = wb.add_worksheet()

        name_format = wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vjustify'
        })

        desc_format = wb.add_format({
            'align': 'center',
            'valign': 'vjustify',
            'text_wrap': True
        })

        ws.merge_range('A1:H1', res["Name"], name_format)

        rarity_dic = {
            "QUALITY_ORANGE": "5*",
            "QUALITY_PURPLE": "4*"
        }

        weapon_dic = {
            "WEAPON_BOW": "Bow",
            "WEAPON_CATALYST": "Catalyst",
            "WEAPON_CLAYMORE": "Claymore",
            "WEAPON_POLE": "Polearm",
            "WEAPON_SWORD_ONE_HAND": "Sword"
        }

        asc_dic = {
            "FIGHT_PROP_HP_PERCENT": "HP%",
            "FIGHT_PROP_ATTACK_PERCENT": "ATK%",
            "FIGHT_PROP_DEFENSE_PERCENT": "DEF%",
            "FIGHT_PROP_ELEMENT_MASTERY": "Elemental Mastery",
            "FIGHT_PROP_CHARGE_EFFICIENCY": "Energy Recharge",
            "FIGHT_PROP_HEAL_ADD": "Heal Bonus",
            "FIGHT_PROP_CRITICAL_HURT": "Crit Damage",
            "FIGHT_PROP_CRITICAL": "Crit Rate",
            "FIGHT_PROP_PHYSICAL_ADD_HURT": "Phys Bonus",
            "FIGHT_PROP_GRASS_ADD_HURT": "Dendro Bonus",
            "FIGHT_PROP_ROCK_ADD_HURT": "Geo Bonus",
            "FIGHT_PROP_WIND_ADD_HURT": "Anemo Bonus",
            "FIGHT_PROP_WATER_ADD_HURT": "Hydro Bonus",
            "FIGHT_PROP_ICE_ADD_HURT": "Cryo Bonus",
            "FIGHT_PROP_ELEC_ADD_HURT": "Electro Bonus",
            "FIGHT_PROP_FIRE_ADD_HURT": "Pyro Bonus"
        }

        ws.merge_range('A2:B2', "Rarity", name_format)
        ws.merge_range('C2:D2', rarity_dic[res["Rarity"]], desc_format)

        ws.merge_range('A3:B3', "Weapon", name_format)
        ws.merge_range('C3:D3', weapon_dic[res["Weapon"]], desc_format)

        ws.merge_range('A4:B4', asc_dic[list(res["StatsModifier"]["Ascension"][5].keys())[3]], name_format)

        if list(res["StatsModifier"]["Ascension"][5].keys())[3] == "FIGHT_PROP_ELEMENT_MASTERY":
            ws.merge_range('C4:D4', "{0:.0f}".format(res["StatsModifier"]["Ascension"][5][list(res["StatsModifier"]["Ascension"][5].keys())[3]]), desc_format)
        else:
            ws.merge_range('C4:D4', "{0:.1%}".format(res["StatsModifier"]["Ascension"][5][list(res["StatsModifier"]["Ascension"][5].keys())[3]]), desc_format)

        ws.merge_range('E2:F2', "HP", name_format)
        ws.merge_range('G2:H2', int(res["BaseHP"] * res["StatsModifier"]["HP"]["90"] + res["StatsModifier"]["Ascension"][5]["FIGHT_PROP_BASE_HP"]) , desc_format)

        ws.merge_range('E3:F3', "ATK", name_format)
        ws.merge_range('G3:H3', int(res["BaseATK"] * res["StatsModifier"]["ATK"]["90"] + res["StatsModifier"]["Ascension"][5]["FIGHT_PROP_BASE_ATTACK"]) , desc_format)

        ws.merge_range('E4:F4', "DEF", name_format)
        ws.merge_range('G4:H4', int(res["BaseDEF"] * res["StatsModifier"]["DEF"]["90"] + res["StatsModifier"]["Ascension"][5]["FIGHT_PROP_BASE_DEFENSE"]) , desc_format)

        ws.merge_range('A6:J6', "Promote Costs", name_format)
        for i in range(6):
            ws.write(i+6, 0, i+1, name_format)

            items = []
            for j in res["Materials"]["Ascensions"][i]["Mats"]:
                items.append(j["Name"] + " x" + str(j["Count"]))

            ws.merge_range(i+6, 1, i+6, 9, ", ".join(items), desc_format)

        ws.merge_range('A14:J14', "Skill Upgrade Costs", name_format)
        for i in range(9):
            ws.write(i+14, 0, "Lv." + str(i+2), name_format)

            items = []
            for j in res["Materials"]["Talents"][0][i]["Mats"]:
                items.append(j["Name"] + " x" + str(j["Count"]))
            
            ws.merge_range(i+14, 1, i+14, 9, ", ".join(items), desc_format)

        ws.merge_range('A25:L25', "Constellations", name_format)
        ws.write('M25', "Real Value", desc_format) # via ParamList
        for i in range(6):
            ws.merge_range(i+25, 0, i+25, 1, res["Constellations"][i]["Name"], name_format)
            ws.merge_range(i+25, 2, i+25, 11, ConvertText(res["Constellations"][i]["Desc"]), desc_format)
            ws.write(i+25, 12, str([i for i in res["Constellations"][i]["ParamList"] if i != 0.0]), desc_format) 
            ws.set_row(i+25, 100)

        ws.merge_range('A33:L33', "Passives", name_format)
        ws.write('M33', "Real Value", desc_format) # via ParamList
        current_row = 33
        for i in range(len(res["Passives"])):
            ws.merge_range(i+33, 0, i+33, 1, res["Passives"][i]["Name"], name_format)
            ws.merge_range(i+33, 2, i+33, 11, ConvertText(res["Passives"][i]["Desc"]), desc_format)
            ws.write(i+33, 12, str([i for i in res["Passives"][i]["ParamList"] if i != 0.0]), desc_format)
            ws.set_row(i+33, 100) # Skill issue

        current_row = current_row + len(res["Passives"]) + 1

        for i in range(len(res["Skills"])):
            ws.merge_range(current_row, 0, current_row, 15, res["Skills"][i]["Name"], name_format)
            current_row += 1
            ws.merge_range(current_row, 0, current_row, 15, ConvertText(res["Skills"][i]["Desc"]), desc_format)
            ws.set_row(current_row, 200) # Skill issue
            current_row += 1
            
            ws.write(current_row, 0, "Modifier", name_format)
            for j in range(15):
                ws.write(current_row, j+1, "Lv." + str(j+1), name_format)
            current_row += 1

            for j in list(res["Skills"][i]["Param"].keys()):
                ws.write(current_row, 0, j)

                
                param_form = res["Skills"][i]["Param"][j]["Name"].split("|")[1]

                pattern = "\{param.*?:(.*?)\}"
                param_parsed = re.split(pattern, param_form)
                type_val = {
                    "P": "{0:.0%}",
                    "F1P": "{0:.1%}",
                    "F2P": "{0:.2%}",
                    "I": "{:0.0f}",
                    "F1": "{:0.1f}",
                    "F2": "{:0.2f}",
                }
                
                for k in range(15):
                    values = res["Skills"][i]["Param"][j]["Levels"][k]
                    out_val = ""
                    for val in param_parsed:
                        if val in list(type_val.keys()):
                            out_val += type_val[val].format(values.pop(0))
                        else:
                            out_val += val

                    ws.write(current_row, k+1, out_val, desc_format)
                
                current_row += 1
        
            current_row += 1

        wb.close()


def ConvertText(desc):
    desc = desc.replace("\\n", "\n")

    pattern = "<color.*?>(.+?)</color>"
    desc_parsed = re.split(pattern, desc)
    
    return "".join(desc_parsed)


if __name__ == '__main__':
    print("YSRes blk parser tool")
    print("Place MiHoYoBinData .bin files in the ./bin folder")
    print("")
    
    # Arg would support later

    dumpTextmap = input("Dump Textmap? (y/n, default=y) : ")
    textMapLanguage = input("Type the textMap Language (Example: KR) : ")

    if dumpTextmap == "" or dumpTextmap.lower() == "y" or dumpTextmap.lower() == "yes":
        print(f"Dumping TextMap_{textMapLanguage}...")
        GetAllTextmaps()

    dumpBin = input("Dump .bin to .json? (y/n, default=y) : ")
    parseBin = input("Parse dumped json to res json? (y/n, default=y) : ")
    generateRes = input("Generate output? (y/n, default=y) : ")
    
    if dumpBin == "" or dumpBin.lower() == "y" or dumpBin.lower() == "yes":
        print("Dumping .bin files...")

        p0 = Process(target=DumpAvatarExcel)
        p1 = Process(target=DumpAvatarSkillDepot)
        p2 = Process(target=DumpAvatarSkill)
        p3 = Process(target=DumpAvatarTalent)
        p4 = Process(target=DumpAvatarPromote)
        p5 = Process(target=DumpFetterInfo)
        p6 = Process(target=DumpProudSkill)
        p7 = Process(target=DumpMaterialExcel)

        p0.start()
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()
        
        p0.join()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        print("This may take a long time...")
        p6.join()
        p7.join()

    if parseBin == "" or parseBin.lower() == "y" or parseBin.lower() == "yes":
        print("Parsing AvatarExcelConfigData...")
        ParseAvatarExcel()
        print("Parsing AvatarSkillDepotExcelConfigData...")
        ParseAvatarSkillDepot()
        print("Parsing AvatarSkillExcelConfigData...")
        ParseAvatarSkill()
        print("Parsing AvatarTalentExcelConfigData...")
        ParseAvatarTalent()
        print("Parsing AvatarPromoteExcelConfigData...")
        ParseAvatarPromote()
        print("Parsing FetterInfoExcelConfigData...")
        ParseFetterInfo()
        print("Parsing ProudSkillExcelConfigData...")
        ParseProudSkill()
        print("Parsing MaterialExcelConfigData...")
        ParseMaterialExcel()
    
    if generateRes == "" or generateRes.lower() == "y" or generateRes.lower() == "yes":

        parseCharacterID = int(input("Type the character ID (Example: 10000078) : "))
        textMapLanguage = input("Type the textMap Language (Example: KR) : ")
        print("")

        print("Generating res via GenshinScripts...")
        GenerateRes(parseCharacterID, textMapLanguage)
