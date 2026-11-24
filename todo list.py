import json

FILE = "tasks.json"


#load task from file 
def load_tasks():
    try:
        with open (FILE,"r") as file:
            return json.load(file)

    except FileNotFoundError:
        return[]

#save task from file
def save_tasks(tasks):
    with open (FILE,"w") as file:
         json.dump(tasks,file)


# Add a task
def add_task(tasks):
    task = input("Enter task: ")

    tasks.append({
        "task": task,
        "done": False
    })

    save_tasks(tasks)
    print("Task added successfully!")

#view tasks
def view_tasks(tasks):
    if len(tasks) ==0:
        print("no tasks available")
        return

    for i, task in enumerate(tasks,start=1):
        if task ["done"]:
            status = "Done"
        else:
            status = "pending"
        print(i,task["task"],"-",status)

#mark task as done
def mark_done(tasks):
    view_tasks(tasks)


    
    if len(tasks) == 0:
        return

    try:

        number = int(input("Enter task number: "))

        if number < 1 or number > len(tasks):
            print("Task number does not exist!")
        else:
            tasks[number - 1]["done"] = True
            save_tasks(tasks)
            print("Task marked as done!")

    except ValueError:
        print("Please enter a valid number!")

# Delete a task
def delete_task(tasks):
    view_tasks(tasks)

    if len(tasks) == 0:
        return

    try:
        number = int(input("Enter task number to delete: "))

        if number < 1 or number > len(tasks):
            print("Task number does not exist!")
        else:
            removed = tasks.pop(number - 1)
            save_tasks(tasks)
            print("Deleted:", removed["task"])

    except ValueError:
        print("Please enter a valid number!")


# Main program
tasks = load_tasks()

while True:
    print("\n===== TO-DO LIST =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_task(tasks)

    elif choice == "2":
        view_tasks(tasks)

    elif choice == "3":
        mark_done(tasks)

    elif choice == "4":
        delete_task(tasks)

    elif choice == "5":       
        save_tasks(tasks)
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")

