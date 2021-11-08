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
#
# Revision:      0.0
# Revision 0.0 - File Created
#
# Additional Comments:
#
################################################################

import argparse
import subprocess

parser = argparse.ArgumentParser(
	description='Launch emStart.')

parser.add_argument('-cmd', '--commandline',
	action = 'store_true',
	help = 'launch without user interface')

parser.add_argument('-sim', '--simulation',
	action = 'store_true',
	help = 'launch without arm controls')

# Parse all arguments
args = parser.parse_args()

if(not args.commandline):
	# launch user interface
	gui = subprocess.Popen(["start", "cmd", "/K", "python", "app.py"], shell=True)
	pass

if(not args.simulation):
	# launch emulator
	em = subprocess.Popen(["start", "cmd", "/K", "python", "emulator.py"], shell=True)
	pass

# launch simulator
sim = subprocess.Popen(["start", "cmd", "/K", "python", "simulator.py"], shell=True)