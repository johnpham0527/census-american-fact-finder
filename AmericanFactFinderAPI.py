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

# Enter this URL into a web browser to explore population data for Queens County Census Tract 25: 
# http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/1400000US36081002500?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9


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


def getACS5YearJSONByCensusTract(year, tableNumber, censusTract): #return JSON data from the American Community Survey (ACS) dataset given a year, ACS table number, and Queens County census tract number
    #build the URL string, given the parameters
    getUrl =    "http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/" + year + "_5YR/tables/" + tableNumber + "/data/1400000US" + censusTract
    parameters = {"maxResults":1, "key":"ea46e190165e1ee608d643fba987f8b3620ec1a9"} #parameters for the URL
    #https://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/S0101/data/1400000US36081002500?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9

    requestResult = requests.get(getUrl,params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText) #convert the requested text to JSON format
    return jsonText


class MyCensusTract:
    def __init__(self, QueensCountyCensusTractNum):
        self.censusTractNum = QueensCountyCensusTractNum
        self.year = "17" #this refers to the American Community Survey yearly 5-year estimate dataset to use. We are using the 2017 as the default.

        #statistics describing the older adult population
        self.totalPopulation = 0
        self.totalOlderAdults65Plus = 0
        self.percentageOlderAdults65Plus = 0
        self.totalOlderAdults55Plus = 0
        self.percentageOlderAdults55Plus = 0
        self.totalOlderAdults65PlusKnownPovertyStatus = 0
        self.povertyOlderAdults65Plus = 0
        self.povertyPercentageOlderAdults65Plus = 0
        self.totalAge65PlusHouseholders = 0
        self.livingAloneAge65PlusHouseholders = 0
        self.livingAlonePercentageAge65PlusHouseholders = 0

        #statistics describing overall community needs
        self.totalPopulation5Plus = 0
        self.limitedEnglishTotalPopulation5Plus = 0
        self.limitedEnglishPercentagePopulation5Plus = 0
        self.povertyPopulation = 0
        self.povertyPercentage = 0
        self.totalPopulation25Plus = 0
        self.noHighSchoolTotalPopulation25Plus = 0
        self.noHighSchoolPercentagePopulation25Plus = 0
        self.totalLaborForce = 0
        self.unemployedLaborForce = 0
        self.unemploymentPercentage = 0

        self.fillOlderAdultValues() #initialize statistics describing the older adult population

    def setYear(self,year): #this function changes which American Community Community yearly dataset to use
        self.year = year

    def fillOlderAdultValues(self):    
        jsonText = getACS5YearJSONByCensusTract(self.year,"S0101",self.censusTractNum) #S0101 refers to the American Community Survey dataset for age and sex

        self.totalPopulation = jsonText["data"]["rows"][0]["cells"]["C1"]["value"] #total population: table key = C1
        self.totalOlderAdults65Plus = jsonText["data"]["rows"][0]["cells"]["C349"]["value"] #older adults age 65+: table key = C349
        self.percentageOlderAdults65Plus = self.totalOlderAdults65Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        populationAge55To59 = jsonText["data"]["rows"][0]["cells"]["C349"]["value"] #older adults age 55-59: table key = C145
        self.totalOlderAdults55Plus = populationAge55To59 + self.totalOlderAdults65Plus 
        self.percentageOlderAdults55Plus = self.totalOlderAdults55Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100

        jsonText = getACS5YearJSONByCensusTract(self.year,"B17001",self.censusTractNum) #B17001 refers to the American Community Survey dataset called "Poverty Status in the Past 12 Months By Sex By Age"
        belowPovertyLevelNumMales65To74 = jsonText["data"]["rows"][0]["cells"]["B17001_15_EST"]["value"] #number of males age 65-74 with income in past 12 months below poverty level
        belowPovertyLevelNumMales75Plus = jsonText["data"]["rows"][0]["cells"]["B17001_16_EST"]["value"] #number of males age 75+ with income in past 12 months below poverty level
        belowPovertyLevelNumFemales65To74 = jsonText["data"]["rows"][0]["cells"]["B17001_29_EST"]["value"] #number of females age 65-74 with income in past 12 months below poverty level
        belowPovertyLevelNumFemales75Plus = jsonText["data"]["rows"][0]["cells"]["B17001_30_EST"]["value"] #number of females age 75+ with income in past 12 months below poverty level
        atOrAbovePovertyLevelNumMales65To74 = jsonText["data"]["rows"][0]["cells"]["B17001_44_EST"]["value"] #number of males age 65-74 with income in past 12 months at or above poverty level
        atOrAbovePovertyLevelNumMales75Plus = jsonText["data"]["rows"][0]["cells"]["B17001_45_EST"]["value"] #number of males age 75+ with income in past 12 months at or above poverty level
        atOrAbovePovertyLevelNumFemales65To74 = jsonText["data"]["rows"][0]["cells"]["B17001_58_EST"]["value"] #number of females age 65-74 with income in past 12 months at or above poverty level
        atOrAbovePovertyLevelNumFemales75Plus = jsonText["data"]["rows"][0]["cells"]["B17001_59_EST"]["value"] #number of females age 75+ with income in past 12 months at or above poverty level
        self.povertyOlderAdults65Plus = belowPovertyLevelNumMales65To74 + belowPovertyLevelNumMales75Plus + belowPovertyLevelNumFemales65To74 + belowPovertyLevelNumFemales75Plus
        self.totalOlderAdults65PlusKnownPovertyStatus = self.povertyOlderAdults65Plus + atOrAbovePovertyLevelNumMales65To74 + atOrAbovePovertyLevelNumMales75Plus + atOrAbovePovertyLevelNumFemales65To74 + atOrAbovePovertyLevelNumFemales75Plus
        self.povertyPercentageOlderAdults65Plus = self.povertyOlderAdults65Plus / self.totalOlderAdults65PlusKnownPovertyStatus * 100 #save this value as a number in the range of 0-100

        jsonText = getACS5YearJSONByCensusTract(self.year,"B11010",self.censusTractNum) #B11010 refers to the American Community Survey dataset called "Nonfamily Households By Sex of Householder By Living Alone By Age of Householder"
        totalLivingAloneMaleHouseholders65Plus = jsonText["data"]["rows"][0]["cells"]["B11010_5_EST"]["value"]
        totalNotLivingAloneMaleHouseholders65Plus = jsonText["data"]["rows"][0]["cells"]["B11010_8_EST"]["value"]
        totalLivingAloneFemaleHouseholders65Plus = jsonText["data"]["rows"][0]["cells"]["B11010_12_EST"]["value"]
        totalNotLivingAloneFemaleHouseholders65Plus = jsonText["data"]["rows"][0]["cells"]["B11010_15_EST"]["value"]
        self.livingAloneAge65PlusHouseholders = totalLivingAloneMaleHouseholders65Plus + totalLivingAloneFemaleHouseholders65Plus
        self.totalAge65PlusHouseholders = self.livingAloneAge65PlusHouseholders + totalNotLivingAloneMaleHouseholders65Plus + totalNotLivingAloneFemaleHouseholders65Plus
        self.livingAlonePercentageAge65PlusHouseholders = self.livingAloneAge65PlusHouseholders / self.totalAge65PlusHouseholders * 100 #save this value as a number in the range of 0-100

    #def setNeedsStatistics():
    #Limited English proficiency
    #poverty
    #population without high school diploma
    #unemployment
    #percentages for each

class MyCensusTractList:
    def __init__(self, censusTractArray):
        self.censusTractArray = list(censusTractArray)
        self.totalPopulation = 0
        self.totalOlderAdults65Plus = 0
        self.percentageOlderAdults65Plus = 0
        self.totalOlderAdults55Plus = 0
        self.percentageOlderAdults55Plus = 0
        self.totalOlderAdults65PlusKnownPovertyStatus = 0
        self.povertyOlderAdults65Plus = 0
        self.povertyPercentageOlderAdults65Plus = 0
        self.totalAge65PlusHouseholders = 0
        self.livingAloneAge65PlusHouseholders = 0
        self.livingAlonePercentageAge65PlusHouseholders = 0

        self.totalPopulation5Plus = 0
        self.limitedEnglishTotalPopulation5Plus = 0
        self.limitedEnglishPercentagePopulation5Plus = 0
        self.povertyPopulation = 0
        self.povertyPercentage = 0
        self.totalPopulation25Plus = 0
        self.noHighSchoolTotalPopulation25Plus = 0
        self.noHighSchoolPercentagePopulation25Plus = 0
        self.totalLaborForce = 0
        self.unemployedLaborForce = 0
        self.unemploymentPercentage = 0

        self.fillOlderAdultValues() #initialize statistics describing the older adult population

    def fillOlderAdultValues(self):
        for censusTract in self.censusTractArray:
            self.totalPopulation += censusTract.totalPopulation
            self.totalOlderAdults65Plus += censusTract.totalOlderAdults65Plus
            self.totalOlderAdults55Plus += censusTract.totalOlderAdults55Plus
            self.totalOlderAdults65PlusKnownPovertyStatus += censusTract.totalOlderAdults65PlusKnownPovertyStatus
            self.povertyOlderAdults65Plus += censusTract.povertyOlderAdults65Plus
            self.totalAge65PlusHouseholders += censusTract.totalAge65PlusHouseholders
            self.livingAloneAge65PlusHouseholders += censusTract.livingAloneAge65PlusHouseholders
            self.totalPopulation5Plus += censusTract.totalPopulation5Plus
            self.limitedEnglishTotalPopulation5Plus += censusTract.limitedEnglishTotalPopulation5Plus
        self.percentageOlderAdults65Plus = self.totalOlderAdults65Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        self.percentageOlderAdults55Plus = self.totalOlderAdults55Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        self.povertyPercentageOlderAdults65Plus = self.povertyOlderAdults65Plus / self.totalOlderAdults65PlusKnownPovertyStatus * 100 #save this value as a number in the range of 0-100  
        self.livingAlonePercentageAge65PlusHouseholders = self.livingAloneAge65PlusHouseholders / self.totalAge65PlusHouseholders * 100 #save this value as a number in the range of 0-100


def createCensusTractArray(censusTractFileName):
    censusTractArray = []
    with open(censusTractFileName, encoding = 'utf-8') as inputFile:
        for censusTract in inputFile: #for each ZIP code in the input file
            censusTractNum = int(censusTract) #this line removes the line break in the ZIP code
            censusTractString = str(censusTractNum) #convert to a string
            print("Retrieving data for Census Tract " + censusTractString + "...")
            censusTractArray.append(MyCensusTract(censusTractString))
    return censusTractArray


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

NYCHACensusTractsAnalysis = MyCensusTractList(createCensusTractArray("NYCHAQueensCensusTracts.txt"))
#print("Older Adult Statistics for Given Census Tracts: ")
#for censusTract in NYCHACensusTractList:
#    print("Census Tract Number: " + censusTract.censusTractNum)
#    print("Total Population: " + str(censusTract.totalPopulation))
#    print("Total Number of Older Adults Age 65+: " + str(censusTract.totalOlderAdults65Plus))
#    print("Percentage Population Who Are Older Adults 65+: " + str(censusTract.percentageOlderAdults65Plus))
#    print("Total Number of Older Adults Age 55+: " + str(censusTract.totalOlderAdults55Plus))
#    print("Percentage Population Who Are Older Adults 55+: " + str(censusTract.percentageOlderAdults55Plus))
#    print("Total Number of Older Adults Age 65+ with Known Poverty Status: " + str(censusTract.totalOlderAdults65PlusKnownPovertyStatus))
#    print("Total Number of Older Adults Age 65+ with Income Below the Poverty Line: " + str(censusTract.povertyOlderAdults65Plus))
#    print("Percentage of Older Adults Age 65+ Who Are Poor: " + str(censusTract.povertyPercentageOlderAdults65Plus))
#    print("Total Number of Age 65+ Householders: " + str(censusTract.totalAge65PlusHouseholders))
#    print("Total Number of Age 65+ Householders Who Live Alone: " + str(censusTract.livingAloneAge65PlusHouseholders))
#    print("Percentage of Age 65+ Householders Who Live Alone: " + str(censusTract.livingAlonePercentageAge65PlusHouseholders))
print("Overall Descriptive Statistics for Given Census Tracts:")
print("Percentage of Older Adults 65+: " + str(NYCHACensusTractsAnalysis.percentageOlderAdults65Plus))
print("Percentage of Older Adults 55+: " + str(NYCHACensusTractsAnalysis.percentageOlderAdults55Plus))
print("Percentage of Older Adults 65+ Who Live Below the Poverty Line: " + str(NYCHACensusTractsAnalysis.povertyPercentageOlderAdults65Plus))
print("Percentage of Age 65+ Householders Who Live Alone: " + str(NYCHACensusTractsAnalysis.livingAlonePercentageAge65PlusHouseholders))

#Older Adult Statistics
#TO-DO:
# implement censusTract class -- COMPLETED for older adults statistics. Need to implement community needs statistics
# create an array of census tracts based on input from a file containing a list of census tracts to look up
# create a census tract instance that stores summary data about the array of census tracts
# output the summary data to the screen
# output the array data to a file to create an audit trail