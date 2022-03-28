from dash import Dash, dcc, html, Input, Output, callback, State

layout = html.Div(className='EditBranchMain', 
	children=[
      html.Div(className='AddBranchBody', 
			children=[
				html.H1('Edit a Branch'),
				html.P('Select Branch:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
				html.P('New info 1:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P('New info 2:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P('New info 3:', id='branchNameP', className='paragraphCredential'),
				dcc.Input(id='branchName', type='text', style={'marginTop': '50px', 'margin': '-10px', 'width': '50%', 'borderRadius': '7px', 'border': '1px solid grey', 'height': '20px'}),
                html.P(id='spacing'),
				html.Button('Edit', id='addBranchButton', className='addBranchCss'),
                html.P('Current Info 1: xxxxxx', id='branchNameP', className='paragraphCredential'),
                 html.P('Current Info 2: xxxxxx', id='branchNameP', className='paragraphCredential'),
                  html.P('Current Info 3: xxxxxx', id='branchNameP', className='paragraphCredential'),
			],
			style={'paddingTop': '90px'}
		),
        html.Button('Home', id='homeButton', className='homeButtonCss', style={'position': 'relative', 'top': '180px'}),
		html.Div(id='hidden_div_for_redirect_callback_add_branch'),
		html.Div(id='hidden_div_for_redirect_callback_home_button')
    ]
)

