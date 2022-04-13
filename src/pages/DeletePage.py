#Author: Ashlen Ashton
#Project: 3D_Org_Chart
#File: DeletePage.py
#Run: python3 App.py. Copy output into url bar. Append /deletePage
#Date: 03-18-2022

from dash import Dash, dcc, html, Input, Output, callback, State
import mysql.connector

connection = mysql.connector.connect(user='root', password='root', host='localhost', database='bayerdatabase')
bayerdb = connection.cursor()

layout = html.Div(className='DeletePageLayout',
    children=[
        html.H1("Delete a branch from the network", className="deleteNodeLabel", style={'color':'white'}),
		html.P("Enter a title for Node 1 to delete that organizational branch and all of its' connections from Bayer network. Enter titles for two nodes to delete the connection between those two nodes.", id="instructions", className="instructions"),
		html.Br(),
        html.Div(className="deleteNode1Body",
            children=[
                html.P("Node 1: ", id="Node1", className="node1Label"),
                dcc.Input(id="node1Title", type="search", style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P(id='spacing'),
            ],
        ),
        
        html.Div(className="deleteNode2Body",
            children=[
                html.P("Node 2: ", id="Node2", className="node2Label"),
                dcc.Input(id="node2Title", type="search",  style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P(id='spacing'),
                
            ],
            
        ),
        
        html.Button("Delete Branch", id="deleteBranchButton", className="deleteABranch"),
        html.Button('Home', id='goHomeButton', className='goHome'),
        html.Div(id="hidden_div_for_redirect_callback_delete_branch"),
        html.Div(id="hidden_div_for_redirect_callback_return_home")
    ]
)

@callback(
    Output('hidden_div_for_redirect_callback_delete_branch', 'children'),
    Input('deleteBranchButton', 'n_clicks'),
    State('node1Title', 'value'),
	State('node2Title', 'value'),
    prevent_initial_call=True
)

def handleDeleteBranch(n_clicks, node1, node2):

    if not node1:
        return html.P('*Please enter a value for Node 1', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
    elif node1 and node2:
        return html.P('*Connection between node1 and node2 deleted.', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '300px'})
    else:
        return html.P('*Node 1 was deleted successfully', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '300px'})

@callback(
	Output('hidden_div_for_redirect_callback_return_home', 'children'),
	Input('goHomeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleReturnHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')