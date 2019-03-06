# README
# This Python script demonstrates how to access the Census Bureau's American Fact Finder website to find demographic and other information. I wrote this script to learn more about Python's request and json libraries and the American Fact Finder API

# TO-DOs
# 1. Write a function that imports a list of Queens County ZIP Codes and outputs a file that contains various demographic information such as unemployment rate
# 2. Add code to protect against errors (such as file handling errors or if the web server request returns an error)

# KNOWN ISSUES
# The CSV output file contains blank rows. I've used Excel to remove the blank rows


# NOTES
# This is my (John Pham's) American Fact Finder API Access Key: ea46e190165e1ee608d643fba987f8b3620ec1a9

# See here for the American Fact Finder API Explorer: https://factfinder.census.gov/service/apps/api-explorer/#!/statisticalData/data?p.langId=en

# More information about geographic identifiers can be found here: 
#   https://factfinder.census.gov/service/GeographyIds.html
#   https://jtleider.github.io/censusdata/geographies.html
# Below is a sample reference list of geographic identifiers:
# 8600000US22039       = ZCTA5 22039
# 0500000US51059       = Fairfax County, Virginia
# 1400000US51059492000 = Census Tract 4920, Fairfax County, Virginia

# American Community Survey Dataset Tables
# B01003    = Population
# S2301     = Employment Status
# S1501     = Educational Attainment
# S1701     = Poverty
# DP02      = English Language Proficiency

# Enter this URL into a web browser to explore population data for Queens ZIP Code 11432: 
# http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/8600000US11432?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9


import requests
import json
import csv

def getAmericanCommunitySurvey5YearEstimateValue(year, tableNumber, zipCode):
    #build the URL string, given the parameters
    getUrl = "http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/" + year + "_5YR/tables/" + tableNumber + "/data/8600000US" + zipCode
    parameters = {"maxResults":1, "key":"ea46e190165e1ee608d643fba987f8b3620ec1a9"} #parameters for the URL
    requestResult = requests.get(getUrl,params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText) #convert the requested text to JSON format

    if (tableNumber == "B01003"): #B01003 refers to the American Community Survey dataset for the population estimate
        tableKey = tableNumber + "_1_EST" #build a string that will serve as the key for the JSON key-value pair
        return jsonText["data"]["rows"][0]["cells"][tableKey]["value"] #return the population estimate

    elif (tableNumber == "S2301"): #S2301 refers to the American Community Survey dataset for the unemployment rate
        tableKey = "C7" #C7 refers to the unemployment rate for the population age 16 and over
        return jsonText["data"]["rows"][0]["cells"][tableKey]["value"] #return the unemployment rate for the population age 16 and over

    elif (tableNumber == "S1501"):#S1501 refers to the American Community Survey dataset for educational attainment
        tableKey = "C75" #this refers to the percentage of people age 25+ who have less than a 9th grade education
        resultAge25OlderLessThan9thGrade = jsonText["data"]["rows"][0]["cells"][tableKey]["value"] #obtain value
        tableKey = "C87" #this refers to the percentage of people age 25+ who have a 9th-12th grade education but lack a high school diploma or its equivalent
        resultAge25Older9thto12thNoDiploma = jsonText["data"]["rows"][0]["cells"][tableKey]["value"] #obtain value
        #The function is looking to return the sum of C75 and C87:
        return resultAge25OlderLessThan9thGrade + resultAge25Older9thto12thNoDiploma #return the total percentage of people age 25+ who do not have a high school diploma or its equivalent

    elif (tableNumber == "S1701"): #S1701 refers to the American Community Survey dataset for poverty
        tableKey = "C5" #C5 refers to the percentage of population for whom poverty status is determined
        return jsonText["data"]["rows"][0]["cells"][tableKey]["value"]

    elif (tableNumber == "DP02"): #DP02 refers to the American Community Survey dataset called "Selected Social Characteristics in the United States"
        tableKey = "C411" #C411 refers to the percentage of people age 5 and older who speak English less than "very well," among those people who speak a language other than English
        return jsonText["data"]["rows"][0]["cells"][tableKey]["value"]

    else:
        print("Error: This code cannot handle Table Number " + tableNumber)

def outputDatabyZIPCodeList(ZIPCodeFileName, CSVoutputFileName, year, tableNumber):
    with open(ZIPCodeFileName, encoding = 'utf-8') as inputFile:
        outputFile = open(CSVoutputFileName,'w',newline=None) #open an output file for writing
        outputWriter = csv.writer(outputFile) #initiate the CSV writer object
        zipCodeArray = []
        for zipCode in inputFile: #for each ZIP code in the input file
            zipCodeNum = int(zipCode) #this line removes the line break in the ZIP code
            zipCodeString = str(zipCodeNum) #convert to a string
            ZIPCodeValue = getAmericanCommunitySurvey5YearEstimateValue(year, tableNumber, zipCodeString)
            print(str(zipCodeString) + " " + str(ZIPCodeValue))
            outputWriter.writerow([zipCode,ZIPCodeValue]) #write the ZIP code and value to the CSV output file
    outputFile.close() #close the file

# Uncomment these lines to run sample queries
#print(getAmericanCommunitySurvey5YearEstimateValue("17","B01003","11432")) #population count
#print(getAmericanCommunitySurvey5YearEstimateValue("17","S2301","11432"))  #unemployment rate
#print(getAmericanCommunitySurvey5YearEstimateValue("17","S1501","11432")) #percentage of people without a HS diploma or equivalency
#print(getAmericanCommunitySurvey5YearEstimateValue("17","S1701","11432")) #poverty rate
print(getAmericanCommunitySurvey5YearEstimateValue("17","DP02","11432")) #limited English language proficiency

# Uncomment these lines to generate a CSV file of values based on an input file containing a list of ZIP codes
#outputDatabyZIPCodeList("QueensZIPCodes.txt","UnemploymentZIP.csv","17","S2301")
#outputDatabyZIPCodeList("QueensZIPCodes.txt","NoHighSchoolZIP.csv","17","S1501")
#outputDatabyZIPCodeList("QueensZIPCodes.txt","PovertyZIP.csv","17","S1701")
#outputDatabyZIPCodeList("QueensZIPCodes.txt","LimitedEnglishZIP.csv","17","DP02")