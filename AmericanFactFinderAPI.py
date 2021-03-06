#!/usr/bin/env python

# README
# This Python script demonstrates how to access the Census Bureau's American Fact Finder website to find demographic and other information.
# Scroll to the bottom of this script to execute, comment, and uncomment code as needed.

# TO-DOs
# Add code to protect against errors (such as file handling errors or if the web server request returns an error)

# KNOWN ISSUES
# The CSV output file contains blank rows. I've used Excel to remove the blank rows

# NOTES
# See here for the American Fact Finder API Explorer: https://factfinder.census.gov/service/apps/api-explorer/#!/statisticalData/data?p.langId=en

# More information about geographic identifiers can be found here: 
#   https://factfinder.census.gov/service/GeographyIds.html
#   https://jtleider.github.io/censusdata/geographies.html

# Below is a sample reference list of geographic identifiers:
#   8600000US22039       = ZCTA5 22039
#   0500000US51059       = Fairfax County, Virginia
#   1400000US51059492000 = Census Tract 4920, Fairfax County, Virginia

# American Community Survey Dataset Tables
#   B01003    = Population
#   S2301     = Employment Status
#   S1501     = Educational Attainment
#   S1701     = Poverty
#   DP02      = English Language Proficiency

# Enter this URL into a web browser to explore population data for Queens ZIP Code 11432: 
#   http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/8600000US11432?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9

# Enter this URL into a web browser to explore population data for Queens County Census Tract 25: 
#   http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/1400000US36081002500?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9

# Enter this URL into a web browser to explore population data for Queens County: 
# http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/0500000US36081?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9


# Before running, ensure that censustracts.py is stored in the same directory
import requests
import json
import csv
from censustracts import *

def getAmericanCommunitySurvey5YearEstimateValue(year, tableNumber, zipCode):
    #build the URL string, given the parameters
    getUrl = "http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/" + year + "_5YR/tables/" + tableNumber + "/data/8600000US" + zipCode
    parameters = {"maxResults":1, "key":"ea46e190165e1ee608d643fba987f8b3620ec1a9"} #parameters for the URL. My (John Pham's) API key is ea46e190165e1ee608d643fba987f8b3620ec1a9
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
        for zipCode in inputFile: #for each ZIP code in the input file
            zipCodeNum = int(zipCode) #this line removes the line break in the ZIP code
            zipCodeString = str(zipCodeNum) #convert to a string
            ZIPCodeValue = getAmericanCommunitySurvey5YearEstimateValue(year, tableNumber, zipCodeString)
            print(str(zipCodeString) + " " + str(ZIPCodeValue))
            zipCodeNoWhiteSpace = zipCode.rstrip() #remove trailing white space
            outputWriter.writerow([zipCodeNoWhiteSpace,ZIPCodeValue]) #write the ZIP code and value to the CSV output file
        outputFile.close() #close the file

def getAmericanCommunitySurvey5YearEstimateValueByCensusTract(year, tableNumber, censusTract): #return a value from the American Community Survey (ACS) dataset given a year, ACS table number, and Queens County census tract number
    #build the URL string, given the parameters
    getUrl = "http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/" + year + "_5YR/tables/" + tableNumber + "/data/1400000US" + censusTract
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
    
    elif (tableNumber == "S0101"): #S0101 refers to the American Community Survey dataset for age and sex
        tableKey = "C349" #C349 refers to the estimated total of older adults age 65+
        return jsonText["data"]["rows"][0]["cells"][tableKey]["value"]

    else:
        print("Error: This code cannot handle Table Number " + tableNumber)

def outputDatabyCensusTractList(censusTractFileName, CSVoutputFileName, year, tableNumber):
    with open(censusTractFileName, encoding = 'utf-8') as inputFile:
        outputFile = open(CSVoutputFileName,'w',newline=None) #open an output file for writing
        outputWriter = csv.writer(outputFile) #initiate the CSV writer object
        for censusTract in inputFile: #for each ZIP code in the input file
            censusTractNum = int(censusTract) #this line removes the line break in the ZIP code
            censusTractString = str(censusTractNum) #convert to a string
            censusTractValue = getAmericanCommunitySurvey5YearEstimateValueByCensusTract(year, tableNumber, censusTractString)
            print(str(censusTractString) + " " + str(censusTractValue))
            censusTractNoWhiteSpace = censusTract.rstrip() #remove trailing white space
            outputWriter.writerow([censusTractNoWhiteSpace, censusTractValue]) #write the ZIP code and value to the CSV output file
        outputFile.close() #close the file

# Uncomment these lines to run sample queries
#print(getAmericanCommunitySurvey5YearEstimateValue("17","B01003","11432")) #population count
#print("Statistics for ZIP Code 11432")
#print("Unemployment Rate: " + str(format(getAmericanCommunitySurvey5YearEstimateValue("17","S2301","11432"),'.1f')))  #unemployment rate. The code limits the output to one decimal place
#print("Percent without a High School Diploma or Equivalent: " + str(format(getAmericanCommunitySurvey5YearEstimateValue("17","S1501","11432"),'.1f'))) #percentage of people without a HS diploma or equivalency
#print("Poverty Rate: " + str(format(getAmericanCommunitySurvey5YearEstimateValue("17","S1701","11432"),'.1f'))) #poverty rate
#print("Percent with Limited English Language Proficiency: " + str(format(getAmericanCommunitySurvey5YearEstimateValue("17","DP02","11432"),'.1f'))) #limited English language proficiency

# Uncomment these lines to generate a CSV file of values based on an input file containing a list of ZIP codes
#outputDatabyZIPCodeList("QueensZIPCodes.txt","UnemploymentZIP.csv","17","S2301")
#outputDatabyZIPCodeList("QueensZIPCodes.txt","NoHighSchoolZIP.csv","17","S1501")
#outputDatabyZIPCodeList("QueensZIPCodes.txt","PovertyZIP.csv","17","S1701")
#outputDatabyZIPCodeList("QueensZIPCodes.txt","LimitedEnglishZIP.csv","17","DP02")

#Queens County Census Tract 2500 = Queensbridge (New York State's ID = 36 and Queens County's ID is 81)
#censusTract = "36081002500"
#print("Statistics for Census Tract 2500 (Queensbridge) in Queens County, NY")
#print("Unemployment Rate: " + str(format(getAmericanCommunitySurvey5YearEstimateValueByCensusTract("17","S2301",censusTract),'.1f')))  #unemployment rate. The code limits the output to one decimal place
#print("Percent without a High School Diploma or Equivalent: " + str(format(getAmericanCommunitySurvey5YearEstimateValueByCensusTract("17","S1501",censusTract),'.1f'))) #percentage of people without a HS diploma or equivalency
#print("Poverty Rate: " + str(format(getAmericanCommunitySurvey5YearEstimateValueByCensusTract("17","S1701",censusTract),'.1f'))) #poverty rate
#print("Percent with Limited English Language Proficiency: " + str(format(getAmericanCommunitySurvey5YearEstimateValueByCensusTract("17","DP02",censusTract),'.1f'))) #limited English language proficiency

# Uncomment these lines to generate a CSV file of values based on an input file containing a list of ZIP codes
#outputDatabyCensusTractList("NYCHAQueensCensusTracts.txt","UnemploymentCensusTract.csv","17","S2301")
#outputDatabyCensusTractList("NYCHAQueensCensusTracts.txt","NoHighSchoolCensusTract.csv","17","S1501")
#outputDatabyCensusTractList("NYCHAQueensCensusTracts.txt","PovertyCensusTract.csv","17","S1701")
#outputDatabyCensusTractList("NYCHAQueensCensusTracts.txt","LimitedEnglishCensusTract.csv","17","DP02")

#Queens County Census Tract 2500 = Queensbridge (New York State's ID = 36 and Queens County's ID is 81)
#Uncomment these lines to retrieve and output statistics for Queensbridge
#Queensbridge = MyCensusTract("36081002500")
#print("Older Adult Statistics for Census Tract 2500 (Queensbridge) in Queens County, NY")
#print("Total Population: " + str(Queensbridge.totalPopulation))
#print("Total Number of Older Adults Age 65+: " + str(Queensbridge.totalOlderAdults65Plus))
#print("Percentage Population Who Are Older Adults 65+: " + str(Queensbridge.percentageOlderAdults65Plus))
#print("Total Number of Older Adults Age 55+: " + str(Queensbridge.totalOlderAdults55Plus))
#print("Percentage Population Who Are Older Adults 55+: " + str(Queensbridge.percentageOlderAdults55Plus))
#print("Total Number of Older Adults Age 65+ with Known Poverty Status: " + str(Queensbridge.totalOlderAdults65PlusKnownPovertyStatus))
#print("Total Number of Older Adults Age 65+ with Income Below the Poverty Line: " + str(Queensbridge.povertyOlderAdults65Plus))
#print("Percentage of Older Adults Age 65+ Who Are Poor: " + str(Queensbridge.povertyPercentageOlderAdults65Plus))
#print("Total Number of Age 65+ Householders: " + str(Queensbridge.totalAge65PlusHouseholders))
#print("Total Number of Age 65+ Householders Who Live Alone: " + str(Queensbridge.livingAloneAge65PlusHouseholders))
#print("Percentage of Age 65+ Householders Who Live Alone: " + str(Queensbridge.livingAlonePercentageAge65PlusHouseholders))

NYCHACensusTractsAnalysis = MyCensusTractList(createCensusTractArray("NYCHAQueensCensusTracts.txt")) #this creates an array of census tract objects, given a list of census tracts read in from a file
print("Summary of Descriptive Statistics for the Given " + str(NYCHACensusTractsAnalysis.censusTractArrayLength) + " Census Tract(s):")
print("Percentage of older adults 65+: " + "{:.1f}".format(NYCHACensusTractsAnalysis.percentageOlderAdults65Plus)+ "%") #print out with one decimal place
print("Percentage of older adults 55+: " + "{:.1f}".format(NYCHACensusTractsAnalysis.percentageOlderAdults55Plus)+ "%")
print("Percentage of older adults 65+ who are below poverty level: " + "{:.1f}".format(NYCHACensusTractsAnalysis.povertyPercentageOlderAdults65Plus)+ "%")
print("Percentage of older age 65+ who live alone: " + "{:.1f}".format(NYCHACensusTractsAnalysis.livingAlonePercentageAge65PlusHouseholders)+ "%")
print("Percentage of all residents who are Limited English Proficient: " + "{:.1f}".format(NYCHACensusTractsAnalysis.limitedEnglishPercentagePopulation5Plus)+ "%")
print("Percentage of all residents who are below poverty level: " + "{:.1f}".format(NYCHACensusTractsAnalysis.povertyPercentage)+ "%")
print("Percentage of all residents who have not attained a high school diploma or its equivalent: " + "{:.1f}".format(NYCHACensusTractsAnalysis.noHighSchoolPercentagePopulation25Plus)+ "%")
print("Percentage of all residents who are unemployed: " + "{:.1f}".format(NYCHACensusTractsAnalysis.unemploymentPercentage)+ "%")
NYCHACensusTractsAnalysis.exportValues("NYCHA_Data.csv") #output the data to a CSV file