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
# Create Date:   09/28/2021
# Design Name:   astro.py
# Project Name:  emStart Earth Subsystem
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

import argparse
# import astropy
from astropy import constants
import dash
import sys

def PrintUsage():
	print("USAGE: astro [time] [location] [space object]")
	print("  This module is intended to stream astronomy data from a remote server.")
	print("  This will allow our emulator to adjust its position based on real data.")
	exit()

# Print Usage
if(sys.argv.count('-?') > 0 or sys.argv.count('-help') > 0 or sys.argv.count('help') > 0):
	PrintUsage()

# Set verbosity
if(sys.argv.count('-verbose') > 0):
	VERBOSE = True
else:
	VERBOSE = False

print("Hi there!")
print("The astropy constant for 'G' is:")
print(constants.G)