import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('members.db')

# Create a cursor object
cursor = conn.cursor()

# Create the member table
cursor.execute('''
CREATE TABLE IF NOT EXISTS member (
               
    Id INT AUTO_INCREMENT UNIQUE,
    Id_card VARCHAR(255) UNIQUE,
    Name TEXT NOT NULL,
    Email TEXT NOT NULL,
    Expiry TEXT,
    Contact TEXT,
    Status TEXT,
    Gender TEXT,
    Birthday TEXT,
    Address TEXT,
    PRIMARY KEY (Id)
);

''')

# Commit the changes and close the connection
conn.commit()
conn.close()
