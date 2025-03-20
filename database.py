
import sqlite3


conn = sqlite3.connect('members.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE gym_login_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_card VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    expiry    VARCHAR(255),
    login_time VARCHAR(255),
    login_date VARCHAR(255)
   
);
""")

cursor.execute("""
CREATE TABLE member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_card VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    expiry DATE NOT NULL,
    contact VARCHAR(255),
    status VARCHAR(50),
    gender VARCHAR(50),
    birthday DATE,
    address TEXT
);
""")

conn.commit()

# Close the connection
conn.close()

print("Database and table created, and records inserted.")
