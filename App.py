from dash import Dash, dcc, html, Input, Output, callback
from pages import AdminLoginPage, AddNewBranch
App = Dash(__name__)


App.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/AdminLoginPage':
        return AdminLoginPage.layout
    elif pathname == '/AddNewBranch':
        return AddNewBranch.layout
    else:
        return '404'

if __name__ == '__main__':
    App.run_server(debug=True)