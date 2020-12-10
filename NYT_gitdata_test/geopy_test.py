#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:15:23 2020

@author: ethanfrier
"""

import geopy

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="covid_streetview")

locations = ['New York, New York','Los Angeles,California','Cook,Illinois','Miami-Dade,Florida','Maricopa,Arizona','Harris,Texas']

for l in locations:
    convertLocation = geolocator.geocode(l)
    print(convertLocation.address)
    print((convertLocation.latitude,convertLocation.longitude))