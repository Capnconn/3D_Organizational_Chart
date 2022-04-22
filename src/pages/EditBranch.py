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



layout = html.Div(className='EditBranchMain', 
	children=[
      html.Div(className='AddBranchBody', 
			children=[
				html.H1('Edit a Team'),
				
				dcc.Dropdown(id="branch", options=branch_titles, placeholder="Select a branch to edit", multi=True),
				html.Br(),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '35px'}, placeholder="Enter a Branch Name"),
				html.Br(),
				
				html.Button('Edit', id='editBranchButton', className='addBranchCss'),
				html.Button('Home', id='homeButton', className='homeButtonCss', style={'position': 'relative'}),
				

                html.Br(),
				html.Img(className='bayerButton', src="/assets/img/bayer.png" , style={'height':'10%', 'width':'10%', 'left': '20px'}),
			],
			style={'paddingTop': '90px'}
		),
        
		html.Div(id='hidden_div_for_redirect_callback_edit_branch'),
		html.Div(id='hidden_div_for_redirect_callback_home_buttonEdit')
    ]
)

@callback(
	Output('hidden_div_for_redirect_callback_edit_branch', 'children'),
	Input('editBranchButton', 'n_clicks'),
	State('branch', 'value'),
	State('branchName', 'value'),
	prevent_initial_call=True
)
def handleEdit(n_clicks, branch, branchName):
	if not branch or not branchName:
		return html.P(("Empty Fields"), id="tempPEdit")

	else:
		str1 = str(''.join(branch))
		cursor.execute(
				"""UPDATE org_chart_branches 
				SET branch_title=%s
				WHERE branch_title=%s""", (branchName, str1))
				
		bayerdb.commit()
		return html.P(("For branch: " + str(branch)+ " - change: " + branchName), id="tempPEdit")


@callback(
	Output('hidden_div_for_redirect_callback_home_buttonEdit', 'children'),
	Input('homeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id="tempL")

