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
from dash_bootstrap_templates import load_figure_template
from datetime import date
from random import random
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import pandas as pd
import time
import zmq

app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])
load_figure_template("DARKLY")

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
	socket = context.socket(zmq.SUB)
	socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent data
	socket.connect("tcp://localhost:5555")
	socket.subscribe("")

	poller = zmq.Poller()
	poller.register(socket, zmq.POLLIN)

	p = poller.poll(1000)
	if(p == []):
		print("WARNING: Emulator unresponsive!")
	else:
		d = int(socket.recv_string(zmq.NOBLOCK))

	socket.close()

	if(fig is None):
		fig = px.area(x=[0], y=[d])
	else:
		# fig.y.append(d)
		print(fig)

	return(fig)

	return(no_update)

if __name__ == '__main__':
	app.run_server(debug = True)