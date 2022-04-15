# 3D_Organizational_Chart

#Dash library was used in conjunction with MySQL for Python to create a 3-tier web application to display a network of Bayer's organization

*********Framework Used to Facilitate GUI*********

-Dash
	Python library used for data visualizations
	Requires a specific file structure
		src: source folder that contains executablee, CSS file(s), and pages that make up the web app
		assets: subfolder of src; contaons CSS
		pages: subfolder of src; contains webpages of app
	Resources:
		example of multi-page Dash App on YouTube: https://youtu.be/RMBSQ6leonU
		Information on callback methods within Dash Apps: https://dash.plotly.com/basic-callbacks
		
*********MySQL with Python*********

Python uses a mysql.connector library to connect to MySQL databases. After a connection is made, a cursor is used to execute queries. 
The queries used to create the tables in the bayerdatabase (and to edit them) are parameterized. User-input values are added to the queries to add interactivity to the network.

The database is created by hand. Executing bayerdb.py will create all of the necessary tables. Executing readcsv.py will populate all of the tables.

CAUTION: MySQL results are returned as tuples! Special conversions are needed to manipulate them in Python:

#converting a MySQL tuple to an int using map to tie each result to a string, then converting that string to an int.
target_id = int(''.join(map(str, cursor.fetchone()))) 

#Reading a tuple from a MySQL query  and then storing each datum in the set as separate Python data types
cursor.execute("""SELECT branch_id, branch_title FROM org_chart_branches WHERE branch_level='Division'""");
division_tuple = cursor.fetchall()

division_tuple = [(str(x[0]), str(x[1])) for x in division_tuple]

nodes = [
	{
		'data': {'id': short, 'label': label},
		'position': {'x': 5 * int(short), 'y': -5 * int(short)}
	}
	for short, label in (
		division_tuple
	)
] 

***********About the Dataset*************

The data for the App is stored in demo_data.csv. It will populate the org_chart_branches, edges, parent, and children tables in the database.
Column labels from left to right:

Organizational Level		Branch Title		Number of Employees		Branch Description		List of Dependent Teams/Edges			Edge Descriptions 		 Parent Branch			List of Child Branches

