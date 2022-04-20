#Author: Ashlen Ashton
#Date: January 30, 2022
#File: bayerdb.py
#exe instructions: python3 bayerdb.py (Linux Ubuntu). Uncomment lines 69-77 if running first time
#comment 69-77 for subsequent runs. Run MySQL Sever prior to execution

#Lines 41-45 establish connection to server and create a cursor object to interact w/ MySQL
#Lines 63-67, 80-88, 90-97, 99-105, 107-113 create tables w/in bayerdatabase
#Lines 69-77 insert values into org_levels
#Lines 115-120 confirm all five tables were created
import mysql.connector
from mysql.connector import errorcode

# try:
#     bayerdb = mysql.connector.connect(
#     	host="localhost",
#     	user="root",
#     	password="root",
#         database="bayerdatabase"
#     )
#     print("Database already created");
#     cursor = bayerdb.cursor()
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does not yet exist, creating database with name: bayerdatabase.")
#         bayerdb = mysql.connector.connect(
#                 host="localhost",
#                 user="root",
#                 password="root",
#             )
#         cursor = bayerdb.cursor()
#         cursor.execute("CREATE DATABASE bayerdatabase")
#         bayerdb = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="root",
#             database="bayerdatabase"
#         )
#         print("Database successfully created.")

bayerdb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
    )
cursor = bayerdb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bayerdatabase")

bayerdb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='bayerdatabase'
)

cursor = bayerdb.cursor()
    





cursor.execute(
"""CREATE TABLE IF NOT EXISTS org_levels
    ( level VARCHAR(255) PRIMARY KEY, 
    description VARCHAR(255))"""
)

insert_level_into_org_levels = "INSERT INTO org_levels (level, description) VALUES (%s, %s)"
vals = [
   ("Division", "Highest level of Bayer's business model; contains teams within Crop Science, Pharmaceuticals, and Consumer Health industries"),
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

cursor.execute(
"""CREATE TABLE IF NOT EXISTS parent_branches
(current_branch_id INT,
parent_branch_id INT,
FOREIGN KEY(current_branch_id) REFERENCES org_chart_branches(branch_id),
FOREIGN KEY(parent_branch_id) REFERENCES org_chart_branches(branch_id))"""
)

cursor.execute(
"""CREATE TABLE IF NOT EXISTS child_branches
(current_branch_id INT,
child_branch_id INT,
FOREIGN KEY(current_branch_id) REFERENCES org_chart_branches(branch_id),
FOREIGN KEY(child_branch_id) REFERENCES org_chart_branches(branch_id))"""
)

cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)



	
