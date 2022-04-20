#Author: Ashlen Ashton
#Project: 3D_Org_Chart
#File: DeletePage.py
#Run: python3 App.py. Copy output into url bar. Append /deletePage
#Date: 03-18-2022

from dash import Dash, dcc, html, Input, Output, callback, State
import mysql.connector

#Connect to database and create a cursor to interact with database
bayerdb = mysql.connector.connect(user='root', password='root', host='localhost', database='bayerdatabase')
cursor = bayerdb.cursor(buffered=True)

branch_titles = []

select_all_branch_titles = "SELECT branch_title FROM org_chart_branches"

cursor.execute(select_all_branch_titles)

next_title = cursor.fetchone()

while next_title is not None:

    next_branch_title_string = str(''.join(map(str, next_title)))

    branch_titles.append(next_branch_title_string)

    next_title = cursor.fetchone()

print(branch_titles)

#Create a webpage with two textboxes, a "Home" button and a "delete" button
layout = html.Div(className='DeletePageLayout',
    children=[
        html.H1("Delete a branch from the network", className="deleteNodeLabel", style={'color':'white'}),
		html.P("Enter a title for Branch 1 to delete that organizational branch and all of its' connections from Bayer network. Enter titles for two branches to delete the connection between those two branches.", id="instructions", className="instructions"),
		html.Br(),
        html.Div(className="deleteNode1Body",
            children=[
                #html.P("Branch 1: ", id="Node1", className="node1Label"),
                dcc.Dropdown(id="node1Title", options=branch_titles, placeholder="Select a first branch to delete"),
                html.P(id='spacing'),
            ],
        ),
        
        html.Div(className="deleteNode2Body",
            children=[
                #html.P("Branch 2: ", id="Node2", className="node2Label"),
                dcc.Dropdown(id="node2Title", options=branch_titles, placeholder="Select a second branch to delete"),
                html.P(id='spacing'),
                
            ],
            
        ),
        
        html.Button("Delete Branch", id="deleteBranchButton", className="deleteABranch"),
        html.Button('Home', id='goHomeButton', className='goHome'),
        html.Br(),
        html.Img(className='bayerButton', src="/assets/img/bayer.png" , style={'height':'10%', 'width':'10%', 'left': '20px'}),
        html.Div(id="hidden_div_for_redirect_callback_delete_branch"),
        html.Div(id="hidden_div_for_redirect_callback_return_home")
    ]
)

#Whenever the delete button is clicked, send the user input from the dropdowns to the handler
@callback(
    Output('hidden_div_for_redirect_callback_delete_branch', 'children'),
    Input('deleteBranchButton', 'n_clicks'),
    State('node1Title', 'value'),
	State('node2Title', 'value'),
    prevent_initial_call=True
)

#Compares user input to branch titles in database. If user only provides one input and a match is found, data is deleted from org_level_branches, edges, parent_branches, and child_branches.
#If user provides two inputs with matches, the edge between the two nodes in the edges table is deleted. If no match is found for one or both inputs, an informative message is posted
#to the web page for the user.
def handleDeleteBranch(n_clicks, node1, node2):

    if not node1:
        return html.P('*Please enter a value for Branch 1', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '20px'})
    elif node1 and not node2:
        select_node1_id = "SELECT branch_id FROM org_chart_branches WHERE branch_title = %s"
    
        cursor.execute(select_node1_id, (node1,))
        
        match = cursor.fetchone()
        
        if match is not None:
        
            node1_id = int(''.join(map(str, match)))
        
            delete_all_node1_edges = "DELETE FROM edges WHERE source_id=%s OR target_id=%s"
        
            cursor.execute(delete_all_node1_edges, (node1_id,node1_id))
            
            bayerdb.commit()
        
            delete_node1 = "DELETE FROM child_branches WHERE current_branch_id=%s OR child_branch_id=%s"
        
            cursor.execute(delete_node1, (node1_id, node1_id,))
            
            bayerdb.commit()
            
            delete_node1 = "DELETE FROM parent_branches WHERE current_branch_id=%s OR parent_branch_id=%s"
        
            cursor.execute(delete_node1, (node1_id, node1_id,))
            
            bayerdb.commit()
            
            delete_node1 = "DELETE FROM org_chart_branches WHERE branch_id=%s"
        
            cursor.execute(delete_node1, (node1_id,))
            
            bayerdb.commit()
        
            return html.P('*Branch 1 was deleted successfully', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '20px'})
        
        else:
        
            return html.P('That title for Branch 1 was not found in the database.', id ='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '20px'})
        
        
    elif node1 and node2:
        
        select_node_id = "SELECT branch_id FROM org_chart_branches WHERE branch_title = %s"
    
        cursor.execute(select_node_id, (node1,))
        
        node1_match = cursor.fetchone()
    
        cursor.execute(select_node_id, (node2,))
        
        node2_match = cursor.fetchone()
        
        if node1_match is not None and node2_match is not None:
        
            node1_id = int(''.join(map(str, node1_match)))
            node2_id = int(''.join(map(str, node2_match)))
            
            delete_edge = "DELETE FROM edges WHERE source_id=%s AND target_id=%s"
        
            cursor.execute(delete_edge, (node1_id,node2_id))
            
            bayerdb.commit()

            cursor.execute(delete_edge,(node2_id, node1_id))

            bayerdb.commit()

            return html.P('*Connection between Branch 1 and Branch 2 deleted.', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '20px'})

        elif node1_match is None:

            return html.P('That title for Branch 1 was not found in the database.', id ='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '20px'})

        elif node2_match is None:

             return html.P('That title for Branch 2 was not found in the database.', id ='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '20px'})

        else:

             return html.P('Neither title was found in the database.', id ='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '20px'})

    else:

        return html.P('*Branch 2 cannot be the only entry', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '20px'})

    branch_titles = []

    select_all_branch_titles = "SELECT branch_title FROM org_chart_branches"

    cursor.execute(select_all_branch_titles)

    next_title = cursor.fetchone()

    while next_title is not None:

        next_branch_title_string = str(''.join(map(str, next_title)))

        branch_titles.append(next_branch_title_string)

        next_title = cursor.fetchone()

#When the "Home" button is clicked, return to Main Menu
@callback(
	Output('hidden_div_for_redirect_callback_return_home', 'children'),
	Input('goHomeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleReturnHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')
