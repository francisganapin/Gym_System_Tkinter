import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3
from tkinter import messagebox






from datetime import datetime

# Get the current date and time
current_datetime = datetime.now()

# Extract the date and convert it to a string
current_date = current_datetime.date().strftime('%Y-%m-%d')

# Extract the time and convert it to a string
current_time = current_datetime.time().strftime('%H:%M:%S')




#when this click it would run the add membership####
def run_add_member_script():
    subprocess.run(['python','add.py'])

def run_edit_member_script():
    subprocess.run(['python','edit.py'])


def run_login_history_script():
    subprocess.run(['python','login_history.py'])
    
def fetch_data_member(member_id):
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT first_name,last_name,expiry,id_card FROM member WHERE Id_card = ?', (member_id,))
        member = cursor.fetchone()
        print(member)

        if member:
            name_label.config(text=f"Name: {member[0]} {member[1]}")
            expiry_label.config(text=f"Expiry: {member[2]}")
            root.after(10000, clear_labels)

            # Call `save_login_history` to save login attempt
            save_login_history(member[0],member[1],member[2],member[3])  # Pass the member's name
        else:
            messagebox.showinfo("Not Found", "Member not found.")
    finally:
        conn.close()

def save_login_history(first_name,last_name,member_expiry,member_card):
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO gym_login_record (first_name,last_name,expiry,id_card,login_time,login_date) VALUES (?,?,?,?,?,?)',
                       (first_name,last_name,member_expiry,member_card,current_time,current_date))
        conn.commit()
    
    finally:
        conn.close()

def get_data_member():
    member_id = id_entry.get()
    fetch_data_member(member_id)


    
def clear_labels():
    name_label.config(text='')
    expiry_label.config(text='')



############base################
root = tk.Tk()
root.title("Basic Tkinter App")
root.tk.call('source', 'forest-dark.tcl')
style = ttk.Style(root)
style.theme_use('forest-dark')
frame = ttk.Frame(root)
frame.pack(padx=20, pady=20, fill="both", expand=False)

# Adjust size
root.geometry("400x400")
 
# set minimum window size value
root.minsize(300,400)
 
# set maximum window size value
root.maxsize(300, 400)



############base################

# Widgets frame
widgets_frame = ttk.LabelFrame(frame, text="Function")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

# Buttons for creating and editing members
button_create = ttk.Button(widgets_frame, text='Create Member', command=run_add_member_script)
button_create.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

button_edit = ttk.Button(widgets_frame, text='Edit Member', command=run_edit_member_script)
button_edit.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


button_edit = ttk.Button(widgets_frame, text='View Login', command=run_login_history_script)
button_edit.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

# Labels and entry for member ID search
id_label = ttk.Label(frame, text="Enter Member ID:", font=('Helvetica', 14))
id_label.grid(row=1, column=0, padx=5, pady=5)

id_entry = ttk.Entry(frame, font=('Helvetica', 14))
id_entry.grid(row=2, column=0, padx=5, pady=5)

search_button = ttk.Button(frame, text="Search", command=get_data_member, style='Accent.TButton')
search_button.grid(row=3, column=0, padx=5, pady=5)

# Labels for displaying name and expiry
name_label = ttk.Label(frame, text="", font=('Helvetica', 16))
name_label.grid(row=4, column=0, padx=5, pady=5)

expiry_label = ttk.Label(frame, text="", font=('Helvetica', 16))
expiry_label.grid(row=5, column=0, padx=5, pady=5)

root.mainloop()