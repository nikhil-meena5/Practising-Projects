import json
from pathlib import Path
from datetime import date

FILE = Path(__file__).resolve().parent / "tasks.json"


def load_tasks():
    if not FILE.exists():
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError):
        print("Could not read tasks.json. Please check the file.")
        return []


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- YOUR TASKS ---")
    for number, task in enumerate(tasks, start=1):
        status = "DONE" if task.get("done", False) else "PENDING"
        task_date = task.get("date", "Date not available")
        print(f"{number}. [{status}] {task.get('task', '')} | {task_date}")


def add_task(tasks):
    task_name = input("Enter task: ").strip()

    if not task_name:
        print("Task cannot be empty.")
        return

    tasks.append({
        "task": task_name,
        "done": False,
        "date": date.today().isoformat()
    })
    save_tasks(tasks)
    print("Task added successfully!")


def get_task_number(tasks):
    if not tasks:
        print("No tasks available.")
        return None

    try:
        number = int(input("Enter task number: "))
        if 1 <= number <= len(tasks):
            return number - 1
        print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

    return None


def mark_done(tasks):
    view_tasks(tasks)
    index = get_task_number(tasks)

    if index is not None:
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("Task marked as done!")


def delete_task(tasks):
    view_tasks(tasks)
    index = get_task_number(tasks)

    if index is not None:
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Deleted task: {removed.get('task', '')}")


def show_statistics(tasks):
    total = len(tasks)
    done = sum(1 for task in tasks if task.get("done", False))
    pending = total - done

    print("\n--- TASK STATISTICS ---")
    print(f"Total tasks   : {total}")
    print(f"Completed     : {done}")
    print(f"Pending       : {pending}")


def main():
    tasks = load_tasks()

    while True:
        print("\n========== TO-DO LIST ==========")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Show statistics")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            show_statistics(tasks)
        elif choice == "6":
            print("Thank you for using To-Do List!")
            break
        else:
            print("Invalid choice. Please select 1 to 6.")


if __name__ == "__main__":
    main()