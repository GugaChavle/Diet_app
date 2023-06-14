import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('diet.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()


create_table_query = '''
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    calorie INTEGER NOT NULL,
    date_of_reception TEXT NOT NULL
);
'''

# Execute the SQL statement to create the table
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
