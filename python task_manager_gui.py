import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

TASK_FILE = "tasks.json"
USER_FILE = "users.json"

# ---------------- USER SYSTEM ----------------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------------- LOGIN / REGISTER ----------------
class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login / Register")
        self.root.geometry("300x250")

        self.users = load_users()

        tk.Label(root, text="Username").pack(pady=5)
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=5)
        tk.Button(root, text="Register", command=self.register).pack()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user in self.users and self.users[user] == pwd:
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            main_app(user)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        user = self.username.get()
        pwd = self.password.get()

        if not user or not pwd:
            messagebox.showerror("Error", "Fill all fields")
            return

        if user in self.users:
            messagebox.showerror("Error", "User already exists")
            return

        self.users[user] = pwd
        save_users(self.users)
        messagebox.showinfo("Success", "Registered successfully!")

# ---------------- TASK MANAGER ----------------
class TaskManagerGUI:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"Task Manager - {user}")
        self.root.geometry("800x500")

        self.tasks = []
        self.dark_mode = False

        self.load_tasks()
        self.create_ui()
        self.refresh_table()

    def create_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Task Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(frame, width=30)
        self.title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Priority:").grid(row=0, column=2)
        self.priority_box = ttk.Combobox(frame, values=["Low", "Medium", "High"], state="readonly")
        self.priority_box.grid(row=0, column=3)
        self.priority_box.set("Low")

        tk.Button(frame, text="Add Task", command=self.add_task).grid(row=0, column=4)

        tk.Label(frame, text="Search:").grid(row=1, column=0)
        self.search_entry = tk.Entry(frame, width=30)
        self.search_entry.grid(row=1, column=1)
        tk.Button(frame, text="Search", command=self.search_task).grid(row=1, column=2)

        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Priority", "Status"), show="headings")
        self.tree.pack(fill="both", expand=True)

        for col in ("ID", "Title", "Priority", "Status"):
            self.tree.heading(col, text=col)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Complete", command=self.complete_task).grid(row=0, column=0)
        tk.Button(btn_frame, text="Delete", command=self.delete_task).grid(row=0, column=1)
        tk.Button(btn_frame, text="Update Priority", command=self.update_priority).grid(row=0, column=2)

        tk.Button(self.root, text="Dark Mode", command=self.toggle_theme).pack(pady=5)

    def add_task(self):
        title = self.title_entry.get().strip()
        priority = self.priority_box.get()

        if not title:
            messagebox.showerror("Error", "Enter title")
            return

        task_id = max([t["id"] for t in self.tasks], default=0) + 1

        self.tasks.append({"id": task_id, "title": title, "priority": priority, "completed": False})

        self.save_tasks()
        self.refresh_table()
        self.title_entry.delete(0, tk.END)

    def refresh_table(self, tasks=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if tasks is None:
            tasks = self.tasks

        for t in tasks:
            status = "Done" if t["completed"] else "Pending"
            self.tree.insert("", "end", values=(t["id"], t["title"], t["priority"], status))

    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            return None
        val = self.tree.item(selected[0])["values"][0]
        return next((t for t in self.tasks if t["id"] == val), None)

    def complete_task(self):
        task = self.get_selected()
        if task:
            task["completed"] = True
            self.save_tasks()
            self.refresh_table()

    def delete_task(self):
        task = self.get_selected()
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            self.refresh_table()

    def update_priority(self):
        task = self.get_selected()
        if task:
            task["priority"] = self.priority_box.get()
            self.save_tasks()
            self.refresh_table()

    def search_task(self):
        key = self.search_entry.get().lower()
        filtered = [t for t in self.tasks if key in t["title"].lower()]
        self.refresh_table(filtered)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.configure(bg="#2c2c2c" if self.dark_mode else "white")

    def save_tasks(self):
        with open(f"{self.user}_{TASK_FILE}", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        file = f"{self.user}_{TASK_FILE}"
        if os.path.exists(file):
            with open(file, "r") as f:
                self.tasks = json.load(f)

# ---------------- MAIN ----------------
def main_app(user):
    root = tk.Tk()
    TaskManagerGUI(root, user)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    AuthWindow(root)
    root.mainloop()
