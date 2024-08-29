import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import os
from tkinter import messagebox
from time import strftime
import sqlite3

def handle_edit_button_click(treeview, name_entry, expiry_entry):
    edit_item(treeview, name_entry, expiry_entry)


def load_data(treeview):
    # Load the SQLite database and fetch data
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'members.db')

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    # Fetch column information from the 'member' table
    cursor.execute('PRAGMA table_info(member)')
    columns_info = cursor.fetchall()

    # Extract column names
    columns = [info[1] for info in columns_info]
    print("Columns:", columns)  # Debug print statement

    # Set up Treeview columns
    treeview['columns'] = columns
    for col_name in columns:
        treeview.heading(col_name, text=col_name)
        treeview.column(col_name, width=100)

    # Fetch all rows from the 'member' table
    cursor.execute('SELECT * FROM member')
    rows = cursor.fetchall()
    print("Rows fetched:", rows)  # Debug print statement

    # Insert data into Treeview
    for row in rows:
        treeview.insert('', 'end', values=row)

    conn.close()

def edit_item(treeview, name_entry, expiry_entry):
    selected_item = treeview.focus()
    if selected_item:
        # Get the item ID from the Treeview (assuming the first column is ID)
        item_id = treeview.item(selected_item)['values'][0]

        # Get the new values from Entry widgets
        new_name = name_entry.get()
        new_expiry = expiry_entry.get()

        # Update the Treeview with the new values
        current_values = list(treeview.item(selected_item)['values'])
        current_values[1] = new_name
        current_values[3] = new_expiry  # Assuming column 3 is Expiry

        treeview.item(selected_item, values=current_values)

        # Update the database with the new values
        current_directory = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Update the Name and Expiry columns in the member table
            cursor.execute('''
                UPDATE member
                SET Name = ?, Expiry = ?
                WHERE Id = ?
            ''', (new_name, new_expiry, item_id))

            # Commit the changes to the database
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            # Close the database connection
            conn.close()

def search_data(treeview, search_type, search_entry):
    query = search_entry.get().strip().lower()

    # Clear the Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'members.db')

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    if search_type == 'ID':
        cursor.execute('SELECT * FROM member WHERE LOWER(CAST(id AS TEXT)) LIKE ?', ('%' + query + '%',))
    elif search_type == 'Name':
        cursor.execute('SELECT * FROM member WHERE LOWER(name) LIKE ?', ('%' + query + '%',))
    else:
        cursor.execute('SELECT * FROM member')

    rows = cursor.fetchall()
    for row in rows:
        treeview.insert("", "end", values=row)

    conn.close()

def my_time():
    time_string = strftime('%H:%M:%S %p \n %x')  # Format time string
    time.config(text=time_string)  # Update label with current time
    time.after(1000, my_time)

# Main application window
root = tk.Tk()
root.title("Basic Tkinter App")

# Applying a dark theme
root.tk.call('source', 'forest-dark.tcl')
style = ttk.Style(root)
style.theme_use('forest-dark')








# Creating main frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")


# Treeview Frame
time_frame = ttk.Frame(frame)
time_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Time display
my_font = ('times', 10, 'bold')
time = tk.Label(time_frame, font=my_font, bg='black')
time.grid(row=5, column=0, padx=5, pady=10)

# Update time display
my_time()

# Search Frame
search_frame = ttk.LabelFrame(frame, text="Search")
search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")


# Search Entries and Buttons (example)
search_id_entry = ttk.Entry(search_frame, width=20)
search_id_entry.insert(0, "Search by ID")
search_id_entry.bind("<FocusIn>", lambda e: search_id_entry.delete('0', 'end'))
search_id_entry.grid(row=0, column=0, padx=5, pady=5)

search_name_entry = ttk.Entry(search_frame, width=20)
search_name_entry.insert(0, "Search by Name")
search_name_entry.bind("<FocusIn>", lambda e: search_name_entry.delete('0', 'end'))
search_name_entry.grid(row=1, column=0, padx=5, pady=5)

search_id_button = ttk.Button(search_frame, text="Search ID", command=lambda: search_data(treeview, 'ID', search_id_entry))
search_id_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

search_name_button = ttk.Button(search_frame, text="Search Name", command=lambda: search_data(treeview, 'Name', search_name_entry))
search_name_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Name Entry
name_label = ttk.Label(search_frame, text="New Name:")
name_label.grid(row=2, column=1, padx=5, pady=5, sticky="e")
name_entry = ttk.Entry(search_frame, width=20)
name_entry.grid(row=2, column=0, padx=5, pady=5, sticky="w")

# Expiry Entry
expiry_label = ttk.Label(search_frame, text="New Expiry:")
expiry_label.grid(row=3, column=1, padx=5, pady=5, sticky="e")
expiry_entry = DateEntry(search_frame, width=12)  # Assuming you have a DateEntry widget for expiry
expiry_entry.grid(row=3, column=0, padx=5, pady=5, sticky="w")

# Edit Button
edit_button = ttk.Button(search_frame, text="Edit Item", command=lambda: edit_item(treeview, name_entry, expiry_entry))
edit_button.grid(row=4, column=0, columnspan=2, pady=10)








# Treeview Frame
treeview_frame = ttk.Frame(frame)
treeview_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Treeview and Scrollbar
treeview = ttk.Treeview(treeview_frame, columns=(), show='headings', height=15)
treeview.grid(row=0, column=0, sticky="nsew")

tree_scroll = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
tree_scroll.grid(row=0, column=1, sticky='ns')
treeview.configure(yscrollcommand=tree_scroll.set)

# Configure resizing
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
treeview_frame.grid_rowconfigure(0, weight=1)
treeview_frame.grid_columnconfigure(0, weight=1)

# Load data into the Treeview (replace with your data loading logic)
load_data(treeview)

root.mainloop()