import tkinter as tk
from tkinter import ttk

def create_dropdown_popup():
    # Create a new top-level window
    popup = tk.Toplevel()

    # Create a variable to hold the selected option
    selected_option = tk.StringVar()

    # Create the combobox
    combobox = ttk.Combobox(popup, textvariable=selected_option)

    # Add some options
    combobox['values'] = ('Option 1', 'Option 2', 'Option 3')

    # Set the default option
    combobox.current(0)

    # Pack the combobox
    combobox.pack()

root = tk.Tk()
create_dropdown_popup()
root.mainloop()
