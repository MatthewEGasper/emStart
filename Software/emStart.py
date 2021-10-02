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
# Create Date:   9/28/2021
# Design Name:   emStart.py
# Project Name:  emStart Main Module
# Tool Versions: Python 3.9.7
# Description:   
#
# Dependencies: astropy, dash, pandas, plotly,
#               pytz, timezonefinder
#
# Revision:      0.0
# Revision 0.0 - File Created
#
# Additional Comments:
#
#################################################

import argparse
import astropy.units as u
import gui
import sys
from astropy.time import TimeDelta
from util import GetEarthLocation, OffsetAt, GetAdjustedTime

def ParseArguments():
	parser = argparse.ArgumentParser(
		description='Launch emStart.')

	class LaunchGui(argparse.Action):
		def __call__(self, parser, namespace, values, option_string=None):
			import dash
			from gui import gui

			app = dash.Dash(__name__)
			g = gui(app)
			g.Launch()
			if __name__ == '__main__':
				app.run_server(debug=True)

			parser.exit()

	parser.register('action', 'override', LaunchGui)
	group = parser.add_argument_group('override arguments')
	group.add_argument('-g', '--gui', nargs=0, action='override', help='launch the graphical user interface')

	parser.add_argument('date',
		type=str,
		nargs=1,
		help='specify the start date of the emulation (YYYY-MM-DD)')
	parser.add_argument('time',
		type=str,
		nargs=1,
		help='specify the start time of the emulation (HH:MM:SS.MS)')
	parser.add_argument('delta',
		type=float,
		nargs=1,
		help='specify the duration of the emulation in seconds')
	parser.add_argument('lat',
		type=float,
		nargs=1,
		help='specify the latitude of the ground station')
	parser.add_argument('lon',
		type=float,
		nargs=1,
		help='specify the longitude of the ground station')
	parser.add_argument('elevation',
		type=float,
		nargs=1,
		help='specify the elevation of the ground station in meters')

	# Parse all arguments
	args = parser.parse_args()
	return(args)

args = ParseArguments()

ground = GetEarthLocation(args.lat[0]*u.deg, args.lon[0]*u.deg, args.elevation[0]*u.m)
timezone = OffsetAt(ground.lat.degree, ground.lon.degree)
time = GetAdjustedTime(ground, args.date[0], args.time[0])
delta = TimeDelta(args.delta[0], format='sec')

# Display the input information after processing
print()
print("====== Emulation Information ======")
print("Timezone is " + str(timezone))
print("Starting at " + str(time))
print("Ending at   " + str(time+delta))
print("Duration of " + str(delta) + " seconds")
print()