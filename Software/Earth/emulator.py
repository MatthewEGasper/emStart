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
# Engineers:     Ivan Borra and TJ Scherer
#
# Create Date:   11/8/2021
# Design Name:   emulator.py
# Project Name:  emStart Emulator
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

from pymycobot import MyCobot, Angle, Coord
import time

class Emulator():

	def __init__(self):
		return(None)

	def Function(self):
		return(None)

if __name__ == '__main__':
	Emulator()

# mc=MyCobot(PI_PORT, PI_BAUD) ## connects to the arm from Raspberry Pi


# def getdata(): # function made to gather coordinate and angle data.
# 	coords = mc.get_coords() # get_coords() records the coordinate data of all joints.
# 	print("\nCoords:")
# 	print(coords) # prints out coordinate data
# 	angle_datas = mc.get_angles()  # get_angles() records the angle position of all joints
# 	print("\nAngle:")
# 	print(angle_datas)  # prints out joint location


# print("\nstartup data:\n")
# getdata()
# ##
# mc.send_angles([0, 0, 0, 0, 0, 0], 50)  #sends all joints to default position at 50% speed
# print(mc.is_paused())
# time.sleep(2.5) # delay added to allow time for the robot to move into place before recording data
# print("\nstartup data:\n")
# getdata()
# ##
# mc.send_angles(Angle.J2.value, 90, 50) # sets joint 2 to 90 degrees
# time.sleep(2.5)
# mc.pause() # pauses arm movement code to allow for brief delay between next command.
# time.sleep(2.5)
# print("\njoint 2 data:\n")
# getdata()
# ##
# mc.send_angles(Angle.J1.value, 90, 50) # sets joint 1 to 90 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 90 degrees data:\n")
# getdata()
# ##
# mc.send_angles(Angle.J1.value, 180, 50) # sets joint 1 to 180 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 180 degrees data:\n")
# getdata()
# time.sleep(1)
# ##
# mc.send_angles(Angle.J1.value, -90, 50) # sets joint 1 to 270=-90 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 -90 degrees data:\n")
# getdata()
# time.sleep(1)
# ##
# mc.send_angles(Angle.J1.value, 0, 50) # sets joint 1 to 0 degrees
# time.sleep(2.5)
# mc.pause()
# time.sleep(2.5)
# print("\njoint 1 0 degrees data:\n")
# getdata()
# time.sleep(1)

# By taking the robot arm at its full length  (280 mm) joint 1 can be the core of the earth and the other arms rotate around it.
# by moving the robot arm around in a full circle and getting the data of angles and coordinates we can create our own latitude and longitude cordintate system.
