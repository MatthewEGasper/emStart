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
from threading import Thread, Lock
from timezonefinder import TimezoneFinder
import astropy.units as u
import math
import numpy as np
import pytz
import time

class emulator():
	
	def __init__(self, args):
		# Initialize based on input arguments

		self.verbose = args.verbose

		ground = EarthLocation(
			lon = args.longitude[0]*u.deg,
			lat = args.latitude[0]*u.deg,
			height = args.elevation[0]*u.m)

		if(args.local):
			localtime = Time(args.date[0] + " " + args.time[0])
		else:
			time = Time(args.date[0] + " " + args.time[0])

		# Determine the timezone of ground
		tz = TimezoneFinder().certain_timezone_at(
			lat = ground.lat.degree,
			lng = ground.lon.degree)
		if tz is None:
			print("WARNING: Could not determine the time zone. Using inputs as UTC.")
			timezone = pytz.timezone(pytz.utc)
		else:
			timezone = pytz.timezone(tz)

		# Obtain local and UTC times
		if(args.local):
			# Convert local time to UTC
			offset = timezone.utcoffset(localtime.to_datetime())
			utctime = localtime - offset
		else:
			# Convert UTC to local time
			offset = timezone.utcoffset(utctime.to_datetime())
			localtime = time + offset

		# Create the list of sample times
		delta = TimeDelta(args.duration[0], format='sec')
		time = utctime + TimeDelta(np.arange(0, delta.to_value('sec')+1, 1), format='sec')

		speed = args.speed[0]
		if(speed < 0.0):
			print("WARNING: Entered speed is not valid, using real-time (1x).")
			speed = 1.0

		# Select target in space
		target = get_sun(time)

		# Calculate altitude and azimuth for all data samples
		samples = AltAz(
			obstime = time,
			location = ground)
		altaz = target.transform_to(samples)

		# Display the input information after processing
		if(self.verbose):
			print()
			print("* Ground Station *********************************")
			print("Latitude  \t" + str(round(ground.lat.degree, 5)))
			print("Longitude \t" + str(round(ground.lon.degree, 5)))
			print("Timezone  \t" + str(timezone))
			print("Starting\t" + str(localtime))
			print("Ending  \t" + str(localtime + delta))
			print()
			print("* Emulation Information **************************")
			print("Starting\t" + str(utctime))
			print("Ending  \t" + str(utctime + delta))
			print("Speed   \t" + str(round(speed, 2)) + "x")
			print()
			print("* Time ******************* Alt ****** Az *********")
			for i in range(len(altaz)):
				print(str(time[i]) + "\t" + str(round(altaz.alt.degree[i], 2)) + "\t" + str(round(altaz.az.degree[i], 2)))
			print()
			print("INFO: Initialization complete!")

		input('Press any key to continue...')

		# Start daemon process
		self.run = True
		self.time_thread = Thread(target=self.UpdateTime, daemon=True)


	def UpdateTime(self):
		print("Run")


	def Quit(self):
		print("Quit")