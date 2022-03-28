from dash import Dash, dcc, html, Input, Output, callback, State

layout = html.Div(className='AddNewBranchMain', 
	children=[
		html.H1('Add New Branch'),
		html.Div(className='AddBranchBody', 
			children=[
				html.P('Branch name:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
				html.P(id='spacing'),
				html.Button('Add branch', id='addBranchButton', className='addBranchCss')
			],
			style={'paddingTop': '90px'}
		),
		html.Button('Home', id='homeButton', className='homeButtonCss', style={'position': 'relative', 'top': '180px'}),
		html.Div(id='hidden_div_for_redirect_callback_add_branch'),
		html.Div(id='hidden_div_for_redirect_callback_home_button')
	]
)

@callback(
	Output('hidden_div_for_redirect_callback_add_branch', 'children'),
	Input('addBranchButton', 'n_clicks'),
	State('branchName', 'value'),
	prevent_initial_call=True
)
def handleAddBranch(n_clicks, branch):
	print((branch))
	if not branch:
		return html.P('* Invalid branch name', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
	else:
		return html.P('* Branch was added successfully', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '300px'})

@callback(
	Output('hidden_div_for_redirect_callback_home_button', 'children'),
	Input('homeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')