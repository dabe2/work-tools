"""
This script takes a string of comma seperated weapon ids and prints out a list
of file asset paths to be used with the build asset bundle jenkins job to deploy
weapons and their associated action skill to the master branch.
"""
import google_drive_authenticate
import gspread
import sys

if len(sys.argv) <= 1:
    sys.exit(1)

gc = google_drive_authenticate.authenticate_google_docs()

exportWeaponIds = sys.argv[-1].split(',')
print exportWeaponIds

#thumbnail, prefab, action skills->animation,effect
thumbnail_file_format="Weapon/ThumbnailTextures/wep_{wId:08d}.png"#./WcatUnity/Assets/App/ExternalResources/Weapon/ThumbnailTextures/wep_00010000.png
weapon_prefab_file_format="Weapon/Prefabs/wep_{wId:08d}.prefab" #./WcatUnity/Assets/App/ExternalResources/Weapon/Prefabs/wep_00010000.prefab
weapon_sub_prefab_file_format="Weapon/Prefabs/wep_{wId:08d}_sub.prefab" #Weapon/Prefabs/wep_00079123_sub.prefab
asset_file_output_string='' #format is Weapon/ThumbnailTextures/wep_00010000.png,Weapon/Prefabs/wep_00010000.prefab

action_skill_file_format="Action/{0}.asset"
action_skill_output_string='' #comma seperated with a space after the comma :act_00040273.asset, act_00040274.asset
#when skill type = 1, build up the string and just call the ImportEffectsFromJPVersion job with the string

weaponMaster = gc.open_by_key('1M2apGU5XVC1T9asbflApCCZis5WgYxnrGhhGd6BoLJE')
weaponMasterSheet = weaponMaster.sheet1;

weaponMasterHeaders = weaponMasterSheet.row_values(1)

weaponId = weaponMasterSheet.col_values(weaponMasterHeaders.index('id'))
evolveId = weaponMasterSheet.col_values(weaponMasterHeaders.index('evolve'))
weaponCategory = weaponMasterSheet.col_values(weaponMasterHeaders.index('category'))

actionSkillMaster = gc.open_by_key('1kJwNd9rDuQV5NuBBYHeP1yLqa7vRHqurKyCQEP_XEJE')
actionSkillMasterSheet = actionSkillMaster.sheet1;

attackMaster = gc.open_by_key('19fs8m5_i-NE0_a3SUhs88i3tgylu_JsLeBkwCYmkugg')
attackMasterSheet = attackMaster.sheet1;

all_weap_ids = weaponMasterSheet.col_values(2)
all_aSkill_ids = actionSkillMasterSheet.col_values(1)
all_attack_ids = attackMasterSheet.col_values(2)

uniqueWeaponActs = set()

#Function addEvolveWeapon adds the evolved weaponId to exportWeaponIds if the value is not -1
def addEvolveWeapon(evolveValue):
    if evolveValue != "-1":
        exportWeaponIds.append(evolveValue)

#Function buildAssetFileOutputString builds the .png and .prefab, it also sees if its "category" is 7,
# if so, it will build a subprefab.
def buildAssetFileOutputString(asset_file_output_string, weaponMasterIterator):
    exportIdNum = int(float(w_id))
    asset_file_output_string += thumbnail_file_format.format(wId=exportIdNum) + "," + weapon_prefab_file_format.format(wId=exportIdNum) + ","
    if weaponMasterSheet.cell(weaponMasterIterator, 53).value == "7":
        asset_file_output_string += weapon_sub_prefab_file_format.format(wId=exportIdNum) + ","
    return asset_file_output_string

#Function checkWeaponActs looks at Column 18,20,22,24 to check if the type is 1. if so it
# will traverse through ActionSkillMaster and AttackMaster to find the correct act files.
def checkWeaponActs(action_skill_output_string, WeaponMasterIterator):
    for typeCol in range(18, 25, 2):
        if weaponMasterSheet.cell(weaponMasterIterator, typeCol).value == "1":
            actionSkillId = weaponMasterSheet.cell(weaponMasterIterator, typeCol + 1).value
            ActionSkillMasterIterator = 1

            for aSkill_id in all_aSkill_ids:
                if actionSkillId == aSkill_id:
                    actionId = actionSkillMasterSheet.cell(ActionSkillMasterIterator, 18).value
                    AttackMasterIterator = 1
                    for attack_id in all_attack_ids:
                        if actionId == attack_id:
                            if attackMasterSheet.cell(AttackMasterIterator, 5).value not in uniqueWeaponActs:
                                action_skill_output_string += action_skill_file_format.format(attackMasterSheet.cell(AttackMasterIterator, 5).value) + ", "
                                uniqueWeaponActs.add(attackMasterSheet.cell(AttackMasterIterator, 5).value)

                        AttackMasterIterator = AttackMasterIterator + 1

                ActionSkillMasterIterator = ActionSkillMasterIterator + 1
    return action_skill_output_string

for weaponSkillNum in range(4):
    pass

#Append more evolutions to our args.

for weaponId in exportWeaponIds:
    weaponMasterIterator = 1
    for w_id in all_weap_ids:
        if w_id == weaponId:
            #print w_id
            addEvolveWeapon(weaponMasterSheet.cell(weaponMasterIterator, 34).value)
            asset_file_output_string = buildAssetFileOutputString(asset_file_output_string, weaponMasterIterator)
            action_skill_output_string = checkWeaponActs(action_skill_output_string, weaponMasterIterator)

        weaponMasterIterator = weaponMasterIterator + 1


asset_file_output_string = asset_file_output_string[:-1]
action_skill_output_string = action_skill_output_string[:-2]

#End Result
print "----End Result-------"
print asset_file_output_string
print "---------------------"
print action_skill_output_string