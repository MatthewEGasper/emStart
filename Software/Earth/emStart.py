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
import time

def terminate(process):
	if process.poll() is None:
		subprocess.call("taskkill /F /T /PID " + str(process.pid), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

parser = argparse.ArgumentParser(
	description='Launch emStart.')

parser.add_argument('-ng', '--nogui',
	action = 'store_true',
	help = 'launch without user interface')

# Parse all arguments
args = parser.parse_args()

if(not args.nogui):
	a = subprocess.Popen('python app.py')
	time.sleep(1)
e = subprocess.Popen('python emulator.py')

e.wait()
if(not args.nogui):
	terminate(a)