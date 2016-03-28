"""
This script takes a string of comma seperated card ids and prints out a list
of file asset paths to be used with the build asset bundle jenkins job to deploy
building (prefab,icon) to the master branch.
"""
import google_drive_authenticate
import gspread
import sys

if len(sys.argv) <= 1:
    sys.exit(1)

gc = google_drive_authenticate.authenticate_google_docs()

exportBuildIds = sys.argv[1:]

#Format Building:
building_thumbnail_file_format="Building/ThumbnailTextures/{0}.png"
building_prefab_file_format="Building/Prefabs/{0}.prefab"
#Format Decoration:
decoration_thumbnail_file_format="Building/ThumbnailTextures/{0}.png"
decoration_prefab_file_format="Building/Prefabs/{0}.prefab"

#Format Output:
asset_file_output_string=''

#Gspread Access:
CityBuildingLevelMaster = gc.open_by_key('1Pc7YV7ojBxrMPKtWWvSArDo3HifIZ9LJ23DVg5024x4')
CityBuildingLevelMasterSheet = CityBuildingLevelMaster.sheet1;

#CityBuildingLevelMasterSheet Information
CityBuildingLevelMasterHeaders = CityBuildingLevelMasterSheet.row_values(1)
buildingIds = CityBuildingLevelMasterSheet.col_values(CityBuildingLevelMasterHeaders.index("buildingId") + 1)

#Helper Functions
def buildBuilding(cellValue, asset_file_output_string):
    asset_file_output_string += building_thumbnail_file_format.format(cellValue) + "," + building_prefab_file_format.format(cellValue) + ","
    return asset_file_output_string

def buildDecoration(cellValue, asset_file_output_string):
    asset_file_output_string += decoration_thumbnail_file_format.format(cellValue) + "," + decoration_prefab_file_format.format(cellValue) + ","
    return asset_file_output_string

#unique Models
uniqueModels = set()

#ArgumentLoop
for buildIds in exportBuildIds:
    sheetIterator = 1
    for id in buildingIds:
        if buildIds == id:
            cellValue = CityBuildingLevelMasterSheet.cell(sheetIterator, 3).value
            #print cellValue
            if cellValue not in uniqueModels:
                #print cellValue
                if cellValue[0] == "b":
                    #print "do B"
                    asset_file_output_string = buildBuilding(cellValue, asset_file_output_string)
                else:
                    #print "do D"
                    asset_file_output_string = buildDecoration(cellValue, asset_file_output_string)
                uniqueModels.add(cellValue)

        sheetIterator = sheetIterator + 1

asset_file_output_string = asset_file_output_string[:-1]
print asset_file_output_string