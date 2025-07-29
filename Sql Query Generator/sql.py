import sqlite3

import os

# Print the absolute path of the database file being used
db_path = os.path.abspath('student.db')
print(f"Using database file at: {db_path}")
connection=sqlite3.connect(db_path)

# cursor  - use to execute sql commands in python
cursor = connection.cursor()

# create a table

# Always start with a clean table
cursor.execute("DROP TABLE IF EXISTS Student")
table_info = """
CREATE TABLE Student (
    Name VARCHAR(25),
    Class VARCHAR(25),
    Section VARCHAR(25),
    Marks INT
);
"""
cursor.execute(table_info)

# Insert records with correct SQL syntax
cursor.execute("""INSERT INTO Student VALUES ('Ashutosh', 'Gen Ai', 'A', 72)""")
cursor.execute("""INSERT INTO Student VALUES ('Rohit', 'Gen Ai', 'A', 60)""")
cursor.execute("""INSERT INTO Student VALUES ('Shanti', 'DGen Ai', 'A', 37)""")
cursor.execute("""INSERT INTO Student VALUES ('Chanchal', 'Agentic Ai', 'B', 89)""")
cursor.execute("""INSERT INTO Student VALUES ('Pooja', 'WebDev', 'A', 70)""")
cursor.execute("""INSERT INTO Student VALUES ('Sheetal', 'PowerBi', 'B', 80)""")

# Display All the records

print("The inserted records are")
data=cursor.execute('''Select * from Student''')
for row in data:
    print(row)

# Commit your changes int the database
connection.commit()

# close the connection
connection.close()
