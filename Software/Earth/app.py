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
# from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
from datetime import date
from random import random
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import pandas as pd
import time
import zmq

print("App started")

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.CONFLATE, 1) # only get the most recent data
socket.connect("tcp://localhost:5555")
socket.subscribe("")

while(True):
	time.sleep(2.3)
	try:
		m = socket.recv_string(zmq.NOBLOCK)
		print("SUB: " + m)
	except zmq.ZMQError:
		print("WARNING: Emulation no pulse")
		exit()

# app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])
# load_figure_template("DARKLY")

# graph = html.Div([
# 	dcc.Graph(
# 		id = 'live-graph'),
# 	dcc.Interval(
# 		id = 'interval',
# 		interval = 500)])

# options = html.Div(
# 	style = {'margin':'10px'},
# 	children = [
# 		html.Div(id='placeholder', style={'display':'none'}),

# 		html.H5('Date'),

# 		dcc.Input(
# 			id = 'select-date',
# 			placeholder = 'Date (YYYY-MM-DD)',
# 			value = date.today()),

# 		html.H5('Time'),

# 		dcc.Input(
# 			id = 'select-time',
# 			placeholder = 'Time (HH:MM:SS.MS)',
# 			value = '12:00:00.00'),

# 		dcc.Checklist(
# 			id = 'select-local',
# 			options = [
# 			{'label': ' Local Time', 'value': 'Local'}]),

# 		html.H5('Duration'),

# 		dcc.Input(
# 			id = 'select-duration',
# 			inputMode = 'numeric',
# 			min = 1,
# 			placeholder = 'Duration (seconds)',
# 			type = 'number',
# 			value = 10),

# 		html.H5('Latitude'),

# 		dcc.Input(
# 			id = 'select-latitude',
# 			inputMode = 'numeric',
# 			min = -90.0,
# 			max = 90.0,
# 			placeholder = 'Latitude',
# 			type = 'number',
# 			value = 29.0),

# 		html.H5('Longitude'),

# 		dcc.Input(
# 			id = 'select-longitude',
# 			inputMode = 'numeric',
# 			min = -180.0,
# 			max = 180.0,
# 			placeholder = 'Longitude',
# 			type = 'number',
# 			value = -81.0),

# 		html.H5('Elevation'),

# 		dcc.Input(
# 			id = 'select-elevation',
# 			inputMode = 'numeric',
# 			min = -100,
# 			max = 100,
# 			placeholder = 'Elevation (m)',
# 			type = 'number',
# 			value = 2),

# 		html.H5('Speed'),

# 		dcc.Slider(
# 			id = 'select-speed',
# 			min = 0.25,
# 			max = 10,
# 			step = 0.25,
# 			value = 1,
# 			marks = {
# 				0.25: {'label':'1/4x'},
# 				0.5: {'label':'1/2x'},
# 				1: {'label':'1x'},
# 				2: {'label':'2x'},
# 				5: {'label':'5x'},
# 				10: {'label':'10x'}}),
# 		html.P(id = 'speed-selected'),
		
# 		html.Button(
# 			'Run',
# 			id = 'select',
# 			style = {'margin-top': '10px'})
# 		])

# app.layout = dbc.Container(fluid = True, children = [graph, options])

# @app.callback(
# 	Output('live-graph', 'figure'),
# 	Input('interval', 'n_intervals'))

# def update_graph(n):
# 	try:
# 		socket.send(b"Hi from app!")
# 		print("Message sent from app")
# 		m = socket.recv()
# 		print("RESPONSE: " + m)
# 	except:
# 		print("Error in update_graph")
# 	return(no_update)

# # Update values based on input boxes
# @app.callback(
# 	Output('placeholder', 'children'),
# 	Input('select-date', 'value'),
# 	Input('select-time', 'value'),
# 	Input('select-local', 'value'),
# 	Input('select-duration', 'value'),
# 	Input('select-latitude', 'value'),
# 	Input('select-longitude', 'value'),
# 	Input('select-elevation', 'value'),
# 	Input('select-speed', 'value'),
# 	Input('select', 'n_clicks'))

# def update_values(date, time, local, duration, latitude, longitude, elevation, speed, button):
# 	ctx = callback_context

# 	if(ctx.triggered):
# 		if(ctx.triggered[0]['prop_id'].split('.')[0] == 'select'):
# 			args = Namespace(
# 				date = [date],
# 				time = [time],
# 				local = local,
# 				duration = [duration],
# 				speed = [speed],
# 				latitude = [latitude],
# 				longitude = [longitude],
# 				elevation = [elevation],
# 				verbose = True)

# 			# Send request to start
# 			print("Click!")
# 	return(no_update)

# if __name__ == '__main__':
# 	app.run_server(debug = True)