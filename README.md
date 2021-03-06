# covid19_streetview

Ethan Frier - ethan.frier@colorado.edu

Streetview Covid19 Visualizer

ATLS 1300-5650 Final Project

December 2020


The script covid_streetview.py downloads streetview images from google maps 
static street view API based on location data from the New York Times Covid19 
github repo.

Humans respond more effectively to emotion as compared to information. In fact
too much information, regardless of quality or source, can sometimes have an
adverse effect. The goal of this project is to put these data into context.
By displaying a limited amount of high quality current data in a more human 
context, the hope is that this piece will make these data more digestible.

The most recent US covid data by county is retrieved from the New York Times
repo - https://github.com/nytimes/covid-19-data . The data is then sorted by
the total number of cases by county and outputs today's top counties to a list.
Each list index contains a text string of 'County,State'. In order to best
communicate with the streetview api this data is converted to latitude and longitude
coordinates using the geopy library. Using these coordinates the StreetView 
class generates an API request and downloads images from those top counties.

The NYTCovidData class was modified from TowardsDataScience.com
https://towardsdatascience.com/analyze-ny-times-covid-19-dataset-86c802164210
I copied and modified the methods: today(), updateCounty(), dateUpdate(),
process(), as well as 5 lines from _init_().

Future Improvements:
    
The top counties by raw case numbers are invariably almost all large cities.
I would like to modify this script further to sort by the highest number of
cases per capita. This will return the case rate, not the total number of cases.
The rate is a more effective way of looking at the velocity and impact of the
virus, and more accurately highlights the effect on less populous areas, which
are currently the hardest hit. This requires a dataset with each county's
population to compare total cases against. I'm not sure where to find best
or cleanest data for 1,929 counties, or if I should use the FIPS system?

The images are just downloaded to a pre-existing generic folder. I want to
add a method to create a new folder for each date. This folder will contain
the images, as well as a csv file generated by the method containing the
original 'County,State' string, the new 'lat,lon' string, as well as the
address text string generated by geopy and additional covid data for each day.

Eventually, I would like to make this into a live viewer of the images which
will display on screen a tiled montage of the images from the top counties by
case rate, with the address text and current covid data overlaid. The speed at
which the images update will be relative to the current national caseload.