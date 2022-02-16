#Author: Ashlen Ashton
#Project: Bayer 3D Org Chart
#File: readcsv.py
#Date: 2-10-2022
#Execute: python3 readcsv.py (Linux Ubuntu Command Line)

import mysql.connector
import csv

#read_csv has two functions: read_csv_file inputs fields from file into global lists. 
#write_csv_to_database then reads in a record into the database by assigning the appropriate index of each list to their corollary fields in the database table
class read_csv:
	
	level = []
	title = []
	num_employees = []
	description = []
	record_count = 0
	
	def read_csv_file(self, file_name):
	
		
		file = open(file_name)
		csvreader = csv.reader(file)
		
		for row in csvreader:
			self.level.append(row[0])
			self.title.append(row[1])
			self.num_employees.append(row[2])
			self.description.append(row[3])
			self.record_count += 1
			
		# print(self.level)
		# print(self.title)
		# print(self.num_employees)
		# print(self.description)
		print(self.record_count)
		file.close()
		
	def write_csv_to_database(self):
		bayerdb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="root",
		database="bayerdatabase"
		)
		
		cursor = bayerdb.cursor()
		
		for x in range(self.record_count):
			cursor.execute(
				"""INSERT INTO org_chart_branches 
				(branch_level, branch_title, num_of_employees, branch_description) 
				VALUES(%s, %s, %s, %s)""", (self.level[x], self.title[x], self.num_employees[x], self.description[x]))
				
			bayerdb.commit() #required to update database through python
		
		cursor.execute("SELECT * FROM org_chart_branches")
		
		display_records = cursor.fetchall() #fetches all matches from last executed statement
		
		for x in display_records:
			print(x)

#Driver for program
if __name__ == '__main__':

	test = read_csv()
	test.read_csv_file("test.csv")
	test.write_csv_to_database()