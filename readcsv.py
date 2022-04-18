#Author: Ashlen Ashton
#Project: Bayer 3D Org Chart
#File: readcsv.py
#Date: 2-10-2022
#Execute: python3 readcsv.py (Linux Ubuntu Command Line)

import mysql.connector
import csv

#read_csv has two functions: read_csv_file inputs fields from file into global lists. 
#write_csv_to_database then reads in a record into the database by assigning the appropriate index of each list to their corollary fields in the database tables
class read_csv:
	
	level = []
	title = []
	num_employees = []
	description = []
	edge_dependencies = []
	edge_descriptions = []
	parent = []
	children = []
	record_count = 0
	
	#the columns of each ro are read into their respective lists. record_count is incremented for each row to be used when writing data to database
	
	def read_csv_file(self, file_name):
	
		
		file = open(file_name)
		csvreader = csv.reader(file)
		
		for row in csvreader:
			self.level.append(row[0])
			self.title.append(row[1])
			self.num_employees.append(row[2])
			self.description.append(row[3])
			edge_dependencies_string = row[4]
			edge_descriptions_string = row[5]
			self.parent.append(row[6])
			children_string = row[7]
			
			self.edge_dependencies.append(edge_dependencies_string.split(", "))
			self.edge_descriptions.append(edge_descriptions_string.split(", "))
			self.children.append(children_string.split(", "))
			
			self.record_count += 1
			
		# print(self.level)
		# print(self.title)
		# print(self.num_employees)
		# print(self.description)
		# print(self.edge_dependencies)
		# print(self.edge_descriptions)
		# print(self.record_count)
		file.close()
		
		#Connect to the database. Lines 71-75 read each record into org_chart_branches, which contains details of individual teams
		#Lines 86-111 read edge info of each team into the edges table. 117-136 fo parent_branches. 141-165 for child_branches.
		
	def write_csv_to_database(self):
		bayerdb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database="bayerdatabase"
		)
		
		cursor = bayerdb.cursor(buffered=True)
		
		for x in range(self.record_count):
			cursor.execute(
				"""INSERT INTO org_chart_branches 
				(branch_level, branch_title, num_of_employees, branch_description) 
				VALUES(%s, %s, %s, %s)""", (self.level[x], self.title[x], self.num_employees[x], self.description[x]))
				
			bayerdb.commit() #required to update database through python.
		
		#cursor.execute("SELECT * FROM org_chart_branches")
		
		#display_records = cursor.fetchall() #fetches all matches from last executed statement
		
		#for x in display_records:
			# print(x)
			# print("\n")
		
		for x in range(self.record_count):
			record_dependencies = len(self.edge_dependencies[x])
			for y in range(record_dependencies):
				dependent_branch_title = self.edge_dependencies[x][y]
				dependent_branch_title = dependent_branch_title.strip()
				dependent_branch_edge_description = self.edge_descriptions[x][y]
				dependent_branch_edge_description = dependent_branch_edge_description.strip()
				
				select_branch_id = "SELECT branch_id FROM org_chart_branches WHERE branch_title = %s"
				
				cursor.execute(select_branch_id, (self.title[x],))
				
				source_id = int(''.join(map(str, cursor.fetchone())))#Converts tuple returned by MySQL into an int
				
				if(dependent_branch_title != "None"):
				
					cursor.execute(select_branch_id, (dependent_branch_title,))
				
					target_id = int(''.join(map(str, cursor.fetchone())))
				
					cursor.execute(
					"""INSERT INTO edges
					(source_id, target_id, edge_description)
					VALUES(%s, %s, %s)""", (source_id, target_id, dependent_branch_edge_description))
				
					bayerdb.commit()
					
				else:
					print("There is no associated id for branch title " + dependent_branch_title)
				
				
		for x in range(self.record_count):
		
			select_branch_id = "SELECT branch_id FROM org_chart_branches WHERE branch_title = %s"
			
			cursor.execute(select_branch_id, (self.title[x],))
			
			current_branch_id = int(''.join(map(str, cursor.fetchone())))
			
			if(self.parent[x] != "None"):
			
				cursor.execute(select_branch_id, (self.parent[x],))
			
				parent_branch_id = int(''.join(map(str, cursor.fetchone())))
			
				cursor.execute(
				"""INSERT INTO parent_branches
			(	current_branch_id, parent_branch_id)
				VALUES(%s, %s)""", (current_branch_id, parent_branch_id))
			
				bayerdb.commit()
			
			else:
				print(self.title[x] + " has no parent.")
			
		for x in range(self.record_count):
			record_children = len(self.children[x])
			for y in range(record_children):
				child_branch_title = self.children[x][y]
				
				select_branch_id = "SELECT branch_id FROM org_chart_branches WHERE branch_title = %s"
			
				cursor.execute(select_branch_id, (self.title[x],))
			
				current_branch_id = int(''.join(map(str, cursor.fetchone())))
				
				#print(child_branch_title)
				
				if(child_branch_title != "None"):
			
					cursor.execute(select_branch_id, (child_branch_title,))
			
					child_branch_id = int(''.join(map(str, cursor.fetchone())))
			
					cursor.execute(
					"""INSERT INTO child_branches
					(current_branch_id, child_branch_id)
					VALUES(%s, %s)""", (current_branch_id, child_branch_id))
				
					bayerdb.commit()
					
				else:
				
					print(self.title[x] + " has no children.")
			
		

#Driver for program
if __name__ == '__main__':

	test = read_csv()
	test.read_csv_file("demo_data.csv")
	test.write_csv_to_database()