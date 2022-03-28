from dash import Dash, dcc, html, Input, Output, callback, State

layout = html.Div(className='EditBranchMain', 
	children=[
      html.Div(className='AddBranchBody', 
			children=[
				html.H1('Edit a Branch'),
				html.P('Select Branch:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
				html.P('New info 1:', id='branchNameP1', className='paragraphCredential'),
				dcc.Input(id='info1', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P('New info 2:', id='branchNameP2', className='paragraphCredential'),
				dcc.Input(id='info2', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P('New info 3:', id='branchNameP3', className='paragraphCredential'),
				dcc.Input(id='info3', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P(id='spacing'),
				html.Button('Edit', id='editBranchButton', className='addBranchCss'),
                html.P('Current Info 1: xxxxxx', id='branchNameP4', className='paragraphCredential'),
                 html.P('Current Info 2: xxxxxx', id='branchNameP5', className='paragraphCredential'),
                  html.P('Current Info 3: xxxxxx', id='branchNameP6', className='paragraphCredential'),
			],
			style={'paddingTop': '90px'}
		),
        html.Button('Home', id='homeButton', className='homeButtonCss', style={'position': 'relative', 'top': '180px'}),
		html.Div(id='hidden_div_for_redirect_callback_edit_branch'),
		html.Div(id='hidden_div_for_redirect_callback_home_buttonEdit')
    ]
)

@callback(
	Output('hidden_div_for_redirect_callback_edit_branch', 'children'),
	Input('editBranchButton', 'n_clicks'),
	State('branchName', 'value'),
	State('info1', 'value'),
	State('info2', 'value'),
	State('info3', 'value'),
	prevent_initial_call=True
)
def handleEdit(n_clicks, branchName, info1, info2, info3):
	return html.P(("For branch: " + branchName + " - change: " + info1 + ", " + info2 + ", " + info3), id="tempPEdit")


@callback(
	Output('hidden_div_for_redirect_callback_home_buttonEdit', 'children'),
	Input('homeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id="tempL")

