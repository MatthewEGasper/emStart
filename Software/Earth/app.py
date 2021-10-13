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

from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from datetime import date

app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])
load_figure_template("DARKLY")

# plot = dcc.Graph(
# 	figure = px.scatter_3d(
# 		px.data.gapminder().query("continent=='Europe'"),
# 		x = "gdpPercap",
# 		y = "pop",
# 		z = "year",
# 		color = 'country'),
# 	style = {'height': '40vh', 'width': '100vw'})

plot = dcc.Graph(
	figure = px.scatter(
		pd.DataFrame(
			dict(
				a=[0,1,2,3,4,5,6,7,8],
				b=[1,3,5,7,9,11,13,15,17])),
		x = "a",
		y = "b"),
	style = {'height': '40vh', 'width': '100vw'})

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
			max = 10,
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
	Output('datetime-selected', 'children'),
	Input('select-date', 'value'),
	Input('select-time', 'value'),
	Input('select-local', 'value'),
	Input('select-duration', 'value'))

def update_output(date, time, local, duration):
	if(local):
		return("You selected " + date + " at " + time + " local time for " + str(duration) + " seconds.")
	else:
		return("You selected " + date + " at " + time + " for " + str(duration) + " seconds.")

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

def update_output(speed):
	return("Speed is " + str(speed) + "x")

@app.callback(
	Output('button-press', 'children'),
	Input('select', 'n_clicks'))

def update_output(num):
	if(num != None):
		print("Emulation started!")
		# Start the emulation
		print(latitude)
		print(longitude)

app.run_server(debug = True)