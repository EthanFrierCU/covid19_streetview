#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ethan Frier
Streetview Covid19 Visualizer
ATLS 1300-5650 Final Project
December 2020

"""

import requests 
import pandas
import io
from datetime import date
import time
import urllib
from geopy.geocoders import Nominatim
import os
import csv


class NYTCovidData:
   
    def __init__(self):
        self.NYTcountiesData = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        self._today = date.today()
        self.numCounties = 20
        self.topCounties = []
        self.topCases = []
        self.countydf = None
        self._countyupdated = False
        self._processed = False
        self._sorted = False
    
    def today(self):
        print("Today's date is: ",self._today)
              
    def updateCounty(self):
        url = self.NYTcountiesData
        s = requests.get(url).content
        self.countydf = pandas.read_csv(io.StringIO(s.decode('utf-8')))
        self.countydf['date'] =  pandas.to_datetime(self.countydf['date'], format='%Y-%m-%d')
        self._countyupdated = True
    
    def dateUpdate(self):
        if self._countyupdated:
            print("Most recent data:",self.countydf.iloc[-1]['date'].date())
        else:
            print("Data has not been updated!")
               
    def process(self):
        pandas.set_option('mode.chained_assignment', None)
        self.countydict= {}
        t1 = time.time()
        
        if self._countyupdated:
            self.countylist = list(self.countydf['county'].unique())
            print('')
            print(f'Processing {str(len(self.countylist))} counties...')
            
            for c in self.countylist:
                county_df=self.countydf[self.countydf['county']==c]
                county_df['newcases'] = county_df['cases'].diff()
                county_df['newdeaths'] = county_df['deaths'].diff()
                self.countydict[c]=county_df       
        
        self._processed = True
        t2 = time.time()
        delt = round(t2-t1,3)
        print("Finished. Took {} seconds".format(delt))
                    
    def sortByCases(self):
        if self._processed:
            self.countydf = self.countydf.sort_values(by=['date','cases'], ascending=False)
            self._sorted = True
            print('Sorted by recent number of cases per county.')
            print('')
        else:
            print('Not processed yet!')
                            
    def getTopCounties(self):
        if self._sorted:       
            for c in range(self.numCounties):
                county_ = self.countydf.iloc[c]['county']
                state_ = self.countydf.iloc[c]['state']
                location_ = str(f'{county_},{state_}')
                self.topCounties.append(location_)
            
            print(f'Top {covid.numCounties} counties by total cases:')
            for location in covid.topCounties:
                print(f'   {location}')
                
    def getTopCases(self):
        if self._sorted:       
            for c in range(self.numCounties):
                cases_ = self.countydf.iloc[c]['cases']
                self.topCases.append(cases_)


class StreetView:  
    
    def __init__(self):
        self.apiKey = ''
        self.locations = []
        self.headings = [0, 120, 240]    
        self.fov = 90               
        self.radius = 100000        
        self.size = '640x500'   
        self.filename = ''
        self.numImages = 0
        self.numLocations = 1
        # self.localFolder = '/Users/ethanfrier/Desktop/covid19_streetview/downloadImages/'

    def getKey(self):
        keyDoc = open('keys.txt', 'r')
        self.apiKey = keyDoc.read()
        printKeyA, printKeyB = self.apiKey[0:5],self.apiKey[-6:-1]
        print(f'Recieved API key: {printKeyA}xxxxxxxxxxxxxxxxxx{printKeyB}')
        print('')

    def getStreetView(self, lat_, lon_, heading_, fileName_, saveFolder_):
        base = r'https://maps.googleapis.com/maps/api/streetview?'
        imageSize = r'&size={}'.format(self.size) 
        imageLocation = r'&location={0},{1}'.format(lat_, lon_)
        imageHeading = r'&fov={0}&heading={1}'.format(self.fov, heading_)
        searchRadius = r'&radius={}'.format(self.radius)
        useKey = r'&key={}'.format(self.apiKey)
       
        myUrl = base + imageSize + imageLocation + imageHeading + searchRadius + useKey 
        urllib.request.urlretrieve(myUrl, os.path.join(saveFolder_,fileName_))
   
    def makeLatLon(self):
        geolocator = Nominatim(user_agent="covid_streetview")
        print('')
        print(f'Using geopy, converting {len(covid.topCounties)} locations:')
        
        for L in covid.topCounties:
            convertLocation = geolocator.geocode(L) 
            # locationText = convertLocation.address 
            latLon = (convertLocation.latitude,convertLocation.longitude)
            
            self.locations.append(latLon)
            print(f'   {latLon}')

    def execute(self):    
        print('')
        print('Downloading from Streetview static API:')
        
        for location in self.locations:
            for heading in self.headings:
                
                lat, lon = location    
                NYTlocation =  covid.topCounties[((self.numLocations)-1)].replace(" ","")
                
                self.filename = "{0}_{1}_{2}_({3},{4},h{5}).jpg".format(str(self.numLocations).zfill(3), covid._today, NYTlocation, lat, lon, heading)        
                self.getStreetView(lat, lon, heading, self.filename, go.todayPath)  
                
                print(f'   Got {self.filename}')      
                self.numImages += 1      
            
            self.numLocations += 1
               

class DailyDataManager:

    def __init__(self):
        self.todayPath = ''
        self.nameCSV = '_' + str(covid._today) + '_byTopCases.csv'
        self.nameFolder = str(covid._today)
        self.rootFolder =  os.getcwd()
        self.saveFolder = '/Users/ethanfrier/Desktop/covid19_streetview/dailyData/'

    def createFolder(self):
        self.todayPath = os.path.join(self.saveFolder, self.nameFolder)
        try:
            os.mkdir(self.todayPath)
            print('')
            print(f'New folder /dailyData/{self.nameFolder} created')
        except Exception:
            pass
            print('')
            print(f'Folder /dailyData/{self.nameFolder} already exists!')

    def createCSV(self):
        os.chdir(self.todayPath)
        with open(self.nameCSV,'w', newline='') as newCSV:
            CSVwriter = csv.writer(newCSV)  
            CSVwriter.writerow(['rank', 'cases', 'county', 'latLon'])
            for idx, data in enumerate(covid.topCounties):
                CSVwriter.writerow( [idx+1, covid.topCases[idx], data, geo.locations[idx]])
            print(f'Saved {self.nameCSV} to /{self.nameFolder}')
        os.chdir(self.rootFolder)
            
            
if __name__ == "__main__":
    covid = NYTCovidData()
    geo = StreetView()
    go = DailyDataManager()

    geo.getKey()
    covid.today()
    covid.updateCounty()
    covid.dateUpdate()

    covid.process()
    covid.sortByCases()
    covid.getTopCounties()
    covid.getTopCases()
    geo.makeLatLon()      
    
    go.createFolder()
    go.createCSV()
    
    geo.execute()
    
    print('')
    print(f'Processed {str(geo.numImages)} images.')
    print('Done.')




