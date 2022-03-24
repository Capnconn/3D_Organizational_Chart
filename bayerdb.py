#Author: Ashlen Ashton
#Date: January 30, 2022
#File: bayerdb.py
#exe instructions: python3 bayerdb.py (Linux Ubuntu). Uncomment lines 28-36 if running first time
#comment 28-36 for subsequent runs. Run MySQL Sever prior to execution

#Lines 13-20 establish connection to server and create a cursor object to interact w/ MySQL
#Lines 22-26, 39-47, 49-57 create tables w/in bayerdatabase
#Lines 28-36 insert values into org_levels
#Lines 58-61 confirm all three tables were created
import mysql.connector

bayerdb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root",
    database="bayerdatabase"
	)
    
cursor = bayerdb.cursor()

cursor.execute(
"""CREATE TABLE IF NOT EXISTS org_levels
    ( level VARCHAR(255) PRIMARY KEY, 
    description VARCHAR(255))"""
)

insert_level_into_org_levels = "INSERT INTO org_levels (level, description) VALUES (%s, %s)"
vals = [
   ("Division", "Highest level of Bayer's business model; contains Crop Science, Pharmaceuticals, and Consumer Health industries"),
   ("Department", "Secondary level; focused interest areas w/in each division"),
   ("Platform", "Tertiary level that contributes functionality to departments"),
   ("Community", "Quarternary level that handles individual roles that make up platform tasks")
]

cursor.executemany(insert_level_into_org_levels, vals)


cursor.execute(
"""CREATE TABLE IF NOT EXISTS org_chart_branches
    (branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_level VARCHAR(255),
    branch_title VARCHAR(255),
    num_of_employees INT NOT NULL,
    branch_description VARCHAR(255),
    FOREIGN KEY(branch_level) REFERENCES org_levels(level))"""
)

cursor.execute(
"""CREATE TABLE IF NOT EXISTS edges
    (source_id INT,
    target_id INT,
    edge_description VARCHAR(255),
    FOREIGN KEY(source_id) REFERENCES org_chart_branches(branch_id),
    FOREIGN KEY(target_id) REFERENCES org_chart_branches(branch_id))"""
)

cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)



	
