"""
This script takes a string of comma seperated card ids and prints out a list
of file asset paths to be used with the build asset bundle jenkins job to deploy
character (prefab,icon) and their associated action skill to the master branch.
"""
import google_drive_authenticate
import gspread
import sys

if len(sys.argv) <= 1:
    sys.exit(1)

gc = google_drive_authenticate.authenticate_google_docs()

exportCardIds = sys.argv[1:]

#Format: Icon and Prefab
thumbnail_file_format="Card/1_bust/card_{0}_1.png"#./WcatUnity/Assets/App/ExternalResources/Card/1_bust/card_20400510_1.png
card_full_format="Card/2_full/card_{0}_2.png"#./WcatUnity/Assets/App/ExternalResources/Card/2_full/card_20101610_2.png
card_extra1_format="Card/0_icon/card_{0}_0_m.png"
card_extra2_format="Card/0_icon/card_{0}_0.png"
card_prefab_file_format="Character/Prefabs/Player/ply_{0}.prefab"#./WcatUnity/Assets/App/ExternalResources/Character/Prefabs/Player/ply_20601430.prefab
card_voice_file_format="Sound/Voice/Player/{cId}/{sId:02d}.wav"
asset_file_output_string=''#Card/1_bust/card_20400510_1.png,Character/Prefabs/Player/ply_20601430.prefab

#Format: ActionSkill animation and ActionSkill effect
action_skill_id_format="Character/Animations/Player/anm_{wId:08d}.anim"
action_skill_file_format="Action/{0}.asset"
action_skill_output_string='' #comma seperated with a space after the comma :act_00040273.asset, act_00040274.asset


#Gspread Access
CardMaster = gc.open_by_key('1jRu0tEHoxKVq5kGNVL-8XOLoQumQb3qz7ommSCoLe8Q')
CardMasterSheet = CardMaster.sheet1;

ActionSkillMaster = gc.open_by_key('1kJwNd9rDuQV5NuBBYHeP1yLqa7vRHqurKyCQEP_XEJE')
ActionSkillMasterSheet = ActionSkillMaster.sheet1;

AttackMaster = gc.open_by_key('19fs8m5_i-NE0_a3SUhs88i3tgylu_JsLeBkwCYmkugg')
AttackMasterSheet = AttackMaster.sheet1;

#CardMasterSheet Information
CardMasterHeaders = CardMasterSheet.row_values(1)
CardId = CardMasterSheet.col_values(CardMasterHeaders.index("id") + 1)
actionSkillId1 = CardMasterSheet.col_values(CardMasterHeaders.index("actionSkillId1") + 1)
actionSkillId2 = CardMasterSheet.col_values(CardMasterHeaders.index("actionSkillId2") + 1)

#ActionSKillMasterSheet Information
ActionSkillMasterHeaders = ActionSkillMasterSheet.row_values(1)
ActionSkillId = ActionSkillMasterSheet.col_values(ActionSkillMasterHeaders.index("skillId") + 1)

#AttackMasterSheet Information
AttackMasterHeaders = AttackMasterSheet.row_values(1)
allatkId = AttackMasterSheet.col_values(AttackMasterHeaders.index("atkId") + 1)


#Helper Functions.
def buildDirectFromCardId(sCardId, asset_file_output_string):
    voiceFiles = lambda x:card_voice_file_format.format(cId=sCardId, sId=x)
    voiceFilesString =','.join(map(voiceFiles, range(1,32)))
    asset_file_output_string += thumbnail_file_format.format(sCardId) + "," + card_full_format.format(sCardId) + "," + card_prefab_file_format.format(sCardId) + "," + card_extra1_format.format(sCardId) + "," + card_extra2_format.format(sCardId) + "," + voiceFilesString + ","
    return asset_file_output_string


def linkToActId(sActionSkillId, action_skill_output_string):
    rowNumber = ActionSkillId.index(sActionSkillId) + 1
    colNumber = ActionSkillMasterHeaders.index("atkId1") + 1
    return buildActId(ActionSkillMasterSheet.cell(rowNumber, colNumber).value, action_skill_output_string)


def buildActId(atkId, action_skill_output_string):
    rowNumber = allatkId.index(atkId) + 1
    colNumber = AttackMasterHeaders.index("actId") + 1
    #print AttackMasterSheet.cell(rowNumber, colNumber).value
    action_skill_output_string += action_skill_file_format.format(AttackMasterSheet.cell(rowNumber, colNumber).value) + ", "
    return action_skill_output_string

def buildExtraAnim(actionSKillId, asset_file_output_string):
    rowNumber = ActionSkillId.index(actionSKillId) + 1
    colNumber = ActionSkillMasterHeaders.index("atkId1") + 1

    rowNumber1 = allatkId.index(ActionSkillMasterSheet.cell(rowNumber, colNumber).value) + 1
    colNumber1 = AttackMasterHeaders.index("actId") + 1
    test = int(float(AttackMasterSheet.cell(rowNumber1, colNumber1).value[7:]))
    asset_file_output_string += action_skill_id_format.format(wId=test) + ","
    return asset_file_output_string


#Argument loop.
for cardId in exportCardIds:
    asset_file_output_string = buildDirectFromCardId(cardId, asset_file_output_string)

    #Purpose of the +1, -1 nonsense is due to the fact that arrays start at 0, but gDocs start at 1.
    #We use  the offseted numbers to access the .col_Values and its counterpart to use the .cell function.
    rowNumber =  CardId.index(cardId) + 1
    colNumber1 = CardMasterHeaders.index("actionSkillId1") + 1
    colNumber2 = CardMasterHeaders.index("actionSkillId2") + 1
    actionSkill1 = CardMasterSheet.cell(rowNumber, colNumber1).value
    #asset_file_output_string = buildAnimation(actionSkill1, asset_file_output_string)
    actionSkill2 = CardMasterSheet.cell(rowNumber, colNumber2).value
    #asset_file_output_string = buildAnimation(actionSkill2, asset_file_output_string)

    asset_file_output_string = buildExtraAnim(actionSkill1, asset_file_output_string)
    asset_file_output_string = buildExtraAnim(actionSkill2, asset_file_output_string)

    action_skill_output_string = linkToActId(actionSkill1, action_skill_output_string)
    action_skill_output_string = linkToActId(actionSkill2, action_skill_output_string)


asset_file_output_string = asset_file_output_string[:-1]
action_skill_output_string = action_skill_output_string[:-2]
#print asset_file_output_string
#print action_skill_output_string

print asset_file_output_string + "|" + action_skill_output_string







