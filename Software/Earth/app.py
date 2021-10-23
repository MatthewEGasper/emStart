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

from argparse import Namespace
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, no_update, callback_context
from datetime import date
from plotly.subplots import make_subplots
from random import random
from threading import Timer
import dash_bootstrap_components as dbc
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import webbrowser
import zmq


app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])

responsive = True # Indicates whether or not the emulator is responsive
port = 5000

graph = html.Div([
	dcc.Graph(
		id = 'live-graph'),
	dcc.Interval(
		id = 'interval-component',
		interval = 500)])

app.layout = dbc.Container(fluid = True, children = [graph])

@app.callback(
	Output('live-graph', 'figure'),
	State('live-graph', 'figure'),
	Input('interval-component', 'n_intervals'))

def update_graph(fig, n):
	context = zmq.Context()
	time_socket = context.socket(zmq.SUB)
	time_socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent data
	time_socket.connect("tcp://localhost:5555")
	time_socket.subscribe("")

	# data_socket = context.socket(zmq.SUB)
	# data_socket.connect("tcp://localhost:5556")
	# data_socket.subscribe("")

	time, alt, az = time_socket.recv_json()

	if(fig is None):
		# Create the figure
		fig = make_subplots(specs=[[{"secondary_y": True}]])
		fig.update_layout(template="plotly_dark")
		fig.add_trace(
			go.Scatter(
				name = "Altitude",
				x = [time],
				y = [alt],
				line = go.scatter.Line(
					color= "fuchsia",
					width = 2)),
			secondary_y = False,
		)
		fig.add_trace(
			go.Scatter(
				name = "Azimuth",
				x = [time],
				y = [az],
				line = go.scatter.Line(
					color = "yellow",
					width = 2)),
			secondary_y = True,
		)
		# Set x axis title
		fig.update_xaxes(title_text = "UTC Time")
		# Set y axes titles
		fig.update_yaxes(title_text = "Altitude", secondary_y = False)
		fig.update_yaxes(title_text = "Azimuth", secondary_y = True)
		# Prevent graph from updating axis
		fig["layout"]["uirevision"] = ""
		fig.add_shape(
			type = "line",
			x0 = time,
			y0 = 0,
			x1 = time,
			y1 = 1,
			line = dict(
				color = "white",
				width = 1),
			xref = "x",
			yref = "paper"
		)
	else:
		# Move the line to the current time
		fig["layout"]["shapes"][0]["x0"] = time
		fig["layout"]["shapes"][0]["x1"] = time
		# Check to see if the data is new
		if(time not in fig["data"][0]["x"]):
			# If it is new data, add it and sort it into the list
			fig["data"][0]["x"].append(time)
			fig["data"][1]["x"].append(time)
			fig["data"][0]["x"].sort()
			fig["data"][1]["x"].sort()
			i0 = fig["data"][0]["x"].index(time)
			i1 = fig["data"][1]["x"].index(time)
			fig["data"][0]["y"].insert(i0, alt)
			fig["data"][1]["y"].insert(i1, az)
		fig["layout"]["uirevision"] = "" # Prevent graph from updating axis

	# Close the opened sockets
	time_socket.close()

	return(fig)

def browser():
	webbrowser.open_new("http://localhost:" + str(port))

if __name__ == '__main__':
	Timer(1, browser).start();
	app.run_server(debug = True, port = port, use_reloader = False)