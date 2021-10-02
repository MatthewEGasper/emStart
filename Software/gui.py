#################################################
#                  _____ _             _   
#                 / ____| |           | |  
#   ___ _ __ ___ | (___ | |_ __ _ _ __| |_ 
#  / _ \ '_ ` _ \ \___ \| __/ _` | '__| __|
# |  __/ | | | | |____) | || (_| | |  | |_ 
#  \___|_| |_| |_|_____/ \__\__,_|_|   \__|
#
#################################################
# School:        Embry-Riddle Daytona Beach
# Engineer:      TJ Scherer
#
# Create Date:   10/1/2021
# Design Name:   gui.py

# Project Name:  emStart Graphical User Interface
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
#################################################

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

class gui():
	def __init__(self, app):
		self.app = app
		return(None)

	def Launch(self):
		colors = {
			'background': '#111111',
			'text': '#7FDBFF'
		}

		df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

		fig = px.scatter(df, x="gdp per capita", y="life expectancy",
		 size="population", color="continent", hover_name="country",
		 log_x=True, size_max=60)

		self.app.layout = html.Div([
			dcc.Graph(
				id='life-exp-vs-gdp',
				figure=fig
			)
		])