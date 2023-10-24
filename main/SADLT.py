import tkinter as tk
import SADLT_Core as core
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import os
import cv2
import datetime

# The main script for the GUI and controls of the application
# This is where the Core methods are used
# (S)emi (A)utomated (D)ata (L)abeling (T)ool

class SADLT(tk.Tk):
    def __init__(self): # Constructor
        tk.Tk.__init__(self) # Call constructor inherited from tk to create window

        # Initialize the background file that logs errors and such. Dont know might be helpful. Also rewrite this comment pls
        self.logger = open(os.path.join(os.getcwd(), 'SADLT_Log_'+datetime.datetime.now().strftime('%d%m%y_%H-%M-%S')+'.txt'), 'w')
        # a flag to signify automatic log saving
        self.save_log = False

        # init internal variables
        self._internal_cwd_path = os.getcwd() # stores the current working directory from which images are loaded
        self._internal_working_image_cv2 = None
        self._internal_working_image_tk = None
        self._internal_detections = []

        # everything else we need to do for the app here
        self.create_widgets()

    def create_widgets(self): # method for creating the widgets and packing them into the app
        # out of frame stuff
        self.lbl_msg = tk.Label(self, text='You won a free trip to Rome')
        self.lbl_msg.pack()

        self.lbl_failState = tk.Label(self, text='Gucci', bg='green', width=10)
        self.lbl_failState.pack()

        # main frame setup
        self.frm_display = tk.Frame(self)
        self.frm_display.pack()

        # subframe for file loading and selection
        self.frm_file_loader = tk.Frame(self.frm_display)
        self.frm_file_loader.pack(side=tk.LEFT)
        # the button to trigger file dialogue
        self.btn_select_working_directory = tk.Button(self.frm_file_loader, text='Browse', command=self.browseFiles)
        self.btn_select_working_directory.pack()
        # list of png, jpg and jpeg files in the selected directory, select single images to load them into the canvas
        self.lbx_files = tk.Listbox(self.frm_file_loader, height=20, width=40, selectmode=tk.SINGLE)
        self.lbx_files.bind('<<ListboxSelect>>', self.loadImage)
        self.lbx_files.pack()
        # button to trigger the processing of a single image


        # the main canvas for display options
        self.cnv_main = tk.Canvas(self.frm_display, width=1026, height=1026, bg='white')
        self.cnv_main.pack(side=tk.LEFT)

        # sub frame for controls of labeling tools
        self.frm_labeling = tk.Frame(self.frm_display)
        self.frm_labeling.pack(side=tk.LEFT)
        # listbox that contains the found frames. select one for further processing like moving and shit
        self.lbx_detected = tk.Listbox(self.frm_labeling, height=20, width=40, selectmode=tk.SINGLE)
        self.lbx_detected.pack()

        self.btn_create = tk.Button(self.frm_labeling, text='Create', command=lambda: self.createBbox(1,1,10,10, 'peter'))
        self.btn_create.pack()

        self.btn_expand_width = tk.Button(self.frm_labeling, text='Expand Width', command=lambda: self.changeBboxWidth(1))
        self.btn_expand_width.pack()
        # need another thing to trigger the creation of a new frame

    def browseFiles(self): # method for file browsing. The path gets returned to a class attribute
        try:
            filename = filedialog.askdirectory(initialdir=self._internal_cwd_path,title="Select a File")
            # save the path to the internal variable
            self._internal_cwd_path = filename
            # delete all entries in the listbox
            self.lbx_files.delete('0', 'end')
            # put all the files within on the listbox
            [self.lbx_files.insert('end', elem) for elem in os.listdir(self._internal_cwd_path) if elem.endswith('.png') or elem.endswith('.jpg') or elem.endswith('.jpeg')]
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def loadImage(self, event): # method for image loading, sets the internal variables for tk and cv2 format images
        try:
            self._internal_working_image_cv2 = cv2.imread(os.path.join(self._internal_cwd_path, self.lbx_files.get(self.lbx_files.curselection()))) # load the image from disk using opencv
            self._internal_working_image_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self._internal_working_image_cv2, cv2.COLOR_BGR2RGB))) # write to a variable so the canvas has a constnat reference to display the image
            self.cnv_main.create_image(512, 512, image=self._internal_working_image_tk)#Convert the image to tk usable and display in canvas
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def createBbox(self, x, y, w, h, label): # method for creating new boundingboxes
        try:
            newBbox=core.bbox(x, y, w, h, self.cnv_main, label)
            self._internal_detections.append(newBbox) # append object to detection list
            self.lbx_detected.insert('end', newBbox.label)
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def changeBboxWidth(self, margin):
        try:
            [elem.changeWidth(margin) for elem in self._internal_detections if elem.label == self.lbx_detected.get(self.lbx_detected.curselection())]
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def handleError(self, error): # error handling, logs error and updates in app signifier, set log saver true
        self.logger.write(datetime.datetime.now().strftime('%H:%M:%S')+' - Caught an Exception of type '+ type(error).__name__ + ' with message: '+str(error)+'\n')
        self.lbl_failState.config(text='Failed', bg='red', width=10)
        self.save_log = True

# Mainloop. When the script is called this part of the script runs
if __name__ == '__main__':
    app = SADLT() # init class instance
    app.state('zoomed') # open in fullscreen mode
    app.title('SADLT - (S)emi (A)utomated (D)ata (L)abeling (T)ool') # set the name
    app.mainloop() # call mainloop

    # this happens after the window has been closed
    if app.save_log: # save log file automatically if something has happened
        app.logger.write(datetime.datetime.now().strftime('%H:%M:%S')+' - exited the application normally') # log exit
        app.logger.close()  # save logger
    else: # just delete the log file for now so we dont get too much garbage in the directories
        app.logger.close()
        os.remove(app.logger.name)