#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:59:30 2020
@author: Ethan Frier

This program downloads street view images from google maps static street view 
api based on latitude and longitude data from a csv file. The images as saved 
to a local folder in same directory as this script. 
"""

import csv
import urllib
import os
import pandas as pd
import requests 
import io
import time
import datetime
import geopy



# store data from CSV file in a list called locations
locations = []
NYTcountiesData = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

class NYTCovid:
    def __init__(self):
        from datetime import date
        self._today = date.today()
        self.numCounties = 12
        self.topCounties = []
        self.countydf = None
        self._countyupdated = False
        self._processed = False
        self._sorted = False
    
    
    def today(self):
        print("Today's date is: ",self._today)
        
        
    def updateCounty(self, url=NYTcountiesData):
        '''
        Retrieves most recent data from New York Times Covid19 github repository. 
        Stores data in self.countydf panda data frame. 
        '''
        url = NYTcountiesData
        s=requests.get(url).content
        self.countydf = pd.read_csv(io.StringIO(s.decode('utf-8')))
        self.countydf['date'] =  pd.to_datetime(self.countydf['date'], format='%Y-%m-%d')
        self._countyupdated = True
    
    
    def dateUpdate(self):
        '''
        Checks that updateCounty() has been run, then displays date of most
        recent data.
        '''
        if self._countyupdated:
            print("Most recent data:",self.countydf.iloc[-1]['date'].date())
        else:
            print("Data has not been updated!")
       
        
    def process(self):
        '''
        Creates a dictionary to store data from data frame countydf. Creates a
        list of all counties, and uses it to traverse countydf data. Calculates
        new cases and new deaths using the difference in numbers by day in 
        each county in the list. Usually takes 60-120 seconds to run. 
        '''
        pd.set_option('mode.chained_assignment', None)
        self.countydict= {}
        t1 = time.time()
        if self._countyupdated:
            self.countylist = list(self.countydf['county'].unique())
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
        '''
        Checks that process() has been run. Sorts counties by data, then total 
        cases in descending order.
        '''
        if self._processed:
            print('Sorted by recent number of cases per county.')
            self.countydf = self.countydf.sort_values(by=['date','cases'], ascending=False)
            self._sorted = True
                
            
    def getTopCounties(self):
        '''
        Stores sorted data into a list limited to numCounties and prints the 
        location (county,state) to the terminal.
        '''
        if self._sorted:       
            for c in range(self.numCounties):
                county_ = self.countydf.iloc[c]['county']
                state_ = self.countydf.iloc[c]['state']
                location_ = str(f'{county_},{state_}')
                self.topCounties.append(location_)
           
            print(f'Top {covid.numCounties} counties by total cases:')
            for location in covid.topCounties:
                print(location)
                
covid = NYTCovid()

covid.today()
covid.updateCounty()
covid.dateUpdate()

covid.process()
covid.sortByCases()
covid.getTopCounties()
         

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="covid_streetview")
# convertLocation = geolocator.geocode("175 5th Avenue NYC")

# variables for street view api and image processing
keyDoc = open('keys.txt', 'r')
apiKey = keyDoc.read()
print(apiKey)
localFolder = '/Users/ethanfrier/Desktop/covid19_streetview/streetview_test/downloadTest/'
curRow = 1
numImages = 0;
headings = [0, 90, 180, 270]
fov = 90


def getStreetView(lat_, lon_, heading_, fileName_, saveFolder_):
    '''This function creates a URL with parameters for each image, 
    and downloads image using streetview static api ''' 
    
    # assign parameters for image request
    base = r'https://maps.googleapis.com/maps/api/streetview?'
    imageSize = r'&size=640x500'    # max free size is 640x640
    imageLocation = r'&location={0},{1}'.format(lat_, lon_)
    imageHeading = r'&fov={0}&heading={1}'.format(fov, heading_)
    useAPI = r'&key={0}'.format(apiKey)
   
    # create URL, request image, and download to localFolder
    myUrl = base + imageSize + imageLocation + imageHeading + useAPI 
    urllib.request.urlretrieve(myUrl, os.path.join(saveFolder_,fileName_))
    
    
# for each location, format file and download street view image for each heading
for location in locations:
    for heading in headings:
        # extract the lat and lon data from tuple in list
        lat, lon = location
        
        # define file name for saved image
        filename = "{0}_{1}_lat{2}_lon{3}.jpg".format(str(curRow).zfill(3), heading, lat, lon,)
        
        # download street view images
        getStreetView(lat, lon, heading, filename, localFolder)  
        print(f'   Got {filename}')
        
        numImages += 1
        
    curRow += 1
    

    
# downloads complete, print number of images processes    
print(f'Processed {str(numImages)} images.')
print('Done.')

