#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:59:30 2020
@author: Ethan Frier

This program downloads street view images from google maps static street view 
api based on latitude and longitude data from a csv file. The images as saved 
to a local folder in same directory as this script. 
"""

import csv, urllib, os


# store data from CSV file in a list called locations
locations = []


# read the data from the CSV file 
with open('testLocations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    print(f'Opened CSV file: {csv_file.name}')
    
    line_count = 0
    
    # read the csv file and store data in a list 
    for row in csv_reader:
        # skip row 0 of the CSV - fields should be column titles
        if line_count == 0:
            print(f'Column0: {row[0]}    , Column1: {row[1]}')
            line_count += 1   
            
        # store the latitude and longitude data as list of tuples 
        else:
            lat = float(row[0])
            lon = float(row[1])
            location = (lat, lon)
            locations.append(location)
            print(f'{str(line_count).zfill(3)}  {row[0]}, {row[1]}')
            line_count += 1 
            
    print(f'Ready to process {str(len(locations))} locations.')


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

