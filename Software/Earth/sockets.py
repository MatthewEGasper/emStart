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
		self.port = 5555

		return(None)

	def client(self):
		client = self.context.socket(zmq.REQ)
		client.connect("tcp://10.33.230.187:" + str(self.port))
		return(client)

	def server(self):
		server = self.context.socket(zmq.REP)
		server.bind("tcp://*:" + str(self.port))
		return(server)

if __name__ == '__main__':
	Sockets()