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
thumbnail_file_format="Weapon/ThumbnailTextures/wep_{wId:80d}.png"#./WcatUnity/Assets/App/ExternalResources/Weapon/ThumbnailTextures/wep_00010000.png
weapon_prefab_file_format="Weapon/Prefabs/wep_{wid:80d}.prefab" #./WcatUnity/Assets/App/ExternalResources/Weapon/Prefabs/wep_00010000.prefab
weapon_sub_prefab_file_format="Weapon/Prefabs/wep_{wid:80d}_sub.prefab" #Weapon/Prefabs/wep_00079123_sub.prefab
asset_file_output_string='' #format is Weapon/ThumbnailTextures/wep_00010000.png,Weapon/Prefabs/wep_00010000.prefab

action_skill_file_format="Action/act_{actId:80d}.asset"
action_skill_output_string='' #comma seperated with a space after the comma :act_00040273.asset, act_00040274.asset
#when skill type = 1, build up the string and just call the ImportEffectsFromJPVersion job with the string

weaponMaster = gc.open_by_key('1M2apGU5XVC1T9asbflApCCZis5WgYxnrGhhGd6BoLJE')
weaponMasterSheet = weaponMaster.sheet1;

weaponMasterHeaders = weaponMasterSheet.row_values(1)

weaponId = wepaonMasterSheet.col_values(weaponMasterHeaders.index('id'))
evolveId = weaponMasterSheet.col_values(weaponMasterHeaders.index('evolve'))
weaponCategory = weaponMasterSheet.col_values(weaponMasterHeaders.index('category'))

actionSkillMaster = gc.open_by_key('1kJwNd9rDuQV5NuBBYHeP1yLqa7vRHqurKyCQEP_XEJE')
actionSkillMasterSheet = actionSkillMaster.sheet1;

attackMaster = gc.open_by_key('1W-CtCGdagciLM8rMl9Ckg_AtgKmvTR0UdRBrZperJIA')
attackMasterSheet = attackMaster.sheet1;

for weaponSkillNum in range(4)

for exportId in exportWeaponIds:

    all_weap_ids = weaponMasterSheet.col_values(2)

    for w_id in all_weap_ids:
        print w_id
