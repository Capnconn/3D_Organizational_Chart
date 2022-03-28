#Author: Ashlen Ashton
#Project: 3D_Org_Chart
#File: DeletePage.py
#Run: python3 App.py. Copy output into url bar. Append /deletePage
#Date: 03-18-2022

from dash import Dash, dcc, html, Input, Output, callback, State

layout = html.Div(className='DeletePageLayout',
    children=[
        html.H1("Delete a Link or Node", className="deleteNodeLabel"),
        html.Div(className="deleteLinkBody",
            children=[
                html.P("Link: ", id="currentLink", className="linkLabel"),
                dcc.Input(id="linkTitle", type="search", style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P(id='spacing'),
                html.Button("Delete Link", id="deleteLinkButton",className="deleteALink")
            ],
        ),
        
        html.Div(className="deleteNodeBody",
            children=[
                html.P("Node: ", id="currentNode", className="nodeLabel"),
                dcc.Input(id="nodeTitle", type="search",  style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P(id='spacing'),
                html.Button("Delete Node", id="deleteNodeButton", className="deleteANode")
            ],
            
        ),
        
        html.Button('Home', id='goHomeButton', className='goHome'),
        html.Div(id="hidden_div_for_redirect_callback_delete_link"),
        html.Div(id="hidden_div_for_redirect_callback-delete_node"),
        html.Div(id="hidden_div_for_redirect_callback_return_home")
    ]
)

@callback(
    Output('hidden_div_for_redirect_callback_delete_link', 'children'),
    Input('deleteLinkButton', 'n_clicks'),
    State('linkTitle', 'value'),
    prevent_initial_call=True
)

def handleDeleteLink(n_clicks, link):
    print((link))
    if not link:
        return html.P('*Link not found', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
    else:
        return html.P('*Link was deleted successfully', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '300px'})

@callback(
    Output('hidden_div_for_redirect_callback_delete_node', 'children'),
    Input('deleteNodeButton', 'n_clicks'),
    State('nodeTitle', 'value'),
    prevent_initial_call=True
)

def handleDeleteNode(n_clicks, node):
	print((link))
	if not link:
		return html.P('*Node not found', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
	else:
		return html.P('*Node was deleted successfully', id='tempP', style={'color': '#49af41', 'position': 'relative', 'bottom': '300px'})

@callback(
	Output('hidden_div_for_redirect_callback_return_home', 'children'),
	Input('goHomeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleReturnHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')