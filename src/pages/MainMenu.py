from dash import Dash, dcc, html, Input, Output, callback, State, callback_context
import dash_cytoscape as cyto
import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import mysql.connector
import json

previous_branch = []

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Query the database for the top level of nodes
bayerdb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root",
	database="bayerdatabase"
)
cursor = bayerdb.cursor(buffered=True);
cursor.execute("""SELECT branch_id, branch_title FROM org_chart_branches WHERE branch_level='Division'""");
division_tuple = cursor.fetchall()

division_tuple = [(str(x[0]), str(x[1])) for x in division_tuple]
# print(division_tuple)

nodes = [
	{
		'data': {'id': short, 'label': label},
		'position': {'x': 5 * int(short), 'y': -5 * int(short)}
	}
	for short, label in (
		division_tuple
	)
]

# print(nodes)
source_id_list = []
for x in division_tuple:
	source_id_list.append(x[0])


query = "SELECT source_id, target_id FROM edges WHERE source_id IN (" + ','.join(str(x) for x in source_id_list) + ")"
cursor.execute(query)

edge_id_list = cursor.fetchall()
edge_id_list = [(str(x[0]), str(x[1])) for x in edge_id_list]

# edges = [
# 	{'data': {'source': source, 'target': target}}
# 	for source, target in (
# 		edge_id_list
# 	)	
# ]

edges = []

elements = nodes + edges

layout = html.Div(className='MainMenu', 
	children=[
			html.Div(className='MainMenuTitle', children=
				[
					html.H1('Bayer 3D Chart', className='mainMenuHeader'),
				]
			),
			html.Div(className='mainMenuBody', children=
				[
					dbc.Button(
						"Open collapse",
						id='collapse-button',
						className='collapseButtonCss',
						color='primary',
						n_clicks=0
					),
					dbc.Row(
						[
							dbc.Col(
								dbc.Collapse(
									dbc.Card(html.Button('Add branch', id='addBranchButton', className='addBranchMenuCss')),
									id='addButton',
									is_open=False
								)
							),
							dbc.Col(
								dbc.Collapse(
									dbc.Card(html.Button('Delete branch', id='deleteBranchButton', className='deleteBranchMenuCss')),
									id='deleteButton',
									is_open=False
								)
							),
							dbc.Col(
								dbc.Collapse(
									dbc.Card(html.Button('Edit branch', id='editBranchButton', className='editBranchMenuCss')),
									id='editButton',
									is_open=False
								)
							),
						],
						className="mt-3"
					),
					html.Button('Filter', id='filterButton', className='filterMenuCss'),
				]
			),
			html.Div(className='mainMenuToggle', children=
				[
					daq.ToggleSwitch(
						id='networkViewToggle',
						className='networkToggleCss',
						value=False,
						label='Click to change network view',
						color='green',
						size=50
					),
					html.Div(id='my-toggle-switch-output')
				]
			),
			html.Div(className='previousBranchDivCss', children=
				[
					html.P("Previous Branch: x", id='previous-branch', className='previousBranchCss', style={'display': 'none'}),
					html.Button('Previous Branch', id='previousBranchButton', className='previousBranchButtonCss'),
					html.Button('update', id='updateButton', className='previousBranchButtonCss')

				]
			),
			html.Div(className='mainMenuNetwork', children=
				[
					cyto.Cytoscape(
						autoungrabify=True,
						userZoomingEnabled=False,
						id='cytoscape-callbacks-1',
						elements=(nodes+edges),
						style={'width': '100%', 'height': '400px'},
						layout={
						'name': 'circle'
						}

					),
    				html.Div(id='cytoscape-tapNodeData-json'),
				]
			),			
		html.Div(id='redirect_add_branch'),
		html.Div(id='redirect_delete_branch'),
		html.Div(id='redirect_edit_branch'),
		html.Div(id='new_Network')
	]
)

# @callback(
# 	Output('cytoscape-callbacks-1', 'tapNodeData'),
# 	Input('updateButton', 'n_clicks'),
# 	State('cytoscape-callbacks-1', 'elements'),
# 	State('cytoscape-callbacks-1', 'tapNodeData'),
# 	prevent_initial_call=True
# )
# def refresh(n_clicks, elements, tapNodeData):
# 	print(tapNodeData)
# 	return

@callback(
	Output("addButton", "is_open"),
	Output("deleteButton", "is_open"),
	Output("editButton", "is_open"),
	Input("collapse-button", "n_clicks"),
	prevent_initial_call=True
)
def openCollapsibleMenu(n_clicks):
	if n_clicks % 2 == 1:
		return True, True, True 
	else:
		return False, False, False


@callback(
	Output('my-toggle-switch-output', 'children'),
	Input('networkViewToggle', 'value'))
def update_network_view(value):
	if value:
		return 'Current network view: {}'.format("Network Overview")
	else:
		return 'Current network view: {}'.format("Layered View")
	

@callback(
	Output('cytoscape-callbacks-1', 'tapNodeData'),
	Input('cytoscape-callbacks-1', 'elements'),
	prevent_initial_call=True
)
def resetTapNodeData(elements):
	return None

@callback(
	Output('cytoscape-callbacks-1', 'elements'),
	Input('cytoscape-callbacks-1', 'tapNodeData'),
	Input('previousBranchButton', 'n_clicks'),
	State('cytoscape-callbacks-1', 'elements'),
	State('cytoscape-callbacks-1', 'tapNodeData'),
	prevent_initial_call=True
)
def displayNodeData(data, n_clicks, elements, nodeData):
	ctx = dash.callback_context
	global previous_branch

	if 'previousBranchButton' in ctx.triggered[0]['prop_id'].split('.')[0]:
		if previous_branch:
			previous_data = previous_branch.pop()
			return previous_data
		else:
			return elements
	# if not being called by tapNodeData, return --> used to counteract 
	# circular callback
	elif not ctx.triggered:
		return


	keys = list(data)
	branch_name = ""
	branch_id = ""

	for x in keys:
		if 'label' in x:
			branch_name = data[x]
		elif 'id' in x:
			branch_id = data[x]
	query = "SELECT branch_level FROM org_chart_branches WHERE branch_id=" + branch_id

	cursor.execute(query)
	current_level = cursor.fetchall()[0][0]

	if("Community" in current_level):
		print('lowest level reached')
		return elements
	previous_branch.append(elements)

	query = "SELECT child_branch_id FROM child_branches WHERE current_branch_id=" + branch_id

	cursor.execute(query)

	# Fetch the response of the query
	list_of_children = cursor.fetchall()

	# Convert the list of [(x,), (x,), (x,)]
	# to q regular list of (x, x, x)
	list_of_children = [int(i[0]) for i in list_of_children]

	# Fetch all branch names and ids
	query = "SELECT branch_id, branch_title FROM org_chart_branches WHERE branch_id IN (" + ','.join(str(x) for x in list_of_children) + ")"
	cursor.execute(query)
	title_id_tuples = cursor.fetchall()
	title_id_tuples= [(str(x[0]), str(x[1])) for x in title_id_tuples]

	nodes = [
	{
		'data': {'id': short, 'label': label},
		'position': {'x': 5 * int(short), 'y': -5 * int(short)}
	}
		for short, label in (
			title_id_tuples
		)
	]
	edges = []
	return nodes + edges

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


