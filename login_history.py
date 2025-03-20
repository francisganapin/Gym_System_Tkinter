import tkinter as tk
from tkinter import ttk

import os
import sqlite3




def load_data(treeview):
    # Load the Excel workbook and select the active sheet
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to 'members.xlsx'
    file_path = os.path.join(current_directory, 'members.db')

    conn = sqlite3.connect(file_path )
    cursor = conn.cursor()

    cursor.execute('PRAGMA table_info(gym_login_record)')
    
    columns_info = cursor.fetchall()
    columns = [info[1]for info in columns_info]

    treeview['columns'] = columns
    for col_name in columns:
        treeview.heading(col_name,text=col_name)
        treeview.column(col_name,width=100)


    cursor.execute('SELECT * FROM gym_login_record')
    rows = cursor.fetchall()

    for row in rows:
        treeview.insert('','end',values=row)

    conn.close()


root = tk.Tk()
root.title("Basic Tkinter App")
root.tk.call('source','forest-dark.tcl')

style =ttk.Style(root)
style.theme_use('forest-dark')


frame = ttk.Frame(root)
frame.pack()



# Data of N of Member Input bar in first row
# Treeview Frame
widgets_frame4 = ttk.Frame(frame)
widgets_frame4.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

tree_scroll = ttk.Scrollbar(widgets_frame4)
tree_scroll.pack(side='right', fill='y')

cols = ()
treeview = ttk.Treeview(widgets_frame4, show='headings', yscrollcommand=tree_scroll.set, columns=cols, height=20)


treeview.pack()
tree_scroll.config(command=treeview.yview)
load_data(treeview)
root.mainloop()

