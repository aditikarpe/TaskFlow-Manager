import sqlite3
from flask import Flask
import threading

app = Flask(__name__)
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    priority TEXT DEFAULT 'Low',
    status TEXT DEFAULT 'Pending'
)
''')
conn.commit()

# Console functions
def add_task():
    content = input("Enter task description: ")
    priority = input("Enter priority (High/Medium/Low): ")
    cursor.execute("INSERT INTO tasks (content, priority) VALUES (?, ?)", (content, priority))
    conn.commit()
    print("Task added successfully.\n")

def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    print("\n--- Your Tasks ---")
    for row in rows:
        print(f"[{row[0]}] {row[1]} | Priority: {row[2]} | Status: {row[3]}")
    print()

def update_task():
    task_id = input("Enter task ID to update: ")
    new_status = input("Enter new status (Pending/Complete): ")
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    print("Task updated.\n")

def delete_task():
    task_id = input("Enter task ID to delete: ")
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print("Task deleted.\n")

def task_menu():
    while True:
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            update_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice.\n")

# Dummy Flask route
@app.route('/')
def hello():
    return "Task Manager is running in the background. Use console to manage tasks."

# Run Flask in background thread
def run_flask():
    app.run(debug=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    task_menu()
