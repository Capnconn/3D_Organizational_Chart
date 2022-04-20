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
print(branch_levels)


layout = html.Div(className='AddNewBranchMain', 
	children=[
		html.H1('Add New Branch', style={'color':'white'}),

		html.Div(className='AddLevel', 
			children=[
				#html.P("Branch 1: ", id="Node1", className="node1Label"),
                dcc.Dropdown(id="branchLevel", options=branch_levels, placeholder="Select the level of the Branch"),
                html.P(id='spacing'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}, placeholder="Enter a Branch Name"),
				html.Br(),
				dcc.Input(id='numEmployees', type='number', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}, placeholder="Enter Number of Employees"),
				html.Br(),
				dcc.Input(id='branchDescription', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}, placeholder="Enter a Branch Description"),
			],
			#style={'paddingTop': '90px'}
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
	prevent_initial_call=True
)
def handleAddBranch(n_clicks, level, branch, num, descriptions):
	
	if not level or not branch or not num or not descriptions:
		return html.P('* Invalid branch name', id='tempP', style={'color': '#cc0000', 'position': 'relative', 'bottom': '300px'})
	else:
		cursor.execute(
				"""INSERT INTO org_chart_branches 
				(branch_level, branch_title, num_of_employees, branch_description) 
				VALUES(%s, %s, %s, %s)""", (level, branch, num, descriptions))	
				
		bayerdb.commit()


		return html.P(level + ' ' + branch + ' ' + str(num) + ' ' + descriptions + ' * Branch was added successfully', id='tempP', style={'color': 'white', 'position': 'relative', 'bottom': '80px'})

@callback(
	Output('hidden_div_for_redirect_callback_home_button', 'children'),
	Input('homeButton', 'n_clicks'),
	prevent_initial_call=True
)
def handleHome(n_clicks):
	return dcc.Location(pathname='/MainMenu', id='tempL')