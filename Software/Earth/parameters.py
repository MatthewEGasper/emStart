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
# Design Name:   parameters.py
# Project Name:  emStart Parameters
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
from timezonefinder import TimezoneFinder
import astropy.units as u
import datetime
import json
import math
import numpy as np
import pytz
import time

class Parameters():

	def __init__(self):
		# Read initialization and configuration data from info.json
		try:
			file = open("info.json")
			info = json.load(file)
			self.info = info
		except:
			print("WARNING: \"info.json\" not found.")

		self.Update()

		return(None)

	def Update(self):
		self.verbose = self.get_verbosity()
		self.speed = self.get_speed()
		self.interval = self.get_interval()
		self.ground = self.get_ground()
		self.local = self.get_local()
		self.timezone = self.get_timezone(self.ground)
		self.time, self.localtime, self.delta, self.timearray = self.get_time(self.local, self.timezone)
		self.target = self.get_target(self.timearray)
		self.altaz = self.get_altaz(self.ground, self.timearray, self.target)

		if(self.verbose):
			self.Print()

	def Print(self):
		# Display the input information after processing
		print("* Ground Station *********************************")
		print("Latitude  \t" + str(round(self.ground.lat.degree, 5)))
		print("Longitude \t" + str(round(self.ground.lon.degree, 5)))
		print("Elevation \t" + str(round(self.ground.height.to_value(u.m), 2)))
		print("Timezone  \t" + str(self.timezone))
		# print("Local?    \t" + str(self.local))
		print("Starting\t" + str(self.localtime))
		print("Ending  \t" + str(self.localtime + self.delta))
		print()
		print("* Emulation Information **************************")
		print("Starting\t" + str(self.time))
		print("Ending  \t" + str(self.time + self.delta))
		print("Duration\t" + str(self.delta.to_value('sec')) + " seconds (" + str(round(self.delta.to_value('hr'), 2)) + " hours)")
		print("Speed   \t" + str(round(self.speed, 2)) + "x")
		if(self.verbose):
			print()
			print("* Sampled Times **********************************")
			print(self.timearray)
			print()
			print("\nTime\t\t\t\tAlt\tAz")
			print("==================================================")
			for i in range(len(self.altaz)):
				print(str(self.timearray[i]) + "\t\t" + str(round(self.altaz.alt.degree[i], 2)) + "\t" + str(round(self.altaz.az.degree[i], 2)))
		print()

	def get_verbosity(self):
		try:
			x = self.info["configuration"]["verbose"]
			if(type(x) is bool):
				return(x)
			else:
				raise Exception
		except:
			print("WARNING: Verbosity configuration is invalid! Verbosity is disabled.")
			return(True)

	def get_speed(self):
		try:
			s = float(self.info["configuration"]["speed"])
			if(s >= 0):
				return(s)
			else:
				raise Exception
		except:
			print("WARNING: Speed configuration is invalid! Using default of 1.")
			return(1.0)

	def get_interval(self):
		try:
			i = int(self.info["configuration"]["interval"])
			if(i >= 0):
				return(i)
			else:
				raise Exception
		except:
			print("WARNING: Interval configuration is invalid! Using default of 1 second interval.")
			return(1)

	def get_ground(self):
		try:
			lat = float(self.info["parameters"]["latitude"])
			if(abs(lat) >= 90):
				print(type(lat) is not float)
				print(type(lat) is not int)
				print(abs(lat) >= 90)
				raise Exception
		except:
			print("WARNING: Invalid latitude! Defaulting to 0.")
			lat = 0

		try:
			lon = float(self.info["parameters"]["longitude"])
			if(abs(lon) >= 180):
				raise Exception
		except:
			print("WARNING: Invalid longitude! Defaulting to 0.")
			lon = 0

		try:
			height = float(self.info["parameters"]["elevation"])
		except:
			print("WARNING: Invalid elevation! Defaulting to 0.")
			height = 0

		ground = EarthLocation(
			lat = lat*u.deg,
			lon = lon*u.deg,
			height = height*u.m)
		return(ground)

	def get_local(self):
		try:
			local = bool(self.info["parameters"]["local"])
		except:
			print("WARNING: Invalid definition for locality. Assuming local time is provided.")
			return(True)

	def get_timezone(self, ground):
		tz = TimezoneFinder().certain_timezone_at(
			lat = ground.lat.degree,
			lng = ground.lon.degree)
		if tz is None:
			print("WARNING: Could not determine the time zone. Using inputs as UTC.")
			timezone = pytz.timezone(pytz.utc)
		else:
			timezone = pytz.timezone(tz)
		return(timezone)

	def get_time(self, local, timezone):
		try:
			date = str(self.info["parameters"]["date"])
			datetime.date.fromisoformat(date)
		except:
			print("WARNING: Invalid date! Using " + datetime.date.today().isoformat() + " instead.")
			date = datetime.date.today().isoformat()

		try:
			time = str(self.info["parameters"]["time"])
			datetime.time.fromisoformat(time)
		except:
			print("WARNING: Invalid time! Using 00:00:00.000 instead.")
			time = "00:00:00.000"

		try:
			duration = int(self.info["parameters"]["duration"])
			if(duration <= 0):
				raise Exception
		except:
			print("WARNING: Invalid duration! Using 3600 seconds.")
			duration = 3600
		
		try:
			if(local):
				localtime = Time(date + " " + time)
				# Convert local time to UTC
				offset = timezone.utcoffset(localtime.to_datetime())
				time = localtime - offset
			else:
				time = Time(date + " " + time)
				# Convert UTC to local time
				offset = timezone.utcoffset(time.to_datetime())
				localtime = time + offset
		except:
			print("ERROR: Failed to read date and time! Program will now exit.")
			exit()

		delta = TimeDelta(duration, format='sec')
		deltarange = TimeDelta(np.arange(0, duration+1, 1), format='sec')
		timearray = time + deltarange
		return([time, localtime, delta, timearray])

	def get_target(self, timearray):
		# Select target in space
		try:
			target = str(self.info["parameters"]["target"])
			if(target == "sun"):
				return(get_sun(timearray))
			elif(target == "moon"):
				return(get_moon(timearray))
			else:
				return(SkyCoord.from_name(target))
		except:
			print("WARNING: Selected target is invalid. Targeting the sun.")
			return(get_sun(timearray))

	def get_altaz(self, ground, timearray, target):
		timeframe = AltAz(
			obstime = timearray,
			location = ground)
		return(target.transform_to(timeframe))