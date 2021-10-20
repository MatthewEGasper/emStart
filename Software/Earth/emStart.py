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
# Example (CMD): python emStart.py 2021-10-31 11:30:00 60 29 -81 2 -v
# Example (GUI): python emStart.py -g
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

parser.add_argument('-g', '--gui',
	action = 'store_true',
	help = 'launch with user interface')

# Parse all arguments
args = parser.parse_args()

if(args.gui):
	a = subprocess.Popen('python app.py')
e = subprocess.Popen('python emulator.py')

if(args.gui):
	a.wait()
e.wait()