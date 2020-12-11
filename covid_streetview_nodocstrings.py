#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:37:25 2020
@author: ethanfrier
covid_streetview.py with no docstrings
"""

import urllib
import os
import pandas
import requests 
import io
import time
import datetime
import geopy
from geopy.geocoders import Nominatim


class NYTCovidData:
   
    def __init__(self):
        from datetime import date
        self.NYTcountiesData = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        self._today = date.today()
        self.numCounties = 20
        self.topCounties = []
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
        self.localFolder = '/Users/ethanfrier/Desktop/covid19_streetview/downloadImages/'

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
            locationText = convertLocation.address 
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
                self.getStreetView(lat, lon, heading, self.filename, self.localFolder)  
                
                print(f'   Got {self.filename}')      
                self.numImages += 1      
            
            self.numLocations += 1
               
            
if __name__ == "__main__":
    covid = NYTCovidData()
    streetView = StreetView()

    streetView.getKey()

    covid.today()
    covid.updateCounty()
    covid.dateUpdate()

    covid.process()
    covid.sortByCases()
    covid.getTopCounties()
        
    streetView.makeLatLon()      
    streetView.execute()
    
    print('')
    print(f'Processed {str(streetView.numImages)} images.')
    print('Done.')


