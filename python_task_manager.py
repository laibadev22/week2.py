import os

class TaskManager:
    """Professional Task Manager with file persistence."""

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from tasks.txt file if it exists."""
        if os.path.exists("tasks.txt"):
            try:
                with open("tasks.txt", "r", encoding="utf-8") as file:
                    for line in file:
                        if line.strip():
                            parts = line.strip().split("|")
                            if len(parts) == 4:
                                task_id, title, priority, completed = parts
                                self.tasks.append({
                                    "id": int(task_id),
                                    "title": title,
                                    "priority": priority,
                                    "completed": completed.lower() == "true"
                                })
            except Exception:
                print("Warning: Could not load previous tasks. Starting with empty list.")

    def save_tasks(self):
        """Save all tasks to tasks.txt file."""
        try:
            with open("tasks.txt", "w", encoding="utf-8") as file:
                for task in self.tasks:
                    file.write(f"{task['id']}|{task['title']}|{task['priority']}|{task['completed']}\n")
        except Exception:
            print("Warning: Could not save tasks to file.")

    def add_task(self):
        """Add a new task to the list."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()

        if not title:
            print("Error: Task title cannot be empty!")
            return

        priority = input("Enter priority (Low/Medium/High): ").strip().capitalize()
        if priority not in ["Low", "Medium", "High"]:
            print("Invalid priority! Default set to Low.")
            priority = "Low"

        # Generate unique ID
        task_id = max([t["id"] for t in self.tasks], default=0) + 1

        self.tasks.append({
            "id": task_id,
            "title": title,
            "priority": priority,
            "completed": False
        })

        self.save_tasks()
        print(f"Task added successfully! (ID: {task_id})")

    def view_tasks(self, tasks=None):
        """Display all tasks in a clean formatted table."""
        if tasks is None:
            tasks = self.tasks

        if not tasks:
            print("\nNo tasks found!")
            return

        print("\n" + "=" * 70)
        print("                          TASK LIST")
        print("=" * 70)
        print(f"{'ID':<5} {'Title':<35} {'Priority':<12} {'Status':<15}")
        print("-" * 70)

        for task in tasks:
            status = "Completed" if task["completed"] else "Pending"
            print(f"{task['id']:<5} {task['title']:<35} {task['priority']:<12} {status}")

        print("=" * 70)
        print(f"Total Tasks: {len(tasks)}")

    def update_task(self):
        """Update title or priority of an existing task."""
        if not self.tasks:
            print("\nNo tasks available to update!")
            return

        self.view_tasks()

        try:
            task_id = int(input("\nEnter Task ID to update: "))
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            return

        for task in self.tasks:
            if task["id"] == task_id:
                print("\nLeave blank to keep current value:")
                new_title = input(f"New Title (current: {task['title']}): ").strip()
                new_priority = input("New Priority (Low/Medium/High): ").strip().capitalize()

                if new_title:
                    task["title"] = new_title

                if new_priority:
                    if new_priority in ["Low", "Medium", "High"]:
                        task["priority"] = new_priority
                    else:
                        print("Invalid priority! No change made.")

                self.save_tasks()
                print("Task updated successfully!")
                return

        print("Task with this ID not found!")

    def complete_task(self):
        """Mark a task as completed."""
        if not self.tasks:
            print("\nNo tasks available!")
            return

        self.view_tasks()

        try:
            task_id = int(input("\nEnter Task ID to mark complete: "))
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            return

        for task in self.tasks:
            if task["id"] == task_id:
                if task["completed"]:
                    print("This task is already marked as completed!")
                else:
                    task["completed"] = True
                    self.save_tasks()
                    print("Task marked as complete successfully!")
                return

        print("Task not found!")

    def delete_task(self):
        """Delete a task after confirmation."""
        if not self.tasks:
            print("\nNo tasks available to delete!")
            return

        self.view_tasks()

        try:
            task_id = int(input("\nEnter Task ID to delete: "))
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            return

        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                confirm = input(f"Are you sure you want to delete '{task['title']}'? (y/n): ").lower().strip()
                if confirm == 'y':
                    self.tasks.pop(i)
                    self.save_tasks()
                    print("Task deleted successfully!")
                else:
                    print("Deletion cancelled.")
                return

        print("Task not found!")

    def filter_tasks(self):
        """Filter tasks by status or priority."""
        if not self.tasks:
            print("\nNo tasks to filter!")
            return

        print("\n" + "=" * 40)
        print("              FILTER TASKS")
        print("=" * 40)
        print("1. Filter by Status")
        print("2. Filter by Priority")
        print("3. Back to Main Menu")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            status_input = input("Enter status (complete/incomplete): ").lower().strip()
            if status_input not in ["complete", "incomplete"]:
                print("Invalid status!")
                return
            is_completed = status_input == "complete"
            filtered = [t for t in self.tasks if t["completed"] == is_completed]
            print(f"\nShowing {status_input} tasks:")
            self.view_tasks(filtered)

        elif choice == "2":
            priority = input("Enter priority (Low/Medium/High): ").strip().capitalize()
            if priority not in ["Low", "Medium", "High"]:
                print("Invalid priority!")
                return
            filtered = [t for t in self.tasks if t["priority"] == priority]
            print(f"\nShowing {priority} priority tasks:")
            self.view_tasks(filtered)

        elif choice == "3":
            return
        else:
            print("Invalid choice!")


# MAIN PROGRAM 
def main():
    print("Welcome to Task Manager")
    manager = TaskManager()

    while True:
        print("\n" + "=" * 55)
        print("                    MAIN MENU")
        print("=" * 55)
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Mark Task Complete")
        print("5. Delete Task")
        print("6. Filter Tasks")
        print("7. Exit Program")
        print("=" * 55)

        choice = input("\nEnter your choice : ").strip()

        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.view_tasks()
        elif choice == "3":
            manager.update_task()
        elif choice == "4":
            manager.complete_task()
        elif choice == "5":
            manager.delete_task()
        elif choice == "6":
            manager.filter_tasks()
        elif choice == "7":
            print("\nSaving tasks... Goodbye!")
            break
        else:
            print("Invalid choice! Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()