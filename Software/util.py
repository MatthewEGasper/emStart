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

from astropy.coordinates import AltAz, EarthLocation, get_sun, SkyCoord
from astropy.time import Time, TimeDelta
from timezonefinder import TimezoneFinder
import astropy.units as u
import pytz
import time

class emulator():
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
		self.ground = EarthLocation(
			lon = args.longitude[0]*u.deg,
			lat = args.latitude[0]*u.deg,
			height = args.elevation[0]*u.m)
		
		self.timezone = self.GetTimezone(self.ground)
		if(self.timezone == False):
			self.timezone = "not available"

		self.time = Time(args.date[0] + " " + args.time[0])
		self.delta = TimeDelta(args.duration[0], format='sec')

		# Display the input information after processing
		print()
		print("===== Ground Station =============================")
		print("Latitude \t" + str(round(self.ground.lat.degree, 5)))
		print("Longitude\t" + str(round(self.ground.lon.degree, 5)))
		print("Timezone \t" + str(self.timezone))
		print()
		print("===== Emulation Information ======================")
		print("Starting\t" + str(self.time) + " UTC")
		print("Ending  \t" + str(self.time+self.delta) + " UTC")
		print("Duration\t" + str(self.delta) + " seconds (" + str(round(self.delta.to_value('hr'), 2)) + " hours)")
		print()

		self.emTime = self.time

		try:
			self.speed = args.speed[0]
		except:
			self.speed = 1.0

	def GetAltAz(self):
		self.target = get_sun(self.emTime)
		self.timeframe = AltAz(
			obstime = self.emTime,
			location = self.ground)
		self.altaz = self.target.transform_to(self.timeframe)

	def PrintAltAz(self):
		print("Time    \t" + str(self.emTime) + " UTC")
		print("Altitude\t" + str(self.altaz.alt.degree) + " degrees")
		print("Azimuth \t" + str(self.altaz.az.degree) + " degrees")
		# print("Distance \t" + str(self.altaz.distance))
		print()

	def Advance(self):
		if(self.speed > 0):
			time.sleep(1/self.speed)
		self.emTime = self.emTime + 1*u.second

	def IsComplete(self):
		if(str(self.emTime) == str(self.time + self.delta)):
			return(True)
		else:
			return(False)
	
	def Run(self):
		print("===== BEGIN EMULATION ============================")
		while(self.IsComplete() == False):
			self.GetAltAz()
			self.PrintAltAz()
			self.Advance()
		print("===== FINAL POSITION =============================")
		self.GetAltAz()
		self.PrintAltAz()