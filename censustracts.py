#This Python module contains code to retrieve American Community Survey and CDC 500 Cities data at the census tract level

#ensure that sodapy is installed before running

import requests
import json
from sodapy import Socrata

class MyCensusTract: #this class of objects retrieves and stores data for a given census tract
    def __init__(self, QueensCountyCensusTractNum):
        self.censusTractNum = QueensCountyCensusTractNum
        self.year = "17" #this refers to the American Community Survey yearly 5-year estimate dataset to use. We are using 2017 ("17") as the default.
        self.totalPopulation = 0

        #statistics describing the older adult population
        self.totalOlderAdults65Plus = 0
        self.percentageOlderAdults65Plus = 0
        self.totalOlderAdults55Plus = 0
        self.percentageOlderAdults55Plus = 0
        self.totalOlderAdults65PlusKnownPovertyStatus = 0
        self.povertyOlderAdults65Plus = 0
        self.povertyPercentageOlderAdults65Plus = 0
        self.livingAloneAge65PlusHouseholders = 0
        self.livingAlonePercentageAge65PlusHouseholders = 0
        self.totalMales65Plus = 0
        self.totalFemales65Plus = 0
        self.totalOlderAdults50To74 = 0
        self.totalFemales50To74 = 0

        #statistics describing overall community needs
        self.totalPopulation5Plus = 0
        self.limitedEnglishTotalPopulation5Plus = 0
        self.limitedEnglishPercentagePopulation5Plus = 0
        self.populationWithKnownPovertyStatus = 0
        self.povertyNum = 0
        self.povertyPercentage = 0
        self.totalPopulation25Plus = 0
        self.noHighSchoolTotalPopulation25Plus = 0
        self.noHighSchoolPercentagePopulation25Plus = 0
        self.totalLaborForce = 0 
        self.unemployedLaborForce = 0.0 #this number has to be handled as a float because I can't seem to find whole numbers in the American Community Survey dataset
        self.unemploymentPercentage = 0     

        #statistics describing community health needs. This data is from the CDC's 2016 BRFSS (Behavioral Risk Factor Surveillance System).
        #TO-DO:
        # 1. Implement all health statistics, not just for those related to older adults. https://chronicdata.cdc.gov/500-Cities/500-Cities-Census-Tract-level-Data-GIS-Friendly-Fo/k86t-wghb
        # 2. Implement percentages for older adult stats. I will need American Census Bureau data for the total females age 50-74, total adults age 50-74, total males age 65+, and total females age 65+
        self.coreMenCrudePrev = 0.0 #Model-based estimate for crude prevalence of older adult men aged >=65 years who are up to date on a core set of clinical preventive services: Flu shot past year, PPV shot ever, Colorectal cancer screening, 2016
        self.coreMenPercentage = 0 
        self.coreWomenCrudePrev = 0.0 #Model-based estimate for crude prevalence of older adult women aged >=65 years who are up to date on a core set of clinical preventive services: Flu shot past year, PPV shot ever, Colorectal cancer screening, and Mammogram past 2 years, 2016
        self.coreWomenPercentage = 0
        self.colonScreenCrudePrev = 0.0 #Model-based estimate for crude prevalence of fecal occult blood test, sigmoidoscopy, or colonoscopy among adults aged 50–75 years, 2016
        self.colonScreenPercentage = 0
        self.mammoUseCrudePrev = 0.0 #Model-based estimate for crude prevalence of mammography use among women aged 50–74 years, 2016
        self.mammoUsePercentage = 0.0
        self.teethLostCrudePrev = 0.0 #Model-based estimate for crude prevalence of all teeth lost among adults aged >=65 years, 2016
        self.teethLostPercentage = 0
        #Geolocation information
        self.geolocation = "" #Latitude, longitude of census tract centroid

        #initialization functions
        self.fillOlderAdultValues() #initialize statistics describing the older adult population
        self.fillCommunityNeedsProfile() #initialize statistics describing community needs
        self.fillCDC500CitiesData() #initialize statistics describing community health data

    def setYear(self,year): #this function changes which American Community Community yearly dataset to use
        self.year = year

    def fillOlderAdultValues(self):    
        jsonText = getACS5YearJSONByCensusTract(self.year,"S0101",self.censusTractNum) #S0101 refers to the American Community Survey dataset for age and sex

        self.totalPopulation = jsonText["data"]["rows"][0]["cells"]["C1"]["value"] #total population: table key = C1
        self.totalOlderAdults65Plus = jsonText["data"]["rows"][0]["cells"]["C349"]["value"] #older adults age 65+: table key = C349
        self.percentageOlderAdults65Plus = self.totalOlderAdults65Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        populationAge55To59 = jsonText["data"]["rows"][0]["cells"]["C145"]["value"] #older adults age 55-59: table key = C145
        populationAge60To64 = jsonText["data"]["rows"][0]["cells"]["C157"]["value"] #older adults age 60-64: table key = C157
        self.totalOlderAdults55Plus = populationAge55To59 + populationAge60To64 + self.totalOlderAdults65Plus 
        self.percentageOlderAdults55Plus = self.totalOlderAdults55Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        populationAge50To54 = jsonText["data"]["rows"][0]["cells"]["C133"]["value"] #older adults age 50-54: table key = C133
        populationAge65To69 = jsonText["data"]["rows"][0]["cells"]["C169"]["value"] #older adults age 65-69: table key = C169
        populationAge70To74 = jsonText["data"]["rows"][0]["cells"]["C181"]["value"] #older adults age 70-74: table key = C181
        self.totalOlderAdults50To74 = populationAge50To54 + populationAge55To59 + populationAge60To64 + populationAge65To69 + populationAge70To74
        self.totalMales65Plus = jsonText["data"]["rows"][0]["cells"]["C353"]["value"] #older males 65+: table key = C353
        self.totalFemales65Plus = jsonText["data"]["rows"][0]["cells"]["C357"]["value"] #older females 65+: table key = C353
        femalePopulationAge50To54 = jsonText["data"]["rows"][0]["cells"]["C141"]["value"] #females age 50-54: table key = C141
        femalePopulationAge55To59 = jsonText["data"]["rows"][0]["cells"]["C153"]["value"] #females age 55-59: table key = C153
        femalePopulationAge60To64 = jsonText["data"]["rows"][0]["cells"]["C165"]["value"] #females age 60-64: table key = C165
        femalePopulationAge65To69 = jsonText["data"]["rows"][0]["cells"]["C177"]["value"] #females age 65-69: table key = C177
        femalePopulationAge70To44 = jsonText["data"]["rows"][0]["cells"]["C189"]["value"] #females age 70-74: table key = C189
        self.totalFemales50To74 = femalePopulationAge50To54 + femalePopulationAge55To59 + femalePopulationAge60To64 + femalePopulationAge65To69 + femalePopulationAge70To44
        self.coreMenPercentage = self.coreMenCrudePrev / self.totalMales65Plus * 100 #save this value as a number in the range of 0-100
        self.coreWomenPercentage = self.coreWomenCrudePrev / self.totalFemales65Plus * 100 #save this value as a number in the range of 0-100
        self.colonScreenPercentage = self.colonScreenCrudePrev / self.totalOlderAdults50To74 * 100 #save this value as a number in the range of 0-100
        self.teethLostPercentage = self.teethLostCrudePrev / self.totalOlderAdults65Plus * 100 #save this value as a number in the range of 0-100

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
        totalLivingAloneMaleHouseholders65Plus = jsonText["data"]["rows"][0]["cells"]["B11010_5_EST"]["value"] #total male householders age 65+ who live alone
        totalLivingAloneFemaleHouseholders65Plus = jsonText["data"]["rows"][0]["cells"]["B11010_12_EST"]["value"] #total female householders age 65+ who live alone
        self.livingAloneAge65PlusHouseholders = totalLivingAloneMaleHouseholders65Plus + totalLivingAloneFemaleHouseholders65Plus #total householders age 65+ who live alone
        self.livingAlonePercentageAge65PlusHouseholders = self.livingAloneAge65PlusHouseholders / self.totalOlderAdults65Plus * 100 #this yields the percentage of older adults who live alone. Save this value as a number in the range of 0-100

    def fillCommunityNeedsProfile(self):
        jsonText = getACS5YearJSONByCensusTract(self.year,"S2301",self.censusTractNum) #S2301 refers to the American Community Survey dataset for employment and labor force statistics
        self.totalLaborForce = jsonText["data"]["rows"][0]["cells"]["C1"]["value"] #C1 key refers to the total population 16 years and over
        self.unemploymentPercentage = jsonText["data"]["rows"][0]["cells"]["C7"]["value"] #C7 key refers to the unemployment rate for the population 16 years and over
        self.unemployedLaborForce = self.totalLaborForce * (self.unemploymentPercentage / 100)

        jsonText = getACS5YearJSONByCensusTract(self.year,"S1501",self.censusTractNum) #S1501 refers to the American Community Survey dataset for educational attainment
        self.totalPopulation25Plus = jsonText["data"]["rows"][0]["cells"]["C61"]["value"] #C61 key refers to the total population 25 years and over
        pop25PlusLessThan9thGrade = jsonText["data"]["rows"][0]["cells"]["C73"]["value"] #C73 key refers to the population 25 years and over that attained less than a 9th grade education
        pop25Plus9thTo12thGradeNoDiploma = jsonText["data"]["rows"][0]["cells"]["C85"]["value"] #C85 key refers to the population 25 years and over that attained a 9th-12th grade education but did not earn a HS diploma or its equivalency
        self.noHighSchoolTotalPopulation25Plus = pop25PlusLessThan9thGrade + pop25Plus9thTo12thGradeNoDiploma
        self.noHighSchoolPercentagePopulation25Plus = self.noHighSchoolTotalPopulation25Plus / self.totalPopulation25Plus * 100 #save this value as a number in the range of 0-100

        jsonText = getACS5YearJSONByCensusTract(self.year,"S1701",self.censusTractNum) #S1501 refers to the American Community Survey dataset for poverty
        self.populationWithKnownPovertyStatus = jsonText["data"]["rows"][0]["cells"]["C1"]["value"] #C1 key refers to the population for whom poverty status is determined
        self.povertyNum = jsonText["data"]["rows"][0]["cells"]["C3"]["value"] #C3 key refers to the population who are below poverty level
        self.povertyPercentage = self.povertyNum / self.populationWithKnownPovertyStatus * 100 #save this value as a number in the range of 0-100

        jsonText = getACS5YearJSONByCensusTract(self.year,"DP02",self.censusTractNum) #DP02 refers to the American Community Survey dataset called "Selected Social Characteristics in the United States"
        self.totalPopulation5Plus = jsonText["data"]["rows"][0]["cells"]["C398"]["value"] #C398 refers to the total population age 5 and older
        self.limitedEnglishTotalPopulation5Plus = jsonText["data"]["rows"][0]["cells"]["C409"]["value"] #C409 refers to the population age 5 and older who (1) speak a language other than English and (2) speak English less than very well
        self.limitedEnglishPercentagePopulation5Plus = self.limitedEnglishTotalPopulation5Plus / self.totalPopulation5Plus * 100 #save this value as a number in the range of 0-100

    def fillCDC500CitiesData(self):
        client = Socrata("chronicdata.cdc.gov", 'QoQet97KEDYpMW4x4Manaflkp') #My (John Pham's) access token is QoQet97KEDYpMW4x4Manaflkp
        jsonText = client.get("47z2-4wuh", where="starts_with(place_tractid,'3651000-36081')", content_type="json", order="place_tractid ASC",limit=1000) #Get all Queens County census tracts
        client.close()
        for censusTract in jsonText:
            if censusTract["tractfips"] == self.censusTractNum:
                self.coreMenCrudePrev = float(censusTract["corem_crudeprev"]) #Model-based estimate for crude prevalence of older adult men aged >=65 years who are up to date on a core set of clinical preventive services: Flu shot past year, PPV shot ever, Colorectal cancer screening, 2016
                self.coreWomenCrudePrev = float(censusTract["corew_crudeprev"]) #Model-based estimate for crude prevalence of older adult women aged >=65 years who are up to date on a core set of clinical preventive services: Flu shot past year, PPV shot ever, Colorectal cancer screening, and Mammogram past 2 years, 2016
                self.colonScreenCrudePrev = float(censusTract["colon_screen_crudeprev"]) #Model-based estimate for crude prevalence of fecal occult blood test, sigmoidoscopy, or colonoscopy among adults aged 50–75 years, 2016
                self.mammoUseCrudePrev = float(censusTract["mammouse_crudeprev"]) #Model-based estimate for crude prevalence of mammography use among women aged 50–74 years, 2016
                self.teethLostCrudePrev = float(censusTract["teethlost_crudeprev"]) #Model-based estimate for crude prevalence of all teeth lost among adults aged >=65 years, 2016
                self.geolocation = censusTract["geolocation"] #Latitude, longitude of census tract centroid
                self.coreMenPercentage = self.coreMenCrudePrev / self.totalMales65Plus * 100 #save this value as a number in the range of 0-100
                self.coreWomenPercentage = self.coreWomenCrudePrev / self.totalFemales65Plus * 100 #save this value as a number in the range of 0-100
                self.mammoUsePercentage = self.mammoUseCrudePrev / self.totalFemales50To74 * 100 #save this value as a number in the range of 0-100
                self.colonScreenPercentage = self.colonScreenCrudePrev / self.totalOlderAdults50To74 * 100 #save this value as a number in the range of 0-100
                self.teethLostPercentage = self.teethLostCrudePrev / self.totalOlderAdults65Plus * 100 #save this value as a number in the range of 0-100


class MyCensusTractList:
    def __init__(self, censusTractArray):
        self.censusTractArray = list(censusTractArray)
        self.censusTracyArrayLength = len(self.censusTractArray)
        self.totalPopulation = 0

        #statistics describing the older adult population
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
        self.totalMales65Plus = 0
        self.totalFemales65Plus = 0
        self.totalOlderAdults50To74 = 0
        self.totalFemales50To74 = 0

        #statistics describing overall community needs
        self.totalPopulation5Plus = 0
        self.limitedEnglishTotalPopulation5Plus = 0
        self.limitedEnglishPercentagePopulation5Plus = 0
        self.populationWithKnownPovertyStatus = 0
        self.povertyNum = 0
        self.povertyPercentage = 0
        self.totalPopulation25Plus = 0
        self.noHighSchoolTotalPopulation25Plus = 0
        self.noHighSchoolPercentagePopulation25Plus = 0
        self.totalLaborForce = 0 
        self.unemployedLaborForce = 0.0 #this number has to be handled as a float because I can't seem to find whole numbers in the American Community Survey dataset
        self.unemploymentPercentage = 0

        #statistics describing community health needs
        #TO-DO:
        # 1. Implement all health statistics, not just for those related to older adults. https://chronicdata.cdc.gov/500-Cities/500-Cities-Census-Tract-level-Data-GIS-Friendly-Fo/k86t-wghb
        # 2. Implement percentages for older adult stats. I will need American Census Bureau data for the total females age 50-74, total adults age 50-74, total males age 65+, and total females age 65+
        self.coreMenCrudePrev = 0.0 #Model-based estimate for crude prevalence of older adult men aged >=65 years who are up to date on a core set of clinical preventive services: Flu shot past year, PPV shot ever, Colorectal cancer screening, 2016
        self.coreMenPercentage = 0.0
        self.coreWomenCrudePrev = 0.0 #Model-based estimate for crude prevalence of older adult women aged >=65 years who are up to date on a core set of clinical preventive services: Flu shot past year, PPV shot ever, Colorectal cancer screening, and Mammogram past 2 years, 2016
        self.coreWomenPercentage = 0.0
        self.colonScreenCrudePrev = 0.0 #Model-based estimate for crude prevalence of fecal occult blood test, sigmoidoscopy, or colonoscopy among adults aged 50–75 years, 2016
        self.colonScreenPercentage = 0.0
        self.mammoUseCrudePrev = 0.0 #Model-based estimate for crude prevalence of mammography use among women aged 50–74 years, 2016
        self.mammoUsePercentage = 0.0
        self.teethLostCrudePrev = 0.0 #Model-based estimate for crude prevalence of all teeth lost among adults aged >=65 years, 2016
        self.teethLostPercentage = 0.0

        self.fillValues() #initialize statistics

    def fillValues(self):
        for censusTract in self.censusTractArray:
            self.totalPopulation += censusTract.totalPopulation
            self.totalOlderAdults65Plus += censusTract.totalOlderAdults65Plus
            self.totalOlderAdults55Plus += censusTract.totalOlderAdults55Plus
            self.totalOlderAdults65PlusKnownPovertyStatus += censusTract.totalOlderAdults65PlusKnownPovertyStatus
            self.povertyOlderAdults65Plus += censusTract.povertyOlderAdults65Plus
            self.livingAloneAge65PlusHouseholders += censusTract.livingAloneAge65PlusHouseholders
            self.totalPopulation5Plus += censusTract.totalPopulation5Plus
            self.limitedEnglishTotalPopulation5Plus += censusTract.limitedEnglishTotalPopulation5Plus
            self.populationWithKnownPovertyStatus += censusTract.populationWithKnownPovertyStatus
            self.povertyNum += censusTract.povertyNum
            self.totalPopulation25Plus += censusTract.totalPopulation25Plus
            self.noHighSchoolTotalPopulation25Plus += censusTract.noHighSchoolTotalPopulation25Plus
            self.totalLaborForce += censusTract.totalLaborForce
            self.unemployedLaborForce += censusTract.unemployedLaborForce
            self.coreMenCrudePrev += censusTract.coreMenCrudePrev
            self.coreWomenCrudePrev += censusTract.coreWomenCrudePrev
            self.colonScreenCrudePrev += censusTract.colonScreenCrudePrev
            self.mammoUseCrudePrev += censusTract.mammoUseCrudePrev
            self.teethLostCrudePrev += censusTract.teethLostCrudePrev
            self.totalMales65Plus += censusTract.totalMales65Plus
            self.totalFemales65Plus += censusTract.totalFemales65Plus
            self.totalOlderAdults50To74 += censusTract.totalOlderAdults50To74
            self.totalFemales50To74 += censusTract.totalFemales50To74
        self.percentageOlderAdults65Plus = self.totalOlderAdults65Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        self.percentageOlderAdults55Plus = self.totalOlderAdults55Plus / self.totalPopulation * 100 #save this value as a number in the range of 0-100
        self.povertyPercentageOlderAdults65Plus = self.povertyOlderAdults65Plus / self.totalOlderAdults65PlusKnownPovertyStatus * 100 #save this value as a number in the range of 0-100  
        self.livingAlonePercentageAge65PlusHouseholders = self.livingAloneAge65PlusHouseholders / self.totalOlderAdults65Plus * 100 #divide number of older adult householders living alone by total number of older adults in the census tract. Save this value as a number in the range of 0-100
        self.limitedEnglishPercentagePopulation5Plus = self.limitedEnglishTotalPopulation5Plus / self.totalPopulation5Plus * 100 #save this value as a number in the range of 0-100
        self.povertyPercentage = self.povertyNum / self.populationWithKnownPovertyStatus * 100 #save this value as a number in the range of 0-100
        self.noHighSchoolPercentagePopulation25Plus = self.noHighSchoolTotalPopulation25Plus / self.totalPopulation25Plus * 100 #save this value as a number in the range of 0-100
        self.unemploymentPercentage = self.unemployedLaborForce / self.totalLaborForce * 100 #save this value as a number in the range of 0-100
        self.coreMenPercentage = self.coreMenCrudePrev / self.totalMales65Plus * 100 #save this value as a number in the range of 0-100
        self.coreWomenPercentage = self.coreWomenCrudePrev / self.totalFemales65Plus * 100 #save this value as a number in the range of 0-100
        self.mammoUsePercentage = self.mammoUseCrudePrev / self.totalFemales50To74 * 100 #save this value as a number in the range of 0-100
        self.colonScreenPercentage = self.colonScreenCrudePrev / self.totalOlderAdults50To74 * 100 #save this value as a number in the range of 0-100
        self.teethLostPercentage = self.teethLostCrudePrev / self.totalOlderAdults65Plus * 100 #save this value as a number in the range of 0-100

    def exportValues(self, fileName): #export array data into a CSV file
        print("\nAttempting to export data to the file " + fileName + "...")
        try:
            with open(fileName, "w") as outputFile: #open the file for writing
                #output column headers
                outputFile.write("Census Tract Number, Total Population, Total Older Adults Age 65+, Percentage of Population Who Are Older Adults Age 65+, Total Older Adults Age 55+, Percentage of Population Who Are Older Adults Age 55+, Total Older Adults Age 65+ With Known Poverty Status, Older Adults Age 65+ Below Poverty Level, Percentage of Older Adults Age 65+ Below Poverty Level, Older Adults Age 65+ Living Alone, Percentage of Older Adults Age 65+ Living Alone, Total Population Age 5+, Residents Age 5+ with Limited English Proficiency, Percentage of Residents with Limited English Proficiency, Total Population with Known Poverty Status, Residents Below Poverty Level, Percentage of Residents Below Poverty Level, Total Population Age 25+, Residents Age 25+ without a High School Diploma or Equivalency, Percentage of Residents Age 25+ without a High School Diploma, Total Labor Force Age 16+, Unemployed Residents, Unemployment Rate, Number of Older Adult Men Age 65+ Who Are Up to Date on Core Set of Clinical Preventive Services, Percentage of Older Men Age 65+ Who Are Up to Date on Core Set of Clinical Preventive Services, Number of Older Adult Women Age 65+ Who Are Up to Date on Core Set of Clinical Preventive Services, Percentage of Older Women Age 65+ Who Are Up to Date on Core Set of Clinical Preventive Services, Older Adults Age 50-75 Fecal Occult Blood Test Sigmoidoscopy or Colonoscopy, Percentage of Older Adults Age 50-75 Fecal Occult Blood Test Sigmoidoscopy or Colonoscopy, Women Age 50-75 Mammogram Use, Percentage of Women Age 50-75 Mammogram Use, Older Adults Age 65+ With All Teeth Lost, Percentage of Older Adults Age 65+ With All Teeth Lost\n")
                #output row data
                for censusTract in self.censusTractArray:
                    outputFile.write(str(censusTract.censusTractNum) + "," + str(censusTract.totalPopulation) + "," + str(censusTract.totalOlderAdults65Plus) + "," + "{:.1f}".format(censusTract.percentageOlderAdults65Plus) + "," + str(censusTract.totalOlderAdults55Plus) + "," + "{:.1f}".format(censusTract.percentageOlderAdults55Plus) + "," + str(censusTract.totalOlderAdults65PlusKnownPovertyStatus) + "," + str(censusTract.povertyOlderAdults65Plus) + "," + "{:.1f}".format(censusTract.povertyPercentageOlderAdults65Plus) + "," + str(censusTract.livingAloneAge65PlusHouseholders) + "," + "{:.1f}".format(censusTract.livingAlonePercentageAge65PlusHouseholders) + "," + str(censusTract.totalPopulation5Plus) + "," + str(censusTract.limitedEnglishTotalPopulation5Plus) + "," + "{:.1f}".format(censusTract.limitedEnglishPercentagePopulation5Plus) + "," + str(censusTract.populationWithKnownPovertyStatus) + "," + str(censusTract.povertyNum) + "," + "{:.1f}".format(censusTract.povertyPercentage) + "," + str(censusTract.totalPopulation25Plus) + "," + str(censusTract.noHighSchoolTotalPopulation25Plus) + "," + "{:.1f}".format(censusTract.noHighSchoolPercentagePopulation25Plus) + "," + str(censusTract.totalLaborForce) + "," + "{:.1f}".format(censusTract.unemployedLaborForce) + "," + "{:.1f}".format(censusTract.unemploymentPercentage) + "," + str(censusTract.coreMenCrudePrev) + "," + "{:.1f}".format(censusTract.coreMenPercentage) + "," + str(censusTract.coreWomenCrudePrev) + "," + "{:.1f}".format(censusTract.coreWomenPercentage) + "," + str(censusTract.colonScreenCrudePrev) + "," + "{:.1f}".format(censusTract.colonScreenPercentage) + "," + str(censusTract.mammoUseCrudePrev) + "," + "{:.1f}".format(censusTract.mammoUsePercentage) + "," + str(censusTract.teethLostCrudePrev) + "," + "{:.1f}".format(censusTract.teethLostPercentage) + "\n")
        except IOError:
            print("Error writing to file " + fileName + ".")
        finally:
            print("Finished writing all data to the file " + fileName + ".")

def getACS5YearJSONByCensusTract(year, tableNumber, censusTract): #return JSON data from the American Community Survey (ACS) dataset given a year, ACS table number, and Queens County census tract number
    #build the URL string, given the parameters
    getUrl =    "http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/" + year + "_5YR/tables/" + tableNumber + "/data/1400000US" + censusTract
    parameters = {"maxResults":1, "key":"ea46e190165e1ee608d643fba987f8b3620ec1a9"} #parameters for the URL
    #https://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/S0101/data/1400000US36081002500?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9

    requestResult = requests.get(getUrl,params=parameters) #submit the GET request
    resultText = requestResult.text #obtain the requested text
    jsonText = json.loads(resultText) #convert the requested text to JSON format
    return jsonText

def createCensusTractArray(censusTractFileName):
    censusTractArray = []
    print("Searching for and retrieving census tracts listed in " + censusTractFileName + "...")
    with open(censusTractFileName, encoding = 'utf-8') as inputFile:
        for censusTract in inputFile: #for each ZIP code in the input file
            censusTractNum = int(censusTract) #this line removes the line break in the ZIP code
            censusTractString = str(censusTractNum) #convert to a string
            print("\tRetrieving data for Census Tract " + censusTractString + "...")
            censusTractArray.append(MyCensusTract(censusTractString))
    print("Done retrieving data for the " + str(len(censusTractArray)) + " census tract(s) that were found in the file.\n")
    return censusTractArray

def createCensusTractArray(censusTractFileName):
    censusTractArray = []
    print("Search for census tracts listed in " + censusTractFileName + "...")
    with open(censusTractFileName, encoding = 'utf-8') as inputFile:
        for censusTract in inputFile: #for each ZIP code in the input file
            censusTractNum = int(censusTract) #this line removes the line break in the ZIP code
            censusTractString = str(censusTractNum) #convert to a string
            print("\tRetrieving data for Census Tract " + censusTractString + "...")
            censusTractArray.append(MyCensusTract(censusTractString))
    print("Done retrieving data for the " + str(len(censusTractArray)) + " census tract(s) that were found in the file.\n")
    return censusTractArray