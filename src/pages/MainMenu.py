from dash import Dash, dcc, html, Input, Output, callback, State

layout = html.Div(className='MainMenu', 
	children=[
		html.H1('Bayer 3D Chart', className='MainMenuTitle'),
		html.Div(className='MainMenuButtons', 
			children=[
				html.P(id='spacing'),
				html.Button('Add branch', id='addBranchButton', className='addBranchMenuCss'),
				html.Button('Delete branch', id='deleteBranchButton', className='deleteBranchMenuCss'),
				html.Button('Edit branch', id='editBranchButton', className='editBranchMenuCss'),
				html.Button('Filter', id='filterButton', className='filterMenuCss'),
				html.Div (className='square')
			]
			
		),
		
		html.Div(id='redirect_add_branch'),
		html.Div(id='redirect_delete_branch'),
		html.Div(id='redirect_edit_branch'),

	]
)

@callback(
	Output('redirect_add_branch', 'children'),
	Input('addBranchButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleAddBranch(n_clicks):
	return dcc.Location(pathname='/AddNewBranch', id='tempL')

@callback(
	Output('redirect_delete_branch', 'children'),
	Input('deleteBranchButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleDeleteBranch(n_clicks):
	return dcc.Location(pathname='/DeleteBranch', id='tempL')

@callback(
	Output('redirect_edit_branch', 'children'),
	Input('editBranchButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleEditPage(n_clicks):
	return dcc.Location(pathname='/EditBranch', id='tempL')


