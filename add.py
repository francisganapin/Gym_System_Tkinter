import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import sqlite3
import openpyxl
from datetime import datetime

#function 
def select_and_copy_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image File",
                                           filetypes=(("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")))
    if file_path:
        try:
            # Load the selected image using PIL
            image = Image.open(file_path)

            # Save the image to the specified folder
            save_folder = "./images/"  # Specify your save folder path here
            os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist
            save_path = os.path.join(save_folder, os.path.basename(file_path))
            image.save(save_path)

            # Resize the image to a smaller size
            image.thumbnail((200, 200))  # Resize to 200x200 pixels

            # Display the resized image in tkinter
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(widgets_frame2, image=photo)
            label.image = photo  # Keep a reference to prevent garbage collection
            label.grid(row=2, column=0, padx=5, pady=5)

        except Exception as e:
            print(f"Error loading image: {e}")

def load_data(treeview):
    # Load the Excel workbook and select the active sheet
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to 'members.xlsx'
    file_path = os.path.join(current_directory, 'members.db')

    conn = sqlite3.connect(file_path )
    cursor = conn.cursor()

    cursor.execute('PRAGMA table_info(member)')
    
    columns_info = cursor.fetchall()
    columns = [info[1]for info in columns_info]

    treeview['columns'] = columns
    for col_name in columns:
        treeview.heading(col_name,text=col_name)
        treeview.column(col_name,width=100)


    cursor.execute('SELECT * FROM member')
    rows = cursor.fetchall()

    for row in rows:
        treeview.insert('','end',values=row)

    conn.close()

def insert_row():
    Id_card = id_entry.get()
    Name = name_entry.get()
    Email = email_entry.get()
    Expiry = date_entry.get()
    Contact = contact_entry.get()
    Status = member_status.get()
    Gender = male_or_female_status.get()
    Birthday = birthday_entry.get()
    Address = adress_input.get("1.0", "end-1c")

 

    # Load the SQLite database and select the active sheet
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to 'members.db'
    file_path = os.path.join(current_directory, 'members.db')

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO member (Id_card, Name, Email, Expiry, Contact, Status, Gender, Birthday, Address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (Id_card, Name, Email, Expiry, Contact, Status, Gender, Birthday, Address))
        
        conn.commit()
        print("Row inserted successfully")
    except sqlite3.IntegrityError as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

# Create the main window
member_or_not = ['Member','Not Member']
male_or_female =['Gender Any','Male','Female']


root = tk.Tk()
root.title("Basic Tkinter App")
root.tk.call('source','forest-dark.tcl')

style =ttk.Style(root)
style.theme_use('forest-dark')


frame = ttk.Frame(root)
frame.pack()

# Data of N of Member Input bar in first row
widgets_frame = ttk.LabelFrame(frame, text="Member")
widgets_frame.grid(row=0, column=0, padx=20, pady=10)


# Column 0 data
id_entry = ttk.Entry(widgets_frame)
id_entry.insert(0, "Id")
id_entry.bind("<FocusIn>", lambda e: id_entry.delete('0', 'end'))
id_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

name_entry = ttk.Entry(widgets_frame)
name_entry.insert(0, "Name")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
name_entry.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

email_entry = ttk.Entry(widgets_frame)
email_entry.insert(0, "Email")
email_entry.bind("<FocusIn>", lambda e: email_entry.delete('0', 'end'))
email_entry.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew")

separator_for_expiry = ttk.Label(widgets_frame,text='Expiry')
separator_for_expiry.grid(row=3,column=0,sticky='nsew',padx=6,pady=(7))

date_entry = DateEntry(widgets_frame)
date_entry.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew")





#### Column 1 data 
contact_entry = ttk.Entry(widgets_frame)
contact_entry.insert(0, "Contact")
contact_entry.bind("<FocusIn>", lambda e: contact_entry.delete('0', 'end'))
contact_entry.grid(row=0, column=1, padx=5, pady=(0, 5), sticky="ew")

member_status = ttk.Combobox(widgets_frame, value=member_or_not)
member_status.current(0)
member_status.grid(row=1, column=1, padx=5, pady=(0, 5), sticky="ew")

male_or_female_status = ttk.Combobox(widgets_frame, value=male_or_female)
male_or_female_status.current(0)
male_or_female_status.grid(row=2, column=1, padx=5, pady=(0, 5), sticky="ew")


separator_for_birthday = ttk.Label(widgets_frame,text='Birthday')
separator_for_birthday.grid(row=3,column=1,sticky='nsew',padx=6,pady=(7))

birthday_entry = DateEntry(widgets_frame)
birthday_entry.grid(row=4, column=1, padx=5, pady=(0, 5), sticky="ew")


# Data of N of Member Input bar in first row
widgets_frame2 = tk.LabelFrame(frame, text="Picture and Adress")
widgets_frame2.grid(row=1, column=0, padx=20, pady=10)


separator_for_address = tk.Label(widgets_frame2,text='Address')
separator_for_address.grid(row=0,column=0,sticky='nsew',padx=6,pady=(7))

adress_input = tk.Text(widgets_frame2,height=5, width=50)
adress_input.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

separator_for_picture = tk.Label(widgets_frame2,text='Picture')
separator_for_picture.grid(row=2,column=0,sticky='nsew',padx=6,pady=(7))

save_button = tk.Button(widgets_frame2,text='Save',command=insert_row)
save_button.grid(row=3,column=0,sticky='nsew',padx=6,pady=(7))


# Data of N of Member Input bar in first row
# Treeview Frame
widgets_frame4 = ttk.Frame(frame)
widgets_frame4.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

tree_scroll = ttk.Scrollbar(widgets_frame4)
tree_scroll.pack(side='right', fill='y')

cols = ('Id','Name','Email','Expiry','Contact','Status','Gender','Birthday','Address')
treeview = ttk.Treeview(widgets_frame4, show='headings', yscrollcommand=tree_scroll.set, columns=cols, height=20)

treeview.column('Id', width=100)
treeview.column('Name', width=100)
treeview.column('Email', width=100)
treeview.column('Expiry', width=100)
treeview.column('Contact', width=100)
treeview.column('Status', width=100)
treeview.column('Gender', width=50)
treeview.column('Birthday', width=100)
treeview.column('Address', width=1000)

treeview.pack()
tree_scroll.config(command=treeview.yview)
load_data(treeview)
root.mainloop()

