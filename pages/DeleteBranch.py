from dash import Dash, dcc, html, Input, Output, callback, State

layout = html.Div(className='DeleteBranchMain', 
	children=[
		html.H1('Delete Branch'),
		html.Div(className='DeleteBranchBody', 
			children=[
				html.P('Branch name:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
				html.P(id='spacing'),
				html.Button('Delete branch', id='deleteBranchButton', className='deleteBranchCss')
			],
			style={'paddingTop': '90px'}
		),
		html.Button('Home', id='homeButton', className='homeButtonCss', style={'position': 'relative', 'top': '180px'}),
		html.Div(id='redirect_delete_branch'),
		html.Div(id='redirect_home_button')
	]
)

@callback(
	Output('redirect_delete_branch', 'children'),
	Input('deleteBranchButton', 'n_clicks'),
	State('branchName', 'value'),
	prevent_initial_call=True
)
def handleDeleteBranch(n_clicks, branch):
	print((branch))
	if not branch:
		return html.P('* Invalid branch name', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
	else:
		return html.P('* Branch was added successfully', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '300px'})

@callback(
	Output('redirect_home_button', 'children'),
	Input('homeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')