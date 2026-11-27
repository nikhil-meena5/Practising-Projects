import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("My Calculator")
root.geometry("450x440")
root.resizable(False, False)
root.configure(bg="#131314")

# Store the display text
display_text = tk.StringVar(value="")

# Create the display box
display = tk.Entry(
    root,
    textvariable=display_text,
    font=("Arial", 26),
    justify="right",
    state="readonly",
    readonlybackground="#303134",
    fg="white",
    bd=0
)
display.pack(fill="x", padx=15, pady=20, ipady=15)


# Add text to the display
def press(value):
    display_text.set(display_text.get() + value)


# Clear the display
def clear():
    display_text.set("")


# Delete the last character
def backspace():
    display_text.set(display_text.get()[:-1])


# Calculate the result
def calculate():
    expression = display_text.get()

    try:
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")

        result = eval(expression, {"__builtins__": {}}, {})
        display_text.set(str(result))

    except (ValueError, TypeError, SyntaxError,
            ZeroDivisionError, OverflowError):
        display_text.set("Error")
 

# Create the calculator buttons
buttons = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["C", "0", "00", "+"],
    ["⌫","AC",".", "="]
]

# Create the button area
button_frame = tk.Frame(root, bg="#202124")
button_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Create and place each button
for row_index, row in enumerate(buttons):
    for col_index, value in enumerate(row):

        if value == "C":
            command = clear
        elif value == "⌫":
            command = backspace
        elif value == "=":
            command = calculate
        elif value == "AC":    
            command = clear
        else:
            command = lambda v=value: press(v)

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 18),
            bg="#3c4043",
            fg="white",
            activebackground="#5f6368",
            activeforeground="white",
            bd=0,
            command=command
        )

        button.grid(
            row=row_index,
            column=col_index,
            sticky="nsew",
            padx=4,
            pady=4
        )

# Make buttons fill the available space
for i in range(5):
    button_frame.rowconfigure(i, weight=1)

for i in range(4):
    button_frame.columnconfigure(i, weight=1)

# Start the application
root.mainloop()


