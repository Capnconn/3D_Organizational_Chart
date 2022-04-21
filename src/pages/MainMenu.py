from platform import node
from dash import Dash, dcc, html, Input, Output, callback, State, callback_context
import dash_cytoscape as cyto
import dash_daq as daq
import dash_bootstrap_components as dbc
from flask import g
import mysql.connector

import chart_studio.plotly as py
from numpy import newaxis
import plotly.graph_objs as go
import igraph as ig
import plotly.figure_factory as ff

from plotly.offline import iplot

cyto.load_extra_layouts()


previous_branch = []
bayerdb = []
curosr = []
fig = []
nodes_clicked = []
initial_elements = []
node_data = {}
nodes_in_network = []
edges_in_network = {}


#############################################################################################
# Initialize network on layered view, and with nodes
# at the highest level (Division).
# Initialize here rather than with initial callback,
# because this produces quicker results when the web page loads
def initialzeNetworkLayered():
	styles = {
	    'pre': {
	        'border': 'thin lightgrey solid',
	        'overflowX': 'scroll'
	    }
	}

	global bayerdb
	# Query the database for the top level of nodes
	bayerdb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database="bayerdatabase"
	)
	global cursor
	cursor = bayerdb.cursor(buffered=True);
	cursor.execute("""SELECT * FROM org_chart_branches WHERE branch_level='Division'""");
	query_results = cursor.fetchall()

	# division_tuple = [(str(x[0]), str(x[2])) for x in division_tuple]
	division_tuple = []
	global node_data
	global nodes_in_network
	nodes_in_network = []
	node_data = {}
	for x in query_results:
		nodes_in_network.append(str(x[0]))
		division_tuple.append((str(x[0]), str(x[2])))
		node_data[str(x[0])] = {}
		node_data[str(x[0])]["level"] = str(x[1])
		node_data[str(x[0])]["num_employees"] = str(x[3])
		node_data[str(x[0])]["description"] = str(x[4])
		node_data[str(x[0])]["parent"] = "None";
  
	nodes_in_network = list(set(nodes_in_network))

		
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

	global initial_elements
	initial_elements = elements
	print(elements)

	return (cyto.Cytoscape(
				userZoomingEnabled=False,
				id='cytoscape-callbacks-1',
				elements=elements,
				style={'width': '100%', 'height': '400px'},
				layout={
					'name': 'random', 'animate': True, 'animationDuration': 2000
				},
				stylesheet=[
        			{
						'selector': 'node',
						'style': {
							'label': 'data(label)'
						}
					},
					{
						'selector': 'edge',
						'style': {
							'curve-style': 'bezier'
						}
					},
     				{
						'selector': 'data(id)',
						'style': {
							'source-arrow-shape': 'triangle',
                		}
					}
				]
			),
	    	html.P(id='cytoscape-callbacks-1-hoverNode-output'),
    		html.P(id='cytoscape-callbacks-1-hoverEdge-output')
    	)

elements = initialzeNetworkLayered()
#############################################################################################

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
						label='Layered View',
						labelPosition='bottom',
						color='green',
						size=50				
					),
					html.Div(id='my-toggle-switch-output')
				]
			),
			html.Div(className='previousBranchDivCss', children=
				[
					html.P("Previous Branch: x", id='previous-branch', className='previousBranchCss', style={'display': 'none'}),
					html.Button('Previous Branch', id='previousBranchButton', className='previousBranchButtonCss')
				]
			),
			html.Div(id='network_Placement', className='mainMenuNetwork', children=
				[
				]
			),		
		html.Div(id='redirect_add_branch'),
		html.Div(id='redirect_delete_branch'),
		html.Div(id='redirect_edit_branch'),
		html.Div(id='new_Network')
	]
)

@callback(
	Output('cytoscape-callbacks-1-hoverEdge-output', 'children'),
	Input('cytoscape-callbacks-1', 'mouseoverEdgeData'),
 	Input('cytoscape-callbacks-1', 'tapEdgeData'),
	prevent_initial_call=True
)
def displayEdgeData(data1, data2):
	hoveredNode = data1['id']
	print(data1)
	print(edges_in_network)
	return edges_in_network[hoveredNode]

@callback(
	Output('cytoscape-callbacks-1-hoverNode-output', 'children'),
	Input('cytoscape-callbacks-1', 'mouseoverNodeData'),
	prevent_initial_call=True
)
def displayHoverNodeData(data):
	hoveredNode = data['id']
	return [data['label'], ":", html.Br(), "Level: ", node_data[hoveredNode]["level"], html.Br(), "Number of employees: ", node_data[hoveredNode]["num_employees"], html.Br(), "Description: ", node_data[hoveredNode]["description"]]

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
	Output('network_Placement', 'children'),
	Input('networkViewToggle', 'value')
)
def displayNetwork(value):
	if value:
		return createNetwork()
	elif not value:
		global nodes_clicked
		nodes_clicked = []
		return initialzeNetworkLayered()

@callback(
	Output('cytoscape-callbacks-1', 'elements'),
	Input('cytoscape-callbacks-1', 'tapNodeData'),
	State('cytoscape-callbacks-1', 'elements'),
	prevent_initial_call=True
)
def retreiveTappedNodeInfo(data, elements):
	if not data:
		return elements

	keys = list(data)
	branch_name = ""
	branch_id = ""

	for x in keys:
		if 'label' in x:
			branch_name = data[x]
		elif 'id' in x:
			branch_id = data[x]


	global nodes_clicked
	if branch_name in nodes_clicked:
		return elements
		print("return1")
	else:
		nodes_clicked.append(branch_name)

	# Query for the children of the clicked node
	query = "SELECT child_branch_id FROM child_branches WHERE current_branch_id=" + branch_id
	cursor.execute(query)
	children_list = cursor.fetchall()
 
	query = "SELECT * FROM edges WHERE source_id=" + branch_id
	cursor.execute(query)
	query_results = cursor.fetchall()
 
	print(query_results)
 
	if not children_list and not query_results:
		print("returning no")
		return elements

	new_node_dependencies = []
	dependency_list = []

	# If there are dependencies:
	if query_results:
     
		global edges_in_network
		# convert dependency list to a list of ID's
		# dependency_list = [(str(x[0]), str(x[1])) for x in dependency_list]
		dependency_list = []
		for dependency in query_results:
			dependency_list.append((str(dependency[0]), str(dependency[1])))
			edges_in_network[str(dependency[0])+str(dependency[1])] = dependency[2]	

		print(dependency_list)
		
		# Query for the nodes of the target_id
		query = "SELECT * FROM org_chart_branches WHERE branch_id IN (" + ','.join(str(x[1]) for x in dependency_list) + ")"
		cursor.execute(query)
		query_results = cursor.fetchall()
  
		query = "SELECT * FROM parent_branches WHERE current_branch_id IN (" + ','.join(str(x[1]) for x in dependency_list) + ")"
		cursor.execute(query)	
		parent_results_list = cursor.fetchall() 

		global nodes_in_network
		global node_data
		for x in query_results:
			if str(x[0]) not in nodes_in_network and (str(x[0]), str(x[1])) not in edges_in_network:
				new_node_dependencies.append((str(x[0]), str(x[2])))
				node_data[str(x[0])] = {}
				node_data[str(x[0])]["level"] = str(x[1])
				node_data[str(x[0])]["num_employees"] = str(x[3])
				node_data[str(x[0])]["description"] = str(x[4])
				nodes_in_network.append(str(x[0]))
    
		# Assign the proper parent to each dependency node
		for x in parent_results_list:
			node_data[str(x[0])]["parent"] = str(x[1])
   
	# If there are children of the tapped node:
	if children_list:
		# Convert query results to list of node_id strings
		children_list = [str(x[0]) for x in children_list]
  
		# Query for the information of the children node of the tapped node
		query = "SELECT * FROM org_chart_branches WHERE branch_id IN (" + ','.join(str(x) for x in children_list) + ")"
		cursor.execute(query)
		query_results = cursor.fetchall()
  
		# Assign the data to the dict, so we can reference this data easier for hovering over node
		# and check if the node is already in the ndetwork - prevent identical nodes in the same network
		for x in query_results:
			if str(x[0]) not in nodes_in_network:
				new_node_dependencies.append((str(x[0]), str(x[2])))
				node_data[str(x[0])] = {}
				node_data[str(x[0])]["level"] = str(x[1])
				node_data[str(x[0])]["num_employees"] = str(x[3])
				node_data[str(x[0])]["description"] = str(x[4])
				node_data[str(x[0])]["parent"] = branch_name
				nodes_in_network.append(str(x[0]))
    
	print(new_node_dependencies)
	print("============================================================================================")
	print(query_results)
 
	if not new_node_dependencies and not query_results:
		print("old elements")
		return elements
   
	nodes = [
	{
		'data': {'id': short, 'label': label},
	}
		for short, label in (
			new_node_dependencies
		)
	]

	edges = [
	{
		'data': {'id':source+target, 'source': target, 'target': source}
	}
		for source, target in (
			dependency_list
		)

	]
 
	new_elements = nodes + edges
	
	updated_elements = new_elements + elements
	if updated_elements == elements:
		print('same')
		return elements
	else:
		print("not the same")
		return updated_elements    

	# # If no children, return
	# if children_list:

	# 	children_list = [str(x[0]) for x in children_list]

	# 	# Query for the dependencies of the children of the selected node
	# 	query = "SELECT source_id,target_id FROM edges WHERE source_id IN (" + ','.join(str(x) for x in children_list) + ")"
	# 	cursor.execute(query)
	# 	dependency_list = cursor.fetchall()
		
	# 	# Convert fetched dependencies to strings
	# 	dependency_list = [(str(x[0]), str(x[1])) for x in dependency_list]

	# 	new_node_list = []

	# # If there are dependencies among the children nodes of the clicked node, then proceed with finding these dependency nodes, if not, skip
	# if dependency_list:
	# 	# Create list of new nodes to add - need to add new nodes to complete dependency edges for children of the selected node
	# 	new_node_list = [x[1] for x in dependency_list]

	# 	# Query for the nodes to complete the dependency edges for the children of the selected node
	# 	query = "SELECT * FROM org_chart_branches WHERE branch_id IN (" + ','.join(str(x) for x in new_node_list) + ")"
	# 	cursor.execute(query)
	# 	query_results = cursor.fetchall()

	# 	# Convert the new node_list values to strings
	# 	new_node_list = []
	# 	global nodes_in_network
	# 	global node_data
	# 	for x in query_results:
	# 		if str(x[0]) not in nodes_in_network:
	# 			new_node_list.append((str(x[0]), str(x[2])))
	# 			node_data[str(x[0])] = {}
	# 			node_data[str(x[0])]["level"] = str(x[1])
	# 			node_data[str(x[0])]["num_employees"] = str(x[3])
	# 			node_data[str(x[0])]["description"] = str(x[4])
	# 			# node_data[str(x[0])]["parent"] = 
	# 			nodes_in_network.append(str(x[0]))

	# # Now query for the rest of the information of the children nodes (branch_title)
	# query = "SELECT * FROM org_chart_branches WHERE branch_id IN (" + ','.join(str(x) for x in children_list) + ")"
	# cursor.execute(query)
	# query_results = cursor.fetchall()

	# # Convert the children_list values to strings
	# children_list = []
	# for x in query_results:
	# 	if str(x[0]) not in nodes_in_network:
	# 		children_list.append((str(x[0]), str(x[2])))
	# 		node_data[str(x[0])] = {}
	# 		node_data[str(x[0])]["level"] = str(x[1])
	# 		node_data[str(x[0])]["num_employees"] = str(x[3])
	# 		node_data[str(x[0])]["description"] = str(x[4])
	# 		node_data[str(x[0])]["parent"] = branch_name
	# 		nodes_in_network.append(str(x[0]))

	# # Combine nodes to add lists
	# total_new_nodes = children_list + new_node_list
 
	# if not total_new_nodes and not dependency_list:
	# 	print('returning now')
	# 	return elements

	# nodes = [
	# {
	# 	'data': {'id': short, 'label': label},
	# }
	# 	for short, label in (
	# 		total_new_nodes
	# 	)
	# ]

	# edges = [
	# {
	# 	'data': {'source': source, 'target': target}
	# }
	# 	for source, target in (
	# 		dependency_list
	# 	)

	# ] 

	# new_elements = nodes + edges
	# num_edges = 0
	# new_elements_after = new_elements + elements
	# for x in new_elements_after:
	# 	if 'source' in x['data'].keys():
	# 		num_edges += 1
	# print(num_edges)

	# return new_elements + elements

def goToNextLayer(data, elements):
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
		return elements
	global previous_branch
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

def initializeNetworkOverview():
	query = "SELECT branch_id, branch_title FROM org_chart_branches"
	cursor.execute(query)
	node_list = cursor.fetchall()
	node_list = [(str(x[0]), str(x[1])) for x in node_list]
	
	nodes = [
	{
		'data': {'id': short, 'label': label},
		'position': {'x': 5 * int(short), 'y': -5 * int(short)}
	}
		for short, label in (
			node_list
		)
	]

	query = "SELECT source_id, target_id FROM edges";
	cursor.execute(query)
	edge_list = cursor.fetchall()
	edge_list = [(str(x[0]), str(x[1])) for x in edge_list]

	edges = [
	{
		'data': {'source': source, 'target': target}
	}
		for source, target in (
			edge_list
		)

	]


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


def createNetwork():
	query = "SELECT branch_level, branch_title, branch_id FROM org_chart_branches"
	cursor.execute(query)
	node_list = cursor.fetchall()
	level = []
	node_id = []
	labels = []
	node_edge = {}
	highest_num = 0
	for node in node_list:

		if "Division" in node[0]:
			level.append(1)
		elif "Department" in node[0]:
			level.append(2)
		elif "Platform" in node[0]:
			level.append(3)
		elif "Community" in node[0]:
			level.append(4)

		labels.append(node[1])
		if int(node[2]) > highest_num:
			highest_num = int(node[2])

		node_id.append(node[2])
		node_edge[node[2]] = node[1]
		# or
		# labels.append(node[0])
  
	print(node_edge)

	print(node_id)
	N = len(node_list)
	# print(labels)
	# print(N)



	# for x in range(N):
	# 	print("(" + str(node_id[x]) + "," + str(labels[x]) +")")


	# query = "SELECT source_id, target_id FROM edges"
	# cursor.execute(query)

	# edge_list = cursor.fetchall()
	edges = []
	# for edge in edge_list:
	# 	edges.append((edge[0], edge[1]))

	query = "SELECT * FROM edges"
	cursor.execute(query)

	child_list = cursor.fetchall()

	edge_description_list = []

	for child in child_list:
		edges.append((child[0], child[1]))
		edge_description_list.append(child[2])	

	# no_double_edges = []

	# for edge in edges:
	# 	if edge not in no_double_edges and edge[::-1] not in no_double_edges:
	# 		no_double_edges.append(edge)
	edges = [(int(x[0]), int(x[1])) for x in edges]

	
	G = ig.Graph(edges, directed=False)

	layt = G.layout('kk', dim=3)

	Xn = []
	Yn = []
	Zn = []
 
	newXn = []
	newYn = []
	newZn = []

	# print(len(layt))

	for x in range(0,highest_num+1):
		Xn += [layt[x][0]]
		Yn += [layt[x][1]]
		Zn += [layt[x][2]]
		if x in node_id:
			print(x)
			newXn.append(Xn[x])
			newYn.append(Yn[x])
			newZn.append(Zn[x])

	Xe=[]
	Ye=[]
	Ze=[]

	for e in edges:
		Xe += [layt[e[0]][0], layt[e[1]][0], None]
		Ye += [layt[e[0]][1], layt[e[1]][1], None]
		Ze += [layt[e[0]][2], layt[e[1]][2], None]
  
	Xm = []
	Ym = []
	Zm = []

	for e in edges:
		xMid = (layt[e[0]][0] + layt[e[1]][0]) / 2
		yMid = (layt[e[0]][1] + layt[e[1]][1]) / 2
		zMid = (layt[e[0]][2] + layt[e[1]][2]) / 2

		Xm.append(xMid)
		Ym.append(yMid)
		Zm.append(zMid)
	
	trace1=go.Scatter3d(x=Xe,
		y=Ye,
		z=Ze,
		mode='lines',
		line=dict(color='rgb(125,125,125)', width=1),
		hoverinfo='none'
	)
	trace2=go.Scatter3d(
		x=newXn,
		y=newYn,
		z=newZn,
		mode='markers',
		name='actors',
		marker=dict(symbol='circle', size=6, color=level, colorscale='Viridis', line=dict(color='rgb(00,00,00)', width=0.5)),
		text=labels,
		hoverinfo='text'
	)

	trace3=go.Scatter3d(
		x=Xm,
		y=Ym,
		z=Zm,
		mode='markers',
		opacity=0,
		marker_size=5,
		text=edge_description_list,
		hoverinfo='text'
	)

	axis=dict(showbackground=False,
		showline=False,
		zeroline=False,
		showgrid=False,
		showticklabels=False,
		title=''
	)
	layout = go.Layout(
		width=1000,
		height=1000,
		showlegend=False,
		scene=dict(
			xaxis=dict(axis),
			yaxis=dict(axis),
			zaxis=dict(axis),
		)
	)

	data=[trace1, trace2, trace3]

	global figure
	fig=go.Figure(data=data, layout=layout)
	print(fig)

	return dcc.Graph(figure=fig)

	# fig.write_html("network.html")

	# fig.show()
	# py.iplot(fig, filename='Les-Miserables')
	# iplot(fig, filename='Les-Miserables')





