import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3
from tkinter import messagebox










#when this click it would run the add membership####
def run_add_member_script():
    subprocess.run(['python','add.py'])

def run_edit_member_script():
    subprocess.run(['python','edit.py'])

def fetch_data_member(member_id):
    conn = sqlite3.connect('members.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Name, Expiry FROM member WHERE Id = ?', (member_id,))
    member = cursor.fetchone()
    conn.close()
    return member


def display_member_data():
    member_id = id_entry.get()
    if not member_id.isdigit():
        messagebox.showerror("Invalid Id try again")
        return
    member = fetch_data_member(int(member_id))
    if member:
        name_label.config(text=f"Name:{member[0]}")
        expiry_label.config(text=f"Expiry: {member[1]}")
        root.after(10000,clear_labels)
    else:
        messagebox.showinfo("Not Found")
    
def clear_labels():
    name_label.config(text='')
    expiry_label.config(text='')

############base################
root = tk.Tk()
root.title("Basic Tkinter App")
root.tk.call('source','forest-dark.tcl')
style =ttk.Style(root)
style.theme_use('forest-dark')
frame = ttk.Frame(root)
frame.pack()
############base################



############base################
root = tk.Tk()
root.title("Basic Tkinter App")
root.tk.call('source', 'forest-dark.tcl')
style = ttk.Style(root)
style.theme_use('forest-dark')
frame = ttk.Frame(root)
frame.pack(padx=20, pady=20, fill="both", expand=True)
############base################

# Widgets frame
widgets_frame = ttk.LabelFrame(frame, text="Function")
widgets_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

# Buttons for creating and editing members
button_create = ttk.Button(widgets_frame, text='Create Member', command=run_add_member_script)
button_create.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

button_edit = ttk.Button(widgets_frame, text='Edit Member', command=run_edit_member_script)
button_edit.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Labels and entry for member ID search
id_label = ttk.Label(frame, text="Enter Member ID:", font=('Helvetica', 14))
id_label.grid(row=1, column=0, padx=5, pady=5)

id_entry = ttk.Entry(frame, font=('Helvetica', 14))
id_entry.grid(row=2, column=0, padx=5, pady=5)

search_button = ttk.Button(frame, text="Search", command=display_member_data, style='Accent.TButton')
search_button.grid(row=3, column=0, padx=5, pady=5)

# Labels for displaying name and expiry
name_label = ttk.Label(frame, text="", font=('Helvetica', 16))
name_label.grid(row=4, column=0, padx=5, pady=5)

expiry_label = ttk.Label(frame, text="", font=('Helvetica', 16))
expiry_label.grid(row=5, column=0, padx=5, pady=5)

root.mainloop()