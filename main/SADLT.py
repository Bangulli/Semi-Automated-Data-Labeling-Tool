import tkinter as tk
import SADLT_Core as core
from tkinter import filedialog
import os

# The main script for the GUI and controls of the application
# This is where the Core methods are used
# (S)emi (A)utomated (D)ata (L)abeling (T)ool

class SADLT(tk.Tk):
    def __init__(self): # Constructor
        tk.Tk.__init__(self) # Call constructor inherited from tk to create window
        # set some inherited attributes
        self.geometry('500x500')
        # init internal variales
        self._internal_cwd_path = os.getcwd() # stores the current working directory from which images are loaded
        # everything else we need to do for the app here
        self.create_widgets()
        self.pack_widgets()

    def create_widgets(self): # method for creating the widgets and packing them into the app
        self.lbl_msg = tk.Label(self, text='Template Application')
        self.btn_quit = tk.Button(self, text='Exit', command=self.quit)
        self.btn_select_working_directory = tk.Button(self, text='Browse', command=self.browseFiles)

    def pack_widgets(self): # method for packing the widgets to the window
        self.lbl_msg.pack()
        self.btn_quit.pack()
        self.btn_select_working_directory.pack()

    def browseFiles(self): # method for file browsing. The path gets returned to a class attribute
        filename = filedialog.askdirectory(initialdir=self._internal_cwd_path,title="Select a File")
        # save the path to the internal variable
        self._internal_cwd_path = filename

        print(filename) # for now debug printout. maybe flag this with a verbose condition

# Mainloop. When the script is called this part of the script runs
if __name__ == '__main__':
    app = SADLT()
    app.title('SADLT - (S)emi (A)utomated (D)ata (L)abeling (T)ool')
    app.mainloop()
