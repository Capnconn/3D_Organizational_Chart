<<<<<<< HEAD
from dash import Dash, dcc, html, Input, Output, callback
from pages import AdminLoginPage, AddNewBranch, MainMenu
App = Dash(__name__, suppress_callback_exceptions=True)

App.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/LoginPage':
        return AdminLoginPage.layout
    elif pathname == '/MainMenu':
        return MainMenu.layout
    elif pathname == '/AddNewBranch':
        return AddNewBranch.layout
    else:
        return '404'


if __name__ == '__main__':
    App.run_server(debug=True)
||||||| empty tree
=======
from dash import Dash, dcc, html, Input, Output, callback
from pages import AdminLoginPage, AddNewBranch, DeletePage
App = Dash(__name__, suppress_callback_exceptions=True)

App.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])


@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/LoginPage':
        return AdminLoginPage.layout
    elif pathname == '/AddNewBranch':
        return AddNewBranch.layout;
    elif pathname == '/DeletePage':
        return DeletePage.layout
    elif pathname == '/MainMenu':
        return MainMenu.layout;
    else:
        return '404: page not found'


if __name__ == '__main__':
    App.run_server(debug=True)
>>>>>>> 5aca30f14c951e38e8c9dd4c304488e00dceb151
