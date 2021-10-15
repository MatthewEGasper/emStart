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
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from datetime import date

app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])
load_figure_template("DARKLY")

from daemon import emulator
em = emulator()

plot = html.Div([
	dcc.Graph(
		id = 'live-update-graph',
		style = {'height': '40vh', 'width': '100vw'}),
	dcc.Interval(
		id = 'interval-component',
		interval = 1000,
		n_intervals = 0)])

options = html.Div(
	style = {'margin': '10px'},
	children = [
		html.H5('Date'),

		dcc.Input(
			id = 'select-date',
			placeholder = 'YYYY-MM-DD',
			value = date.today()),

		html.H5('Time', style = {'margin-top': '10px'}),

		dcc.Input(
			id = 'select-time',
			placeholder = 'HH:MM:SS.MS',
			value = '12:00:00.00'),

		dcc.Checklist(
			id = 'select-local',
			options = [
			{'label': 'Local Time', 'value': 'Local'}]),

		html.H5('Duration', style = {'margin-top': '10px'}),

		dcc.Input(
			id = 'select-duration',
			inputMode = 'numeric',
			min = 1,
			placeholder = 'Duration in seconds',
			type = 'number',
			value = 3600),
		html.P(id = 'datetime-selected'),

		html.H5('Latitude', style = {'margin-top': '10px'}),

		dcc.Input(
			id = 'select-latitude',
			inputMode = 'numeric',
			min = -90.0,
			max = 90.0,
			placeholder = 'Latitude',
			type = 'number',
			value = 29.0),

		html.H5('Longitude', style = {'margin-top': '10px'}),

		dcc.Input(
			id = 'select-longitude',
			inputMode = 'numeric',
			min = -180.0,
			max = 180.0,
			placeholder = 'Longitude',
			type = 'number',
			value = -81.0),
		html.P(id = 'location-selected'),

		html.H5('Speed', style = {'margin-top': '10px'}),

		dcc.Slider(
			id = 'select-speed',
			min = 0.1,
			max = 3600,
			step = 0.1,
			value = 1.0),
		html.P(id = 'speed-selected'),
		
		html.Button(
			'Run',
			id = 'select',
			style = {'margin-top': '10px'}),
		html.P(id = 'button-press'),
		])

app.layout = dbc.Container(fluid = True, children = [plot, options])

@app.callback(
	Output('live-update-graph', 'figure'),
	Input('interval-component', 'n_intervals'))

def update_graph_live(n):
	# Create the graph
	df = pd.DataFrame(
		data = {'time': em.t, 'altitude': em.alt, 'azimuth': em.az})
	fig = px.scatter(
		df,
		x = "time",
		y = "altitude")

	return fig

@app.callback(
	Output('datetime-selected', 'children'),
	Input('select-date', 'value'),
	Input('select-time', 'value'),
	Input('select-local', 'value'),
	Input('select-duration', 'value'))

def update_output(d, t, l, delta):
	global date, time, local, duration
	date = d
	time = t
	local = l
	duration = delta
	if(l):
		return("You selected " + d + " at " + t + " local time for " + str(delta) + " seconds.")
	else:
		return("You selected " + d + " at " + t + " for " + str(delta) + " seconds.")

@app.callback(
	Output('location-selected', 'children'),
	Input('select-latitude', 'value'),
	Input('select-longitude', 'value'))

def update_output(lat, lon):
	global latitude, longitude
	latitude = lat
	longitude = lon
	return("Location lat/lon is " + str(lat) + "/" + str(lon))

@app.callback(
	Output('speed-selected', 'children'),
	Input('select-speed', 'value'))

def update_output(s):
	global speed
	speed = s
	return("Speed is " + str(s) + "x")

@app.callback(
	Output('button-press', 'children'),
	Input('select', 'n_clicks'))

def update_output(num):
	if(num != None):
		print("Emulation started!")
		# Start the emulation
		args = Namespace(date=[date], time=[time], local=local, duration=[duration], speed=[speed], latitude=[latitude], longitude=[longitude], elevation=[2.0], verbose=False)
		em.Initialize(args)
		em.Run()

app.run_server(debug = True)