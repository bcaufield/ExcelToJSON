# This is an example tool to convert the US turnout standard data US-Turnout-Catalog-Sample-920-18.xlsx to US turnout catalog -'US_Imperial.json' and 'US_Metric.json'.
# Verified Python version: 3.9.7. Note that dump json with low version python may cause the json nodes disorder issue.
# Verified Python xlrd version: 1.2.0. Note that high version xlrd cannot support the xlrd.open_workbook
# Sample Python install scripts FYI: $pip list &  $pip uninstall xlrd  &  $pip install xlrd==1.2.0
# Readme: the files are in the same folder with this python script file.
# Input: sample json file 'US_Imperial_base.json' ; US catalog data US-Turnout-Catalog-Sample-920-18.xlsx 
# Output: 'US_Imperial.json' and 'US_Metric.json'

import os
import sys
import json
import math
import xlrd

SheetStartRowNum = 7 # conversion from 8th row to the end in the sheet US-Turnout-Catalog-Sample-920-18.xlsx 
DesignSpeedMi = 80
HeelSpreadInch = 6.25
InchToFeet = 12.0
MiToKm = 1.609
FeetToMeter = 0.3048
#--------------------
def indentJson(j, sortkeys=True):
	return json.dumps(j, indent=4, sort_keys=sortkeys)

def saveJson(j, filename, sortkeys=True):
	with open(filename, 'w+') as outfile:
		outfile.write(indentJson(j, sortkeys))

def readJson(filename):
	with open(filename, 'r', encoding='utf-8') as infile:
		return json.load(infile)
	return {}

def FeetInchXY(feet, inch , x, y):
	if (x=='' or x == 0 or y == 0):
		return feet + inch/InchToFeet
	else:
		return feet + (inch + x/y)/InchToFeet

def FeetInchXY_row(rows_i, y):
	return FeetInchXY(rows_i[y], rows_i[y+1],rows_i[y+2],rows_i[y+3])

def ConvertAngle(deg, min, sec):
	return deg + min/60 +  sec / 3600;

def ConvertAngle_row(rows_i, y):
	return ConvertAngle(rows_i[y], rows_i[y+1],rows_i[y+2])

def InchXY_row(rows_i, y):
	if (rows_i[y] > 0):
		return (rows_i[y] + rows_i[y+1]/ rows_i[y+2]) /InchToFeet
	else:
		return -(-rows_i[y] + rows_i[y+1]/ rows_i[y+2]) /InchToFeet

def ToMeter(feet):
	return feet*FeetToMeter

def toModels(model1, sheet1, nrows, newmodel_base, isFeet=True):
	model1.clear()
	for i in range(SheetStartRowNum, nrows): # from 8th row to the end
		rows_i = sheet1.row_values(i)
		cell0 = rows_i[0]
		newmodel = newmodel_base.copy()
		newmodel["name"] = cell0
		parameters = newmodel["parameters"].copy()
		if (isFeet):
			parameters["us_switch_length"] = FeetInchXY_row(rows_i, 2)
			parameters["us_toe_distance_d"] = InchXY_row(rows_i, 29)
			parameters["us_toe_length"] = FeetInchXY_row(rows_i, 62)
			parameters["us_crossover_track"] = FeetInchXY_row(rows_i, 80)
			parameters["us_actual_lead"] = FeetInchXY_row(rows_i, 13)
			parameters["us_straight_track"] = FeetInchXY_row(rows_i, 76)
			parameters["us_heel_length"] = FeetInchXY_row(rows_i, 66)
			parameters["us_radius_of_center_line"] = rows_i[25]
			parameters["us_heel_spread"] = HeelSpreadInch/InchToFeet
			parameters["design_speed"] = DesignSpeedMi
		else:
			parameters["us_switch_length"] = ToMeter(FeetInchXY_row(rows_i, 2))
			parameters["us_toe_distance_d"] = ToMeter(InchXY_row(rows_i, 29))
			parameters["us_toe_length"] = ToMeter(FeetInchXY_row(rows_i, 62))
			parameters["us_crossover_track"] = ToMeter(FeetInchXY_row(rows_i, 80))
			parameters["us_actual_lead"] = ToMeter(FeetInchXY_row(rows_i, 13))
			parameters["us_straight_track"] = ToMeter(FeetInchXY_row(rows_i, 76))
			parameters["us_heel_length"] = ToMeter(FeetInchXY_row(rows_i, 66))
			parameters["us_radius_of_center_line"] = ToMeter(rows_i[25])
			parameters["us_heel_spread"] = ToMeter(HeelSpreadInch/InchToFeet)
			parameters["design_speed"] = DesignSpeedMi * MiToKm
			newmodel["parameter_overrides"]["design_speed"]["default_value"] = DesignSpeedMi * MiToKm

		parameters["us_heel_angle"] = ConvertAngle_row(rows_i, 6)
		frogAngle = ConvertAngle_row(rows_i, 55)
		parameters["us_frog_angle"] = frogAngle
		tanValue = math.tan(math.radians(frogAngle))
		parameters["rotation_angle_tan"] = round(tanValue, 4)
		parameters["rotation_angle_tan_filter"] =  '{0:.4f}'.format(tanValue)
		newmodel["parameters"] = parameters
		model1.append(newmodel)

def convertToUSJson(datafile, standardfile, outputfile, isFeet, sheet1, nrows):
	jsonBase = readJson(standardfile)
	#print("jsonBase =" + jsonBase.__str__() + " standardfile=" + standardfile + " isFeet=" + isFeet.__str__())  
	models = jsonBase["models"]
	newmodel_base = models[0].copy()
	toModels(models, sheet1, nrows, newmodel_base, isFeet)
	saveJson(jsonBase, outputfile, False)
	print( str(len(models)) + " models are converted.")
	#print("Finsh the conversion to Json file:" + outputfile)



#------------------------------------------------------------------------
#datafile     = '/Users/bcaufield/source/Python/convert_c3d/US-Turnout-Catalog-Sample-920-18.xlsx'
#standardfile = '/Users/bcaufield/source/Python/convert_c3d/US_Imperial_base.json'
#standardfileOuput = '/Users/bcaufield/source/Python/convert_c3d/US_Imperial.json'
#datafile     = '/uploads/US-Turnout-Catalog-Sample-920-18.xlsx'
datafile     = ''
standardfile = '/US_Imperial_base.json'
standardfileOuput = '/US_Imperial.json'

standardfileOuput_Metric = 'US_Metric.json'
if len(sys.argv) > 1:
	datafile = sys.argv[1]
if len(sys.argv) > 2:
	standardfile = sys.argv[2]
if len(sys.argv) > 3:
    	standardfileOuput = sys.argv[2]	

if datafile != '' and os.path.exists(datafile):
  data = xlrd.open_workbook(datafile) # open xls file
  sheet1 = data.sheet_by_index(0) # sheet start index 0
  nrows = sheet1.nrows # row number
  print("The row number in the sheet is: " + str(nrows))

  # convert to US imperial
  jsonImperial = readJson(standardfile)
  convertToUSJson(jsonImperial, standardfileOuput, True, sheet1, nrows)

  # convert to US metric
  jsonMeteric = readJson(standardfile)
  jsonMeteric["name"] = "United State Metric"
  jsonMeteric["unit"] = "metric"
  convertToUSJson(jsonMeteric, standardfileOuput_Metric, False, sheet1, nrows)
