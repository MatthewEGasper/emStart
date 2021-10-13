################################################################
#
# ███████╗███╗   ███╗███████╗████████╗ █████╗ ██████╗ ████████╗
# ██╔════╝████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
# █████╗  ██╔████╔██║███████╗   ██║   ███████║██████╔╝   ██║   
# ██╔══╝  ██║╚██╔╝██║╚════██║   ██║   ██╔══██║██╔══██╗   ██║   
# ███████╗██║ ╚═╝ ██║███████║   ██║   ██║  ██║██║  ██║   ██║   
# ╚══════╝╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  
#
################################################################
# School:        Embry-Riddle Daytona Beach
# Engineer:      TJ Scherer
#
# Create Date:   10/1/2021
# Design Name:   daemon.py
# Project Name:  emStart Daemon
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
################################################################

from astropy.coordinates import AltAz, EarthLocation, get_sun, SkyCoord
from astropy.time import Time, TimeDelta
from astropy.timeseries import TimeSeries
from datetime import datetime
from timezonefinder import TimezoneFinder
import astropy.units as u
import math
import numpy as np
import pytz
import time

class emulator():
	def __init__(self):
		return(None)

	# Obtain all data needed to begin the emulation
	def Initialize(self, args):
		self.ground = EarthLocation(
			lon = args.longitude[0]*u.deg,
			lat = args.latitude[0]*u.deg,
			height = args.elevation[0]*u.m)

		if(args.local):
			self.localtime = Time(args.date[0] + " " + args.time[0])
		else:
			self.time = Time(args.date[0] + " " + args.time[0])

		# Get the timezone name
		tz = TimezoneFinder().certain_timezone_at(
			lat = self.ground.lat.degree,
			lng = self.ground.lon.degree)
		if tz is None:
			print("WARNING: Could not determine the time zone. Using inputs as UTC.")
			self.timezone = pytz.timezone(pytz.utc)
		else:
			self.timezone = pytz.timezone(tz)

		if(args.local):
			# Convert local time to UTC
			self.offset = self.timezone.utcoffset(self.localtime.to_datetime())
			self.time = self.localtime - self.offset
		else:
			# Convert UTC to local time
			self.offset = self.timezone.utcoffset(self.time.to_datetime())
			self.localtime = self.time + self.offset

		self.delta = TimeDelta(args.duration[0], format='sec')
		self.deltarange = TimeDelta(np.arange(0, args.duration[0]+1, 1), format='sec')
		self.timearray = self.time + self.deltarange

		try:
			self.speed = args.speed[0]
		except:
			self.speed = 1.0
		if(self.speed <= 0.0):
			self.speed = 1.0
		
		self.verbose = args.verbose

		if(self.verbose):
			self.PrintInfo()

		self.GetAltAz()


	def PrintInfo(self):
		# Display the input information after processing
		print()
		print("* Ground Station *********************************")
		print("Latitude  \t" + str(round(self.ground.lat.degree, 5)))
		print("Longitude \t" + str(round(self.ground.lon.degree, 5)))
		print("Timezone  \t" + str(self.timezone))
		print("Starting\t" + str(self.localtime))
		print("Ending  \t" + str(self.localtime + self.delta))
		print()
		print("* Emulation Information **************************")
		print("Starting\t" + str(self.time))
		print("Ending  \t" + str(self.time + self.delta))
		print("Duration\t" + str(self.delta.to_value('sec')) + " seconds (" + str(round(self.delta.to_value('hr'), 2)) + " hours)")
		print("Speed   \t" + str(round(self.speed, 2)) + "x")


	def GetAltAz(self):
		self.target = get_sun(self.timearray)
		self.timeframe = AltAz(
			obstime = self.timearray,
			location = self.ground)
		self.altaz = self.target.transform_to(self.timeframe)

		if(self.verbose):
			for i in range(len(self.altaz)):
				print("Alt: " + str(self.altaz.alt.degree[i]))
				print("Az:  " + str(self.altaz.az.degree[i]))


	def Run(self):
		print("Run!")