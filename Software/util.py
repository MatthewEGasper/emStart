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

from astropy.coordinates import EarthLocation
from astropy.time import Time, TimeDelta
from timezonefinder import TimezoneFinder
import astropy.units as u
import pytz

class util():
	def __init__(self):
		return(None)

	# Get the timezone at the specified location
	def GetTimezone(self, loc):
		tz = TimezoneFinder().timezone_at(
			lat = loc.lat.degree,
			lng = loc.lon.degree)
		
		if tz is None:
			print("Could not determine the time zone at the specified coordinates!")
			return(False)
		else:
			return(pytz.timezone(tz))

	def ProcessArgs(self, args):
		self.ground = EarthLocation(args.latitude[0]*u.deg, args.longitude[0]*u.deg, args.elevation[0]*u.m)
		
		self.timezone = self.GetTimezone(self.ground)
		if(self.timezone == False):
			self.timezone = "not available"

		self.time = Time(args.date[0] + " " + args.time[0])
		self.delta = TimeDelta(args.duration[0], format='sec')

		# Display the input information after processing
		print()
		print("The ground station timezone is " + str(self.timezone))
		print()
		print("========== Emulation Information ==========")
		print("Starting at     " + str(self.time) + " UTC")
		print("Ending at       " + str(self.time+self.delta) + " UTC")
		print("Duration of     " + str(self.delta) + " seconds")
		print()