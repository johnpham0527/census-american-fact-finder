# README
# This Python script demonstrates how to access the Census Bureau's American Fact Finder website to find demographic and other information. I wrote this script to learn more about Python's request and json libraries and the American Fact Finder API

# TO-DOs
# Write a function that imports a list of Queens County ZIP Codes and outputs a file that contains various demographic information such as poverty rate

# This is my (John Pham's) API Access Key: ea46e190165e1ee608d643fba987f8b3620ec1a9

# See here for the American Fact Finder API Explorer: https://factfinder.census.gov/service/apps/api-explorer/#!/statisticalData/data?p.langId=en

# More information about geographic identifiers can be found here: https://factfinder.census.gov/service/GeographyIds.html
# Below is a sample reference list of geographic identifiers:
# 8600000US22039       = ZCTA5 22039
# 0500000US51059       = Fairfax County, Virginia
# 1400000US51059492000 = Census Tract 4920, Fairfax County, Virginia

import requests
import json

# Enter this URL into a web browser to explore data for Queens ZIP Code 11432: http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/8600000US11432?maxResults=10&key=ea46e190165e1ee608d643fba987f8b3620ec1a9

url = "http://factfinder.census.gov/service/data/v1/en/programs/ACS/datasets/17_5YR/tables/B01003/data/8600000US11432" #Prep the URL to obtain data from the American Community Survey Data 2017 5-Year Estimates for Fairfax County, VA
parameters = {"maxResults":"10", "key":"ea46e190165e1ee608d643fba987f8b3620ec1a9"} #This variable stores the parameters for the GET request

requestResult = requests.get(url,params=parameters) #submit the GET request to the Census Bureau American Fact Finder web server

#print(requestResult) #print the result of the request; used for troubleshooting a bad request

resultText = requestResult.text #obtain the requested text
jsonText = json.loads(resultText) #convert the requested text to JSON format
print(jsonText["data"]["rows"][0]["categories"]["GEO"]["label"]) #print out the county name
population = jsonText["data"]["rows"][0]["cells"]["B01003_1_EST"]["value"] #obtain the population estimate for the county
#print(population) #print out the population estimate as an integer
print(format(population,",")) #print out the population estimate, formatted with commas for readability