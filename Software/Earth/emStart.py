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
# Create Date:   9/28/2021
# Design Name:   emStart.py
# Project Name:  emStart Main Module
# Tool Versions: Python 3.9.7
# Description:   
#
# Dependencies:  pip install -r requirements.txt
# Example:       python emStart.py 2021-10-31 11:30:00 3600 29 -81 2 -s 60 -v
#
# Revision:      0.0
# Revision 0.0 - File Created
#
# Additional Comments:
#
################################################################

import argparse

def ParseArguments():
	parser = argparse.ArgumentParser(
		description='Launch emStart.')

	class Application(argparse.Action):
		def __call__(self, parser, namespace, values, option_string=None):
			import app
			parser.exit()

	parser.register('action', 'override', Application)
	group = parser.add_argument_group('override arguments')
	group.add_argument('-g', '--gui', nargs=0, action='override', help='launch the graphical user interface')


	def validate(x, min, max):
		try:
			x = float(x)
		except ValueError:
			raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))
		if x < min or x > max:
			raise argparse.ArgumentTypeError("%r out of bounds [%.1f, %.1f]" % (x, min, max))
		return(x)

	def float_lat(x):
		x = validate(x, -90.0, 90.0)
		return(x)

	def float_lon(x):
		x = validate(x, -180.0, 180.0)
		return(x)

	# Required date, time, and duration
	parser.add_argument('date',
		type=str,
		nargs=1,
		help='specify the UTC date of the emulation (YYYY-MM-DD)')
	parser.add_argument('time',
		type=str,
		nargs=1,
		help='specify the UTC time of the emulation (HH:MM:SS.MS)')

	# Optional local time
	parser.add_argument('-l', '--local',
		action = 'store_true',
		help='indicate if values are provided in local time')

	parser.add_argument('duration',
		type=int,
		nargs=1,
		help='specify the duration of the emulation in seconds')

	# Optional step modifier
	parser.add_argument('-s', '--speed',
		type=float,
		nargs=1,
		help='specify the emulation speed')

	# Required ground station location
	parser.add_argument('latitude',
		type=float_lat,
		nargs=1,
		help='specify the latitude of the ground station')
	parser.add_argument('longitude',
		type=float_lon,
		nargs=1,
		help='specify the longitude of the ground station')
	parser.add_argument('elevation',
		type=float,
		nargs=1,
		help='specify the elevation of the antenna in meters')

	# Optional verbosity
	parser.add_argument('-v', '--verbose',
		action = 'store_true',
		help='enable verbosity')

	# Parse all arguments
	return(parser.parse_args())

args = ParseArguments()

# Extract information from args
from daemon import emulator

em = emulator()
em.Initialize(args)
em.Run()