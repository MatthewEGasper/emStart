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
# Design Name:   app.py

# Project Name:  emStart Application
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

from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, no_update, callback_context
from datetime import date
from plotly.subplots import make_subplots
from sockets import Sockets
from threading import Lock, Timer, Thread
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import time
import webbrowser
import zmq

class Dashboard():

	def __init__(self):
		self.fig = None
		self.nofig = None
		self.obsolete = False
		# Open communication sockets
		self.sockets = Sockets()
		self.socket = self.sockets.client()
		self.lock = Lock()

		# Spawn thread to get updates from server
		Thread(target = self.Client, daemon = True).start()

		self.Run()
		
		return(None)

	def Client(self):
		while(True):
			time.sleep(1)
			# See if there is new data
			with self.lock:
				self.socket.send_string('new')
				new = self.socket.recv_json()

			if(new or self.nofig):
				# Request figure data
				with self.lock:
					self.socket.send_string('all')
					data = self.socket.recv_json()

				# Create the figure
				self.fig = None
				self.fig = make_subplots(specs=[[{"secondary_y": True}]])
				self.fig.update_layout(template="plotly_dark")

				self.fig.add_trace(
					go.Scatter(
						name = "Altitude",
						x = data[0],
						y = data[1],
						line = go.scatter.Line(
							color= "fuchsia",
							width = 2)),
					secondary_y = False,)

				self.fig.add_trace(
					go.Scatter(
						name = "Azimuth",
						x = data[0],
						y = data[2],
						line = go.scatter.Line(
							color = "yellow",
							width = 2)),
					secondary_y = True,)

				# Set axis titles
				self.fig.update_xaxes(title_text = "UTC Time")
				self.fig.update_yaxes(title_text = "Altitude", secondary_y = False)
				self.fig.update_yaxes(title_text = "Azimuth", secondary_y = True)

				# Add line showing the current time
				self.fig.add_shape(
					type = "line",
					x0 = data[0][0],
					y0 = 0,
					x1 = data[0][0],
					y1 = 1,
					line = dict(
						color = "white",
						width = 1),
					xref = "x",
					yref = "paper"
				)

				# Prevent graph from updating axis
				self.fig["layout"]["uirevision"] = ""

				self.obsolete = True

	def Run(self):
		app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])

		graph = html.Div([
			dcc.Graph(
				id = 'live-graph'),
			dcc.Interval(
				id = 'interval-component',
				interval = 1000)])

		app.layout = dbc.Container(fluid = True, children = [graph])

		@app.callback(
			Output('live-graph', 'figure'),
			State('live-graph', 'figure'),
			Input('interval-component', 'n_intervals'))

		def update_graph(fig, n):
			if(self.obsolete):
				self.nofig = False
				self.obsolete = False
				return(self.fig)

			if(fig is not None):
				# Request current time
				with self.lock:
					self.socket.send_string('now')
					time = self.socket.recv_json()

				# Move the line to the current time
				fig['layout']['shapes'][0]['x0'] = fig['layout']['shapes'][0]['x1'] = time

				# Prevent graph from updating axis
				fig['layout']['uirevision'] = ''

				return(fig)
			else:
				self.nofig = True
				return(no_update)

		if __name__ == '__main__':
			app.run_server(debug = True, use_reloader = False)

if __name__ == '__main__':
	Dashboard()