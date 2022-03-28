from dash import Dash, html, dcc, callback
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, State, Output

layout = html.Div(className='AdminLoginBody',
	children=[
    	html.H1('Admin Login'),
    	html.Div(className='UsernameCredential', 
    		children=[
    			html.P('Username', className='paragraphCredential'),
    			dcc.Input(id='username', type='text', className='inputBox')
    		]
    	),
    	html.Div(className='PasswordCredential', 
    		children=[
    			html.P('Password', className='paragraphCredential'),
    			dcc.Input(id='password', type='password', className='inputBox')
    		]
    	),
		dcc.Link('Forgot username', href='', className="UsernameHyperLink"),
		html.Button('Login', id='submitValue', n_clicks=0, className='LoginButton'),
		dcc.Link('Forgot password', href='', className="PasswordHyperLink"),
    	html.Div(className='PasswordCredential', 
    		children=[
    			html.P(id='temp_id')
    		]
    	),
    	html.Div(className='ViewGuest', 
			children=[
			html.P('View as a guest', className='ViewParagraph'),
			html.Button('View', id='view', className="LoginButton")
			]
		),
		html.Div(id='hidden_div_for_redirect_callback_submit'),
		html.Div(id='hidden_div_for_redirect_callback_view')
])
@callback(
    Output('hidden_div_for_redirect_callback_submit', 'children'),
    Input('submitValue', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value'),
    prevent_initial_call=True

)
def update_output_div(n_clicks, username, password):
    if username == 'connor' and password == 'password':
    	return dcc.Location(pathname='/MainMenu', id='temp');
    else:
    	return html.P('*Username or Password is incorrect', id='temp_p', style={'color': '#cc0000', 'position': 'relative', 'bottom': '540px'})

@callback(
	Output('hidden_div_for_redirect_callback_view', 'children'),
	Input('view', 'n_clicks'),
	prevent_initial_call=True
)
def handleGuest(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='temp')