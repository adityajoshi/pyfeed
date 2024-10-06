import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser

FEED_FOLDER = 'feeds'


# Function to find all CSV files in the current directory
def find_csv_files():
    # return [f for f in os.listdir() if f.endswith('.csv')]
    folder_path = os.path.join(os.getcwd(), FEED_FOLDER)
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", FEED_FOLDER + " folder not found!")
        return []

    return [f for f in os.listdir(folder_path) if f.endswith('.csv')]


# Function to read and display the selected CSV file
def display_csv(file_name):
    try:
        with open(os.path.join(FEED_FOLDER, file_name), newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if rows:
                display_table(rows)
            else:
                messagebox.showinfo("Info", f"{file_name} is empty!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to open a URL in the default browser
def open_link(event):
    selected_item = treeview.selection()[0]
    link = treeview.item(selected_item)['values'][3]  # The link is in the 4th column (index 3)
    webbrowser.open_new(link)


# Function to display the CSV content in a table (Treeview)
def display_table(data):
    for row in treeview.get_children():
        treeview.delete(row)

    # columns = data[0]  # First row is considered header
    columns = ["Read", "Date", "Owner", "Title", "Link"]

    treeview["columns"] = columns
    treeview["show"] = "headings"  # Show only headings

    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100)

    for row in data[1:]:
        read_status = row[0]
        if read_status == "True":
            treeview.insert("", "end", values=row, tags=('read',))
        else:
            treeview.insert("", "end", values=row)

    # Configure tag for the "read" rows
    treeview.tag_configure('read', background='light gray')
    # Scrollbar
    # scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
    # treeview.configure(yscroll=scrollbar.set)
    # scrollbar.pack(side='right', fill='y')

    # Pack Treeview
    # treeview.pack(fill="both", expand=True)

    # Bind double-click to open link in browser
    treeview.bind("<Double-1>", open_link)


# Function to handle the CSV selection from list
def on_select(event):
    selected_item = csv_listbox.curselection()
    if selected_item:
        file_name = csv_listbox.get(selected_item)
        display_csv(file_name)


def mark_as_read():
    selected_item = treeview.selection()
    if selected_item:
        # Get the selected row data
        item = treeview.item(selected_item)
        row_values = item['values']

        # Mark as "Read"
        row_values[0] = "True"  # Update the "Read" status to True

        # Update the CSV file
        file_name = csv_listbox.get(csv_listbox.curselection())  # Get the selected file name
        update_csv(file_name, row_values[3], "True")  # Update CSV based on the Title

        # Update the GUI
        treeview.item(selected_item, values=row_values)


def update_csv(file_name, title, status):
    file_path = os.path.join(FEED_FOLDER, file_name)
    rows = []

    # Read the CSV and update the status of the matching title
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        for row in rows:  # Skip header
            if row[3] == title:  # Match based on title
                row[0] = status  # Update the "Read" status

    # Write the updated rows back to the CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


# Setting up the GUI
def setup_gui():
    root = tk.Tk()
    root.title("PyFeed")

    # Frame for the CSV file list
    left_frame = tk.Frame(root)
    left_frame.pack(side='left', fill='y', padx=10, pady=10)

    # Label for Listbox
    tk.Label(left_frame, text="CSV Files in Folder:").pack()

    # Listbox for displaying CSV files
    global csv_listbox
    csv_listbox = tk.Listbox(left_frame, height=15, width=30)
    csv_listbox.pack(fill='y')

    # Add CSV files to the listbox
    csv_files = find_csv_files()
    if not csv_files:
        csv_listbox.insert(tk.END, "No CSV files found!")
    else:
        for file in csv_files:
            csv_listbox.insert(tk.END, file)

    # Bind the selection event to display CSV contents
    csv_listbox.bind('<<ListboxSelect>>', on_select)

    # Frame for the CSV content table
    right_frame = tk.Frame(root)
    right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    # Treeview widget for displaying CSV data
    global treeview
    treeview = ttk.Treeview(right_frame)
    treeview.pack(fill='both', expand=True)

    mark_read_button = tk.Button(right_frame, text="Mark as Read", command=mark_as_read)
    mark_read_button.pack(pady=5)

    # Start the GUI loop
    root.mainloop()


# Main function
if __name__ == "__main__":
    setup_gui()
