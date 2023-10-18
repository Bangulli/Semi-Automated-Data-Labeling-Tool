import tkinter as tk
import SADLT_Core as core
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import os
import cv2

# The main script for the GUI and controls of the application
# This is where the Core methods are used
# (S)emi (A)utomated (D)ata (L)abeling (T)ool

class SADLT(tk.Tk):
    def __init__(self): # Constructor
        tk.Tk.__init__(self) # Call constructor inherited from tk to create window
        # set some inherited attributes

        # init internal variales
        self._internal_cwd_path = os.getcwd() # stores the current working directory from which images are loaded
        self._internal_working_image_cv2 = None
        self._internal_working_image_tk = None

        # everything else we need to do for the app here
        self.create_widgets()

    def create_widgets(self): # method for creating the widgets and packing them into the app
        # out of frame stuff
        self.lbl_msg = tk.Label(self, text='Template Application')
        self.lbl_msg.pack()

        self.btn_quit = tk.Button(self, text='Exit', command=self.quit)
        self.btn_quit.pack()

        # main frame setup
        self.frm_display = tk.Frame(self)
        self.frm_display.pack()

        # subframe for file loading and selection
        self.frm_file_loader = tk.Frame(self.frm_display)
        self.frm_file_loader.pack(side=tk.LEFT)

        self.lbx_files = tk.Listbox(self.frm_file_loader, height=20, width=40, selectmode=tk.SINGLE)
        self.lbx_files.bind('<<ListboxSelect>>', self.loadImage)
        self.lbx_files.pack()

        self.btn_select_working_directory = tk.Button(self.frm_file_loader, text='Browse', command=self.browseFiles)
        self.btn_select_working_directory.pack()

        # the main canvas for display options
        self.cnv_main = tk.Canvas(self.frm_display, width=1026, height=1026, bg='white')
        self.cnv_main.pack(side=tk.LEFT)

        # sub frame for controls of labeling tools
        self.frm_labeling = tk.Frame(self.frm_display)
        self.frm_labeling.pack(side=tk.LEFT)

        self.lbx_detected = tk.Listbox(self.frm_labeling, height=20, width=40, selectmode=tk.SINGLE)
        self.lbx_detected.pack()

    def browseFiles(self): # method for file browsing. The path gets returned to a class attribute
        filename = filedialog.askdirectory(initialdir=self._internal_cwd_path,title="Select a File")
        # save the path to the internal variable
        self._internal_cwd_path = filename
        # delete all entries in the listbox
        self.lbx_files.delete('0', 'end')
        # put all the files within on the listbox
        [self.lbx_files.insert('end', elem) for elem in os.listdir(self._internal_cwd_path) if elem.endswith('.png') or elem.endswith('.jpg') or elem.endswith('.jpeg')]

    def loadImage(self, event): # method for image loading, sets the internal variables for tk and cv2 format images
        self._internal_working_image_cv2 = cv2.imread(os.path.join(self._internal_cwd_path, self.lbx_files.get(self.lbx_files.curselection()))) # load the image from disk using opencv
        self._internal_working_image_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self._internal_working_image_cv2, cv2.COLOR_BGR2RGB))) # write to a variable so the canvas has a constnat reference to display the image
        self.cnv_main.create_image(512, 512, image=self._internal_working_image_tk)#Convert the image to tk usable and display in canvas

# Mainloop. When the script is called this part of the script runs
if __name__ == '__main__':
    app = SADLT()
    app.title('SADLT - (S)emi (A)utomated (D)ata (L)abeling (T)ool')
    app.mainloop()
