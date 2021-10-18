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
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
from random import random
import dash_bootstrap_components as dbc
import plotly
import plotly.express as px
import pandas as pd

from datetime import date

class app():
	def __init__(self):
		self.complete = True
		return(None)

	def Run(self):
		app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])
		load_figure_template("DARKLY")

		graph = html.Div([
			dcc.Graph(
				id = 'live-graph',
				animate = True),
			dcc.Interval(
				id = 'interval')])

		options = html.Div(
			style = {'margin':'10px'},
			children = [
				html.Div(id='placeholder', style={'display':'none'}),

				html.H5('Date'),

				dcc.Input(
					id = 'select-date',
					placeholder = 'Date (YYYY-MM-DD)',
					value = date.today()),

				html.H5('Time'),

				dcc.Input(
					id = 'select-time',
					placeholder = 'Time (HH:MM:SS.MS)',
					value = '12:00:00.00'),

				dcc.Checklist(
					id = 'select-local',
					options = [
					{'label': ' Local Time', 'value': 'Local'}]),

				html.H5('Duration'),

				dcc.Input(
					id = 'select-duration',
					inputMode = 'numeric',
					min = 1,
					placeholder = 'Duration (seconds)',
					type = 'number',
					value = 10),

				html.H5('Latitude'),

				dcc.Input(
					id = 'select-latitude',
					inputMode = 'numeric',
					min = -90.0,
					max = 90.0,
					placeholder = 'Latitude',
					type = 'number',
					value = 29.0),

				html.H5('Longitude'),

				dcc.Input(
					id = 'select-longitude',
					inputMode = 'numeric',
					min = -180.0,
					max = 180.0,
					placeholder = 'Longitude',
					type = 'number',
					value = -81.0),

				html.H5('Elevation'),

				dcc.Input(
					id = 'select-elevation',
					inputMode = 'numeric',
					min = -100,
					max = 100,
					placeholder = 'Elevation (m)',
					type = 'number',
					value = 2),

				html.H5('Speed'),

				dcc.Slider(
					id = 'select-speed',
					min = 0.25,
					max = 10,
					step = 0.25,
					value = 1,
					marks = {
						0.25: {'label':'1/4x'},
						0.5: {'label':'1/2x'},
						1: {'label':'1x'},
						2: {'label':'2x'},
						5: {'label':'5x'},
						10: {'label':'10x'}}),
				html.P(id = 'speed-selected'),
				
				html.Button(
					'Run',
					id = 'select',
					style = {'margin-top': '10px'})
				])

		app.layout = dbc.Container(fluid = True, children = [graph, options])

		@app.callback(
			Output('live-graph', 'figure'),
			Input('interval', 'n_intervals'))

		def update_graph(n):
			# Grab the semaphore to update the data
			em.mutex.acquire()
			df = pd.DataFrame(
				data = {'time': em.t, 'altitude': em.alt, 'azimuth': em.az})
			em.mutex.release()

			# Update the graph with the new data
			fig = px.area(
				df,
				x = "time",
				y = "altitude")
			print("fig update")
			return(fig)

			# em.mutex.acquire()
			# traces = list()
			# traces.append(plotly.graph_objs.Scatter(
			# 	x=em.t,
			# 	y=em.alt,
			# 	name='Scatter',
			# 	mode= 'lines+markers'))
			# em.mutex.release()
			# return {'data': traces}

		# Update values based on input boxes
		@app.callback(
			Output('placeholder', 'children'),
			Input('select-date', 'value'),
			Input('select-time', 'value'),
			Input('select-local', 'value'),
			Input('select-duration', 'value'),
			Input('select-latitude', 'value'),
			Input('select-longitude', 'value'),
			Input('select-elevation', 'value'),
			Input('select-speed', 'value'),
			Input('select', 'n_clicks'))

		def update_values(date, time, local, duration, latitude, longitude, elevation, speed, clicks):
			self.date = date
			self.time = time
			self.local = local
			self.duration = duration
			self.latitude = latitude
			self.longitude = longitude
			self.elevation = elevation
			self.speed = speed
			try:
				if(clicks != self.clicks):
					self.clicks = clicks
					args = Namespace(
						date = [self.date],
						time = [self.time],
						local = self.local,
						duration = [self.duration],
						speed = [self.speed],
						latitude = [self.latitude],
						longitude = [self.longitude],
						elevation = [self.elevation],
						verbose = True)
					from daemon import emulator
					em = emulator(args)
			except:
				self.clicks = clicks

		app.run_server(debug = True)