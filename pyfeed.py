import csv
import tkinter as tk
from tkinter import ttk
import webbrowser


# Function to read CSV data
def read_csv(file_name):
    data = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            data.append(row)
    return data


# Function to open a URL in the default browser
def open_link(event):
    selected_item = treeview.selection()[0]
    link = treeview.item(selected_item)['values'][3]  # The link is in the 4th column (index 3)
    webbrowser.open_new(link)


# Set up the GUI
def setup_gui(data):
    root = tk.Tk()
    root.title("RSS Feeds")

    # Define columns
    columns = ("Date", "Owner", "Title", "Link")

    # Create Treeview
    global treeview
    treeview = ttk.Treeview(root, columns=columns, show='headings', height=10)

    # Define headings
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=150)

    # Insert data into Treeview
    for row in data:
        treeview.insert("", "end", values=row)

    # Scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Pack Treeview
    treeview.pack(fill="both", expand=True)

    # Bind double-click to open link in browser
    treeview.bind("<Double-1>", open_link)

    root.mainloop()


# Main function
if __name__ == "__main__":
    # Load data from CSV
    csv_file = "Amit Sengupta_records.csv"  # Replace with your actual CSV file path
    rss_data = read_csv(csv_file)

    # Set up and run the GUI
    setup_gui(rss_data)
