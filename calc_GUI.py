import tkinter as tk
import math  # for square root

button_values = [
    ["AC", "+/-", "%", "÷"], 
    ["7", "8", "9", "*"], 
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

right_symbols=["÷","*","-","+","="]  # include divide symbol and remove duplicate '+'
top_symbols=["AC","+/-","%"]

row_count = len(button_values)
column_count=len(button_values[0])

color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

window = tk.Tk()
window.title("Simple Calculator")
window.resizable(False, False)

frame = tk.Frame(window)
label = tk.Label(frame, text="0", font=("Arial", 40), bg=color_black, fg=color_white, padx=10, pady=10, anchor="e")
label.grid(row=0, column=0,columnspan=column_count, sticky="we")

for row in range(row_count):
    for column in range(column_count):
        value=button_values[row][column]
        button=tk.Button(frame, text=value, font=("Arial", 30), width=column_count-1, height=1, command=lambda value=value: button_clicked(value))

        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white,background=color_dark_gray)

        button.grid(row=row+1,column=column)

frame.pack()

A="0"
operator=None
B=None

def clear_all():
    # reset state only, keep display as-is unless AC explicitly sets it
    global A,B,operator
    A="0"
    operator=None
    B=None

def remove_zero_decimal(num):
    if num % 1 == 0:
        num = int(num)
    return str(num)

def button_clicked(value):
    global right_symbols, top_symbols, A, B, operator

    if value in right_symbols:
        if value=="=":
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)

                if operator == "+":
                    label["text"] = remove_zero_decimal(numA + numB)
                elif operator == "-":
                    label["text"] = remove_zero_decimal(numA - numB)
                elif operator == "*":
                    label["text"] = remove_zero_decimal(numA * numB)
                elif operator in ("/", "÷"):
                    # basic divide-by-zero guard
                    label["text"] = "Error" if numB == 0 else remove_zero_decimal(numA / numB)

                clear_all()

        elif value in "+-*/÷":
            if operator is None:
                A = label["text"]
                label["text"] = "0"
                B = "0"
            # normalize '÷' to '/'
            operator = "/" if value == "÷" else value

    elif value in top_symbols:
        if value == "AC":
            clear_all()
            label["text"] = "0"

        elif value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_zero_decimal(result)

        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)

    else:
        if value == "√":
            try:
                x = float(label["text"])
                label["text"] = "Error" if x < 0 else remove_zero_decimal(math.sqrt(x))
            except ValueError:
                label["text"] = "Error"
        elif value == ".":
            if value not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value
            else:
                label["text"] += value

window.update()
window_width = window.winfo_width()
window_height= window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

window_x=int((screen_width/2)-(window_width/2))
window_y=int((screen_height/2)-(window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()

