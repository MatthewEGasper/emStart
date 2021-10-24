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
# Create Date:   10/22/2021
# Design Name:   sockets.py
# Project Name:  emStart Sockets
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

import zmq

class Sockets():

	def __init__(self):
		self.context = zmq.Context()

		self.time_port = 5555
		self.data_port = 5556

		return(None)

	def pub_time(self):
		pub_time = self.context.socket(zmq.PUB)
		pub_time.bind("tcp://*:" + str(self.time_port))
		return(pub_time)

	def sub_time(self):
		sub_time = self.context.socket(zmq.SUB)
		sub_time.setsockopt(zmq.CONFLATE, 1) # only get the most recent data
		sub_time.connect("tcp://localhost:" + str(self.time_port))
		sub_time.subscribe("")
		return(sub_time)

	def req_data(self):
		req_data = self.context.socket(zmq.REQ)
		req_data.connect("tcp://localhost:" + str(self.data_port))
		return(req_data)

	def rep_data(self):
		rep_data = self.context.socket(zmq.REP)
		rep_data.bind("tcp://*:" + str(self.data_port))
		return(rep_data)