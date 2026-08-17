import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import os
import threading

current_file = None
process = None

def new_file():

    global current_file

    editor.delete("1.0", tk.END)

    current_file = None

    window.title("My Python IDE - Untitled")

def open_file():

    global current_file

    file_path = filedialog.askopenfilename(
        title="Open Python File",
        filetypes=[
            ("Python Files", "*.py"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            code = file.read()

        editor.delete(
            "1.0",
            tk.END
        )

        editor.insert(
            "1.0",
            code
        )

        current_file = file_path

        window.title(
            f"My Python IDE - {os.path.basename(file_path)}"
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )

def save_file():

    global current_file

    if current_file is None:

        save_as()

        return

    try:

        code = editor.get(
            "1.0",
            tk.END
        )

        with open(
            current_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(code)

        status_label.config(
            text="File saved successfully."
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )

def save_as():

    global current_file

    file_path = filedialog.asksaveasfilename(
        title="Save Python File",
        defaultextension=".py",
        filetypes=[
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:

        code = editor.get(
            "1.0",
            tk.END
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(code)

        current_file = file_path

        window.title(
            f"My Python IDE - {os.path.basename(file_path)}"
        )

        status_label.config(
            text="File saved successfully."
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )

def run_code():

    global current_file
    global process

    if current_file is None:

        save_as()

        if current_file is None:
            return

    else:
        save_file()

    output.delete(
        "1.0",
        tk.END
    )

    output.insert(
        tk.END,
        "Running program...\n\n"
    )

    run_button.config(
        state=tk.DISABLED
    )

    thread = threading.Thread(
        target=execute_program,
        daemon=True
    )

    thread.start()

def execute_program():

    global process

    try:

        process = subprocess.Popen(
            [
                sys.executable,
                current_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        window.after(
            0,
            show_output,
            stdout,
            stderr
        )

    except Exception as error:

        window.after(
            0,
            show_output,
            "",
            str(error)
        )

def show_output(
    stdout,
    stderr
):

    output.delete(
        "1.0",
        tk.END
    )

    if stdout:

        output.insert(
            tk.END,
            stdout
        )

    if stderr:

        output.insert(
            tk.END,
            "\nERROR:\n"
        )

        output.insert(
            tk.END,
            stderr
        )

    if not stdout and not stderr:

        output.insert(
            tk.END,
            "Program finished with no output."
        )

    status_label.config(
        text="Program finished."
    )

    run_button.config(
        state=tk.NORMAL
    )

def stop_program():

    global process

    if process is not None:

        try:

            process.terminate()

            output.insert(
                tk.END,
                "\n\nProgram stopped."
            )

        except Exception:
            pass

        process = None

def clear_output():

    output.delete(
        "1.0",
        tk.END
    )

window = tk.Tk()

window.title(
    "My Python IDE - Untitled"
)

window.geometry(
    "1100x700"
)

window.minsize(
    800,
    500
)

menu_bar = tk.Menu(window)

file_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

file_menu.add_command(
    label="New",
    command=new_file
)

file_menu.add_command(
    label="Open",
    command=open_file
)

file_menu.add_command(
    label="Save",
    command=save_file
)

file_menu.add_command(
    label="Save As",
    command=save_as
)

file_menu.add_separator()

file_menu.add_command(
    label="Exit",
    command=window.destroy
)

menu_bar.add_cascade(
    label="File",
    menu=file_menu
)

run_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

run_menu.add_command(
    label="Run",
    command=run_code
)

run_menu.add_command(
    label="Stop",
    command=stop_program
)

menu_bar.add_cascade(
    label="Run",
    menu=run_menu
)

window.config(
    menu=menu_bar
)

toolbar = tk.Frame(
    window,
    bd=1,
    relief=tk.RAISED
)

toolbar.pack(
    fill=tk.X
)

new_button = tk.Button(
    toolbar,
    text="New",
    command=new_file
)

new_button.pack(
    side=tk.LEFT,
    padx=3,
    pady=3
)

open_button = tk.Button(
    toolbar,
    text="Open",
    command=open_file
)

open_button.pack(
    side=tk.LEFT,
    padx=3,
    pady=3
)

save_button = tk.Button(
    toolbar,
    text="Save",
    command=save_file
)

save_button.pack(
    side=tk.LEFT,
    padx=3,
    pady=3
)

run_button = tk.Button(
    toolbar,
    text="▶ Run",
    command=run_code
)

run_button.pack(
    side=tk.LEFT,
    padx=3,
    pady=3
)

stop_button = tk.Button(
    toolbar,
    text="■ Stop",
    command=stop_program
)

stop_button.pack(
    side=tk.LEFT,
    padx=3,
    pady=3
)

clear_button = tk.Button(
    toolbar,
    text="Clear Output",
    command=clear_output
)

clear_button.pack(
    side=tk.LEFT,
    padx=3,
    pady=3
)

main_frame = tk.PanedWindow(
    window,
    orient=tk.VERTICAL,
    sashrelief=tk.RAISED
)

main_frame.pack(
    fill=tk.BOTH,
    expand=True
)

editor_frame = tk.Frame(
    main_frame
)

line_numbers = tk.Text(
    editor_frame,
    width=5,
    padx=5,
    font=("Consolas", 12),
    bg="#eeeeee",
    fg="#555555",
    state=tk.DISABLED
)

line_numbers.pack(
    side=tk.LEFT,
    fill=tk.Y
)

editor = tk.Text(
    editor_frame,
    font=("Consolas", 12),
    undo=True,
    wrap=tk.NONE
)

editor.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

editor_scrollbar = tk.Scrollbar(
    editor_frame,
    command=editor.yview
)

editor_scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

editor.config(
    yscrollcommand=editor_scrollbar.set
)

main_frame.add(
    editor_frame,
    minsize=300
)

output_frame = tk.Frame(
    main_frame
)

output_title = tk.Label(
    output_frame,
    text="Output",
    font=("Arial", 11, "bold"),
    anchor="w"
)

output_title.pack(
    fill=tk.X
)

output = tk.Text(
    output_frame,
    height=10,
    font=("Consolas", 11),
    bg="#1e1e1e",
    fg="#ffffff",
    wrap=tk.NONE
)

output.pack(
    fill=tk.BOTH,
    expand=True
)

main_frame.add(
    output_frame,
    minsize=150
)

status_label = tk.Label(
    window,
    text="Ready",
    anchor="w",
    relief=tk.SUNKEN
)

status_label.pack(
    fill=tk.X,
    side=tk.BOTTOM
)

window.bind(
    "<Control-n>",
    lambda event: new_file()
)

window.bind(
    "<Control-o>",
    lambda event: open_file()
)

window.bind(
    "<Control-s>",
    lambda event: save_file()
)

window.bind(
    "<F5>",
    lambda event: run_code()
)

editor.insert(
    "1.0",
    '''# Welcome to My Python IDE

print("Hello, Dil Jan!")

name = "Python"
print("I am learning", name)
'''
)

window.mainloop()