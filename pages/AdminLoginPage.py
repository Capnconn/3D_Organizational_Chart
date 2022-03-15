from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, State, Output
from pages import AddNewBranch

layout = html.Div(children=[

	html.Div(className="AdminLoginBody", 
		children=
		[
		html.H1('Admin Login'),
		html.Div(className="UsernameCredential", 
			children=[
			html.P('Username', className='paragraphCredential'),
			dcc.Input(id='username', type='text', placeholder='', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
			]
		),
		html.Div(className="PasswordCredential", 
			children=[
			html.P('Password', className='paragraphCredential'),
			dcc.Input(id='password', type='text', placeholder='', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'})
			]
		),		
		dcc.Link('Forgot username', href='', className="UsernameHyperLink"),
		html.Button('Login', id='submit-val', n_clicks=0, className="LoginButton"),
		dcc.Link('Forgot password', href='', className="PasswordHyperLink"),
		html.Div(className='ViewGuest', 
			children=[
			html.P('View as a guest', className='ViewParagraph'),
			html.Button('View', id='view', className="LoginButton")
			]
		)
	])
])
# # Change this to handle onClick
# @AdminLoginPage.callback(
# 	Output('hidden-div', 'children'),
# 	Input('username', 'value'),
# 	Input('password', 'value'),
# 	Input('submit-val', 'n_clicks')
# )
# def handleSubmit(username, password, n_clicks):
# 	# if n_clicks > 1:
# 	# 	print('username: ' + n_clicks + ' password: ' + password)
# 	# else:
# 	print('dsfasfd')