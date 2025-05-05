import mysql.connector
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jai1234*",
        database="university_db"
    )

current_table = None

def fetch_table_data(table_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return columns, rows
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
        return [], []

def update_table_view(table_name):
    global current_table
    current_table = table_name
    columns, rows = fetch_table_data(table_name)

    for widget in table_frame.winfo_children():
        widget.destroy()

    if not columns:
        return

    tree = tb.Treeview(table_frame, columns=columns, show='headings', bootstyle="info", height=20)
    style = tb.Style()
    style.configure("Treeview", rowheight=35)  # More row height for spacing

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    for row in rows:
        tree.insert('', 'end', values=row)

    tree.pack(fill='both', expand=True)
    table_frame.tree = tree
    table_frame.columns = columns

def insert_record():
    if not current_table:
        return

    fields = table_frame.columns
    insert_window = tb.Toplevel(root)
    insert_window.title(f"Insert into {current_table}")
    insert_window.geometry("400x400")
    insert_window.resizable(False, False)

    entries = {}
    for i, field in enumerate(fields):
        tb.Label(insert_window, text=field).pack(pady=(10, 0))
        entry = tb.Entry(insert_window, bootstyle="info")
        entry.pack(pady=5, fill=X, padx=20)
        entries[field] = entry

    def submit_insert():
        values = [entries[f].get() for f in fields]
        if any(v == "" for v in values):
            messagebox.showwarning("Missing Input", "Please fill all fields.")
            return
        query = f"INSERT INTO {current_table} ({', '.join(fields)}) VALUES ({', '.join(['%s'] * len(values))})"
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record inserted.")
            insert_window.destroy()
            update_table_view(current_table)
        except mysql.connector.Error as e:
            messagebox.showerror("Insert Error", str(e))

    tb.Button(insert_window, text="Submit", bootstyle="success", command=submit_insert).pack(pady=20)

def delete_record():
    tree = getattr(table_frame, 'tree', None)
    if not tree or not current_table:
        return
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Select a row to delete.")
        return
    values = tree.item(selected[0])['values']
    pk_column = table_frame.columns[0]
    pk_value = values[0]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {current_table} WHERE {pk_column} = %s", (pk_value,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record deleted.")
        update_table_view(current_table)
    except mysql.connector.Error as e:
        messagebox.showerror("Delete Error", str(e))

def update_record():
    tree = getattr(table_frame, 'tree', None)
    if not tree or not current_table:
        return
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Select a row to update.")
        return

    old_values = tree.item(selected[0])['values']
    fields = table_frame.columns

    update_window = tb.Toplevel(root)
    update_window.title(f"Update {current_table}")
    update_window.geometry("400x400")
    update_window.resizable(False, False)

    entries = {}
    for i, field in enumerate(fields):
        tb.Label(update_window, text=field).pack(pady=(10, 0))
        entry = tb.Entry(update_window, bootstyle="info")
        entry.insert(0, old_values[i])
        entry.pack(pady=5, fill=X, padx=20)
        entries[field] = entry

    def submit_update():
        new_values = [entries[f].get() for f in fields]
        if any(v == "" for v in new_values):
            messagebox.showwarning("Missing Input", "Please fill all fields.")
            return
        pk_column = fields[0]
        pk_value = old_values[0]
        assignments = ', '.join([f"{col} = %s" for col in fields])
        query = f"UPDATE {current_table} SET {assignments} WHERE {pk_column} = %s"
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, (*new_values, pk_value))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record updated.")
            update_window.destroy()
            update_table_view(current_table)
        except mysql.connector.Error as e:
            messagebox.showerror("Update Error", str(e))

    tb.Button(update_window, text="Update", bootstyle="warning", command=submit_update).pack(pady=20)

def toggle_theme():
    current = app_style.theme.name
    new_theme = "darkly" if current != "darkly" else "minty"
    app_style.theme_use(new_theme)

# Root window
app_style = tb.Style(theme="minty")
root = app_style.master
root.title("University Database Admin Panel")
root.geometry("1100x650")
root.resizable(False, False)

# Layout
sidebar = tb.Frame(root, padding=10)
sidebar.pack(side=LEFT, fill=Y)

table_frame = tb.Frame(root, padding=10)
table_frame.pack(side=RIGHT, fill=BOTH, expand=True)

# Sidebar content
tb.Label(sidebar, text="Tables", font=("Helvetica", 14, "bold")).pack(pady=(10, 5))

tables = [
    "Administrator", "Student", "Course", "Enrollment",
    "Attendance", "Exam", "Faculty", "Department"
]

for t in tables:
    tb.Button(sidebar, text=t, bootstyle="secondary-outline", width=20, command=lambda table=t: update_table_view(table)).pack(pady=3)

tb.Label(sidebar, text="Actions", font=("Helvetica", 12, "bold")).pack(pady=(20, 5))

tb.Button(sidebar, text="Insert", bootstyle="success", width=20, command=insert_record).pack(pady=3)
tb.Button(sidebar, text="Update", bootstyle="warning", width=20, command=update_record).pack(pady=3)
tb.Button(sidebar, text="Delete", bootstyle="danger", width=20, command=delete_record).pack(pady=3)

# Theme toggle button
tb.Separator(sidebar, bootstyle="secondary").pack(pady=10, fill=X)
tb.Button(sidebar, text="Toggle Dark/Light", bootstyle="info-outline", width=20, command=toggle_theme).pack(pady=10)

root.mainloop()
