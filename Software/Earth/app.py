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
from dash.exceptions import PreventUpdate
from datetime import date
from plotly.subplots import make_subplots
from random import random
from sockets import Sockets
from threading import Lock, Timer
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

sockets = Sockets()
sub_time = sockets.sub_time()
req_data = sockets.req_data()
# Request figure data
req_data.send(b"")
data = req_data.recv_json()

# Create the figure
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(template="plotly_dark")

fig.add_trace(
	go.Scatter(
		name = "Altitude",
		x = data[0],
		y = data[1],
		line = go.scatter.Line(
			color= "fuchsia",
			width = 2)),
	secondary_y = False,)

fig.add_trace(
	go.Scatter(
		name = "Azimuth",
		x = data[0],
		y = data[2],
		line = go.scatter.Line(
			color = "yellow",
			width = 2)),
	secondary_y = True,)

# Set axis titles
fig.update_xaxes(title_text = "UTC Time")
fig.update_yaxes(title_text = "Altitude", secondary_y = False)
fig.update_yaxes(title_text = "Azimuth", secondary_y = True)

# Add line showing the current time
fig.add_shape(
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
fig["layout"]["uirevision"] = ""

graph = html.Div([
	dcc.Graph(
		id = 'live-graph',
		figure = fig),
	dcc.Interval(
		id = 'interval-component',
		interval = 500)])

app.layout = dbc.Container(fluid = True, children = [graph])

@app.callback(
	Output('live-graph', 'figure'),
	State('live-graph', 'figure'),
	Input('interval-component', 'n_intervals'))

def update_graph(fig, n):
	if(fig is not None):
		global sub_time
		# Get the current time
		time = sub_time.recv_json()[0]

		# Move the line to the current time
		fig["layout"]["shapes"][0]["x0"] = time
		fig["layout"]["shapes"][0]["x1"] = time

		# Prevent graph from updating axis
		fig["layout"]["uirevision"] = ""

		return(fig)

def browser():
	webbrowser.open_new("http://localhost:8050")

if __name__ == '__main__':
	browser()
	app.run_server(debug = True, use_reloader = False)