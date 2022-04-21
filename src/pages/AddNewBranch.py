from dash import Dash, dcc, html, Input, Output, callback, State
import mysql.connector

#Connect to database and create a cursor to interact with database
bayerdb = mysql.connector.connect(user='root', password='root', host='localhost', database='bayerdatabase')
cursor = bayerdb.cursor(buffered=True)

branch_levels = []

select_all_branch_levels = "SELECT branch_level FROM org_chart_branches"

cursor.execute(select_all_branch_levels)

next_level = cursor.fetchone()

while next_level is not None:
	
    next_branch_level_string = str(''.join(map(str, next_level)))

    branch_levels.append(next_branch_level_string)

    next_level = cursor.fetchone()
#removes duplicates for drop down menu
branch_levels = list(set(branch_levels))
# print(branch_levels)

branch_titles = []

select_all_branch_titles = "SELECT branch_title FROM org_chart_branches"

cursor.execute(select_all_branch_titles)

next_title = cursor.fetchone()

while next_title is not None:

    next_branch_title_string = str(''.join(map(str, next_title)))

    branch_titles.append(next_branch_title_string)

    next_title = cursor.fetchone()



layout = html.Div(className='AddNewBranchMain', 
	children=[
		html.H1('Add New Branch', style={'color':'white'}),

		html.Div(className='AddLevel', 
			children=[
				#html.P("Branch 1: ", id="Node1", className="node1Label"),
                dcc.Dropdown(id="branchLevel", options=branch_levels, placeholder="Select the level of the Branch"),
                html.P(id='spacing'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '35px'}, placeholder="Enter a Branch Name"),
				html.Br(),
				html.Br(),
				dcc.Input(id='numEmployees', type='number', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '35px'}, placeholder="Enter Number of Employees"),
				html.Br(),
				html.Br(),
				dcc.Input(id='branchDescription', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '35px'}, placeholder="Enter a Branch Description"),
				html.Br(),
				html.Br(),
			#style={'paddingTop': '90px'}
				dcc.Dropdown(id="branchEdges", options=branch_titles, placeholder="Select some dependencies for the new branch", multi=True),
				html.Br(),
				dcc.Input(id='edgeDescriptions', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '35px'}, placeholder="Enter a description for the relationship. Separate multiple descriptions with commas"),
				html.Br(),
				html.Br(),
				dcc.Dropdown(id="branchParent", options=branch_titles, placeholder="Select a parent for the new branch"),
				html.Br(),
				dcc.Dropdown(id="branchChildren", options=branch_titles, placeholder="Select some children for the new branch", multi=True)
			],
		),

		
		
		html.Button('Add Branch', id='addButton', className='addButtonCss', style={'position': 'relative', 'top': '180px'}),
		
		html.Button('Home', id='homeButton', className='homeButtonCss', style={'position': 'relative', 'top': '180px'}),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Img(className='bayerButton', src="/assets/img/bayer.png" , style={'height':'10%', 'width':'10%', 'left': '20px'}),
		html.Div(id='hidden_div_for_redirect_callback_add_branch'),
		html.Div(id='hidden_div_for_redirect_callback_home_button')
	]
)



@callback(
	Output('hidden_div_for_redirect_callback_add_branch', 'children'),
	Input('addButton', 'n_clicks'),
	State('branchLevel', 'value'),
	State('branchName', 'value'),
	State('numEmployees', 'value'),
	State('branchDescription', 'value'),
	State('branchEdges', 'value'),
	State('edgeDescriptions', 'value'),
	State('branchParent', 'value'),
	State('branchChildren', 'value'),
	prevent_initial_call=True
)
def handleAddBranch(n_clicks, level, branch, num, descriptions, edges, edgeDescriptions, parent, children):
	
	if not level or not branch or not num or not descriptions or not parent:
		return html.P('* Only child, edge, and edge description can be empty', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
	else:
		cursor.execute(
				"""INSERT INTO org_chart_branches 
				(branch_level, branch_title, num_of_employees, branch_description) 
				VALUES(%s, %s, %s, %s)""", (level, branch, num, descriptions))	
				
		bayerdb.commit()
		
		select_node_id = "SELECT branch_id FROM org_chart_branches WHERE branch_title = %s"

		cursor.execute(select_node_id, (branch,))

		current_match = cursor.fetchone()

		cursor.execute(select_node_id, (parent,))
		
		parent_match = cursor.fetchone()
	
		if current_match is not None and parent_match is not None:

			current_id = int(''.join(map(str, current_match)))
			parent_id = int(''.join(map(str, parent_match)))
		
			cursor.execute(
				"""INSERT INTO parent_branches 
				(current_branch_id, parent_branch_id) 
				VALUES(%s, %s)""", (current_id, parent_id))	
				
			bayerdb.commit()
		
		if children is not None:
			cursor.execute(select_node_id, (branch,))

			current_match = cursor.fetchone()
		
			for x in range(len(children)):
				cursor.execute(select_node_id, (children[x],))

				next_child_match = cursor.fetchone()
	
				if current_match is not None:

					current_match_id = int(''.join(map(str, current_match)))

					next_child_id = int(''.join(map(str, next_child_match)))

					cursor.execute(
						"""INSERT INTO child_branches 
						(current_branch_id, child_branch_id) 
						VALUES(%s, %s)""", (current_match_id, next_child_id))	
				
					bayerdb.commit()
					
		if edges is not None:
				
			edge_descriptions = []
		
			edge_descriptions.append(edgeDescriptions.split(", "))
			
			print(edge_descriptions)
			print(edgeDescriptions)
			
		
			cursor.execute(select_node_id, (branch,))

			current_match = cursor.fetchone()
		
			for x in range(len(edges)):
				for y in range(len(edge_descriptions[x])):
			
					print(edge_descriptions[x][y])
					cursor.execute(select_node_id, (edges[x],))

					next_edge_match = cursor.fetchone()

					if current_match is not None:

						current_match_id = int(''.join(map(str, current_match)))

						next_edge_id = int(''.join(map(str, next_edge_match)))

						cursor.execute(
							"""INSERT INTO edges
							(source_id, target_id, edge_description) 
							VALUES(%s, %s, %s)""", (current_match_id, next_edge_id, edge_descriptions[x][y]))	
				
						bayerdb.commit()
				
						cursor.execute(
							"""INSERT INTO edges
							(source_id, target_id, edge_description) 
							VALUES(%s, %s, %s)""", (next_edge_id, current_match_id, edge_descriptions[x][y]))	
				
						bayerdb.commit()
				
		return html.P(level + ' ' + branch + ' ' + str(num) + ' ' + descriptions + ' * Branch was added successfully', id='tempP', style={'color': 'white', 'position': 'relative', 'bottom': '80px'})

@callback(
	Output('hidden_div_for_redirect_callback_home_button', 'children'),
	Input('homeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')
