#################################################
#                  _____ _             _   
#                 / ____| |           | |  
#   ___ _ __ ___ | (___ | |_ __ _ _ __| |_ 
#  / _ \ '_ ` _ \ \___ \| __/ _` | '__| __|
# |  __/ | | | | |____) | || (_| | |  | |_ 
#  \___|_| |_| |_|_____/ \__\__,_|_|   \__|
#
#################################################
# School:        Embry-Riddle Daytona Beach
# Engineer:      TJ Scherer
#
# Create Date:   10/1/2021
# Design Name:   util.py
# Project Name:  emStart Utilities
# Tool Versions: Python 3.9.7
# Description:   
#
# Dependencies:  
#
# Revision:      0.0
# Revision 0.0 - File Created
#
# Additional Comments: 
#
#################################################

import astropy.units as u
import pytz
from astropy.coordinates import EarthLocation
from astropy.time import Time
from datetime import datetime
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo

# Determine the position of the ground station
def GetEarthLocation(latitude, longitude, elevation):
	loc = EarthLocation(
		lat    = latitude,
		lon    = longitude,
		height = elevation)
	return(loc)

# Get the timezone at the specified location
def OffsetAt(latitude, longitude):
	tz = TimezoneFinder().timezone_at(
		lat = latitude,
		lng = longitude)
	if tz is None:
		print("Could not determine the time zone at the specified coordinates!")
		return(False)
	else:
		return(pytz.timezone(tz))

# Process the date and time
def GetAdjustedTime(loc, date, time):
	timezone = OffsetAt(loc.lat.degree, loc.lon.degree)
	utcoffset = timezone.utcoffset(None)
	if(utcoffset == None):
		utcoffset = 0
	time = Time(date + " " + time) + utcoffset
	return(time)