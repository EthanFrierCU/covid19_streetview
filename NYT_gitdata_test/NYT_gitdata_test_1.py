#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ethanfrier
Streetview Covid19 Visualizer
ATLS 1300-5650 Final Project 

This script retrieves the most recent US covid data by county from the New York
Times covid github repository. It then sorts by the total number of cases by 
county, and outputs today's top 12 counties to a list. The top counties are 
invariably large cities, so this data is not as interesting as it would seem.

I would like to modify it further to sort by the highest number of cases 
per capita. This will show the case rate, not the total number of cases. The 
rate is a more effective way of looking at the velocity and impact of the
virus, and more accurately highlights the effect on less populous areas, which 
are currently the hardest hit. This requires a dataset with each county's 
population to compare total cases against. I'm not sure where to find best 
or cleanest data for 1,929 counties, or if I should use the FIPS system?
 
NYTCovid class is modified from: https://github.com/tirthajyoti/Covid-19-analysis/blob/master/Notebook/NYTCovid.py
The methods updateCounty(), dateUpdate(), process() were copied - 24 lines total

"""
import pandas as pd
import requests 
import io
import time
import datetime


class NYTCovid:
    def __init__(self):
        from datetime import date
        self.numCounties = 12
        self.topCounties = []
        self.countydf = None
        self._countyupdated = False
        self._processed = False
        self._sorted = False
        self._today = date.today()
    
    
    def today(self):
        print("Today's date is: ",self._today)
        
        
    def updateCounty(self, url="https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"):
        '''
        Retrieves most recent data from New York Times Covid19 github repository. 
        Stores data in self.countydf panda data frame. 
        '''
        url = url
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
        new cases and new deaths using teh difference in numbers by day in 
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
                location_ = (county_, state_)
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




