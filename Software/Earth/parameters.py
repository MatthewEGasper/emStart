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

from astropy.coordinates import AltAz, EarthLocation, get_sun, get_moon, SkyCoord
from astropy.time import Time, TimeDelta
from astropy.timeseries import TimeSeries
from timezonefinder import TimezoneFinder
import astropy.units as u
import configparser
import datetime
import math
import numpy as np
import pytz
import time

class Parameters():

	def __init__(self):
		self.Update()
		return(None)

	def Sections(self, file = 'config.ini'):
		config = configparser.ConfigParser()
		config.read(file)
		print(config.sections())

	def Update(self, file = 'config.ini', section = 'DEFAULT'):
		try:
			config = configparser.ConfigParser()
			config.read(file)
			self.config = config
		except:
			print('WARNING: Configuration file \'' + file + '\' not found.')

		# Set parameters of the emulation
		self.section = section
		self.verbose = self.get_verbosity()
		self.speed = self.get_speed()
		if(self.section == 'OVERRIDE'):
			file = config[self.section]['file']
			print('INFO: Data override requested!')
			
			self.t, self.alt, self.az = [], [], []
			import csv
			with open(file) as csvfile:
				csvreader = csv.reader(csvfile)
				header = next(csvreader)
				for row in csvreader:
					self.t.append(row[0])
					self.alt.append(float(row[1]))
					self.az.append(float(row[2]))
				csvfile.close()

			print('INFO: Data override accepted!')
			if(self.verbose):
				self.PrintData()
		else:
			ground = self.get_ground()
			local = self.get_local()
			timezone = self.get_timezone(ground)
			interval = self.get_interval()
			time, localtime, delta, timearray = self.get_time(local, timezone, interval)
			target = self.get_target(timearray)
			altaz = self.get_altaz(ground, timearray, target)
			self.t, self.alt, self.az = self.get_info(timearray, altaz)
			self.Print(ground, local, timezone, interval, time, localtime, delta, timearray, target, altaz)

	def PrintData(self):
		print()
		print('* Simulation Data ********************************')
		print("{:<25} {:<10} {:<10}".format('Time', 'Altitude', 'Azimuth'))
		for i in range(len(self.t)):
			print("{:<25} {:<10} {:<10}".format(self.t[i], str(round(self.alt[i], 2)), str(round(self.az[i], 2))))
		print()

	def Print(self, ground, local, timezone, interval, time, localtime, delta, timearray, target, altaz):
		print()
		# Display the input information after processing
		print('* Ground Station *********************************')
		print('Latitude  \t' + str(round(ground.lat.degree, 5)))
		print('Longitude \t' + str(round(ground.lon.degree, 5)))
		print('Elevation \t' + str(round(ground.height.to_value(u.m), 2)))
		print('Timezone  \t' + str(timezone))
		# print('Local?    \t' + str(local))
		print('Starting\t' + str(localtime))
		print('Ending  \t' + str(localtime + delta))
		print()
		print('* Simulation Information **************************')
		print('Config  \t' + self.section)
		print('Starting\t' + self.t[0])
		print('Ending  \t' + self.t[-1])
		print('Duration\t' + str(delta.to_value('sec')) + ' seconds (' + str(round(delta.to_value('hr'), 2)) + ' hours)')
		print('Speed   \t' + str(round(self.speed, 2)) + 'x')	
		if(self.verbose):
			self.PrintData()
		else:
			print()

	def get_verbosity(self):
		return(self.config.getboolean(self.section, 'verbose', fallback = False))

	def get_speed(self):
		s = self.config.getfloat(self.section, 'speed', fallback = 1)
		if(s >= 0 and s <= 1):
			return(s)
		else:
			print('WARNING: Invalid speed! Using default of 1.')
			return(1.0)

	def get_ground(self):
		lat = self.config.getfloat(self.section, 'latitude', fallback = 0)
		if(abs(lat) >= 90):
			print('WARNING: Invalid latitude! Defaulting to 0.')
			lat = 0

		lon = self.config.getfloat(self.section, 'longitude', fallback = 0)
		if(abs(lon) >= 180):
			print('WARNING: Invalid longitude! Defaulting to 0.')
			lon = 0

		height = self.config.getfloat(self.section, 'elevation', fallback = 0)

		ground = EarthLocation(
			lat = lat*u.deg,
			lon = lon*u.deg,
			height = height*u.m)
		return(ground)

	def get_local(self):
		return(self.config.getboolean(self.section, 'local', fallback = True))

	def get_timezone(self, ground):
		tz = TimezoneFinder().certain_timezone_at(
			lat = ground.lat.degree,
			lng = ground.lon.degree)
		if tz is None:
			print('WARNING: Could not determine the time zone! Using inputs as UTC.')
			timezone = pytz.timezone(pytz.utc)
		else:
			timezone = pytz.timezone(tz)
		return(timezone)

	def get_interval(self):
		i = self.config.getint(self.section, 'interval', fallback = 1)
		if(i > 0):
			return(i)
		else:
			print('WARNING: Invalid interval! Using default of 1 second interval.')
			return(1)

	def get_time(self, local, timezone, interval):
		try:
			date = self.config[self.section]['date']
			datetime.date.fromisoformat(date)
		except:
			date = datetime.date.today().isoformat()
			print('WARNING: Invalid date! Using ' + date + ' instead.')

		try:
			time = self.config[self.section]['time']
			datetime.time.fromisoformat(time)
		except:
			time = '00:00:00.000'
			print('WARNING: Invalid time! Using ' + time + ' instead.')

		duration = self.config.getint(self.section, 'duration', fallback = 3600)
		if(duration <= 0):
			print('WARNING: Invalid duration! Using 3600 seconds.')
			duration = 3600
		
		try:
			if(local):
				localtime = Time(date + ' ' + time)
				# Convert local time to UTC
				offset = timezone.utcoffset(localtime.to_datetime())
				time = localtime - offset
			else:
				time = Time(date + ' ' + time)
				# Convert UTC to local time
				offset = timezone.utcoffset(time.to_datetime())
				localtime = time + offset
		except:
			print('FATAL: Failed to read date and time! Program will now exit.')
			exit()

		delta = TimeDelta(duration, format='sec')
		deltarange = TimeDelta(np.arange(0, duration+1, interval), format='sec')
		timearray = time + deltarange
		return([time, localtime, delta, timearray])

	def get_target(self, timearray):
		# Select target in space
		try:
			target = self.config[self.section]['target']
			if(target == 'sun'):
				return(get_sun(timearray))
			elif(target == 'moon'):
				return(get_moon(timearray))
			else:
				return(SkyCoord.from_name(target))
		except:
			print('WARNING: Selected target is invalid. Targeting the sun.')
			return(get_sun(timearray))

	def get_altaz(self, ground, timearray, target):
		timeframe = AltAz(
			obstime = timearray,
			location = ground)
		return(target.transform_to(timeframe))

	def get_info(self, timearray, altaz):
		t = []
		[t.append(str(time)) for time in timearray]
		alt = list(altaz.alt.degree)
		az = list(altaz.az.degree)
		return([t, alt, az])

if __name__ == '__main__':
	Parameters()