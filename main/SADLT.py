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
        # the list of possible labels
        self._label_types = ['Person', 'Dog', 'Horse', 'Car', 'Bus', 'Truck']
        # The variable to store the dpd selcetion
        self._dpd_label_type_selection = tk.StringVar()
        self._dpd_label_type_selection.set(self._label_types[0])
        # internal variables for frame creation
        self._x_origin = tk.IntVar()
        self._x_origin.set(0)
        self._y_origin = tk.IntVar()
        self._y_origin.set(0)

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
        self.frm_file_loader.pack(side=tk.LEFT, anchor=tk.N)
        # list of png, jpg and jpeg files in the selected directory, select single images to load them into the canvas
        self.lbx_files = tk.Listbox(self.frm_file_loader, height=20, width=40, selectmode=tk.SINGLE)
        self.lbx_files.bind('<<ListboxSelect>>', self.loadImage)
        self.lbx_files.pack()
        # the button to trigger file dialogue
        self.btn_select_working_directory = tk.Button(self.frm_file_loader, text='Browse', command=self.browseFiles)
        self.btn_select_working_directory.pack()
        # button to trigger the processing of a single image


        # the main canvas for display options
        self.cnv_main = tk.Canvas(self.frm_display, width=1026, height=1026, bg='white')
        self.cnv_main.bind('<Button-1>', self.getCoordsFromCanvas)
        self.cnv_main.pack(side=tk.LEFT)

        # sub frame for controls of labeling tools
        self.frm_labeling = tk.Frame(self.frm_display)
        self.frm_labeling.pack(side=tk.LEFT, anchor=tk.N)
        # listbox that contains the found frames. select one for further processing like moving and shit
        self.lbx_detected = tk.Listbox(self.frm_labeling, height=20, width=40, selectmode=tk.SINGLE)
        self.lbx_detected.pack()
        # frame for the creation controls
        self.frm_creation = tk.Frame(self.frm_labeling)
        self.frm_creation.pack()
        # button to create a new frame
        self.btn_create = tk.Button(self.frm_creation, text='Create', command=lambda: self.createBbox(self._x_origin.get(),self._y_origin.get(),10,10, self._dpd_label_type_selection.get()))
        self.btn_create.pack()
        # dropdown to select label type
        self.dpd_label_type = tk.OptionMenu(self.frm_creation, self._dpd_label_type_selection, *self._label_types)
        self.dpd_label_type.config(width=10)
        self.dpd_label_type.pack()
        # lbl x coord
        self.lbl_x_coord_input = tk.Label(self.frm_creation, text='X Origin')
        self.lbl_x_coord_input.pack()
        # entry for x coord
        self.ent_x = tk.Entry(self.frm_creation, textvariable=self._x_origin)
        self.ent_x.pack()
        # lbl Y coord
        self.lbl_y_coord_input = tk.Label(self.frm_creation, text='Y Origin')
        self.lbl_y_coord_input.pack()
        # entry for y coord
        self.ent_x = tk.Entry(self.frm_creation, textvariable=self._y_origin)
        self.ent_x.pack()
        # frame to contain the contorols for moving the selected bbox
        self.frm_move = tk.Frame(self.frm_labeling)
        self.frm_move.pack()
        # label fyi
        self.lbl_move = tk.Label(self.frm_move, text='Control Bounding Box position', width=30)
        self.lbl_move.grid(columnspan=3, column=0, row=0)
        # button to move right
        self.btn_move_right = tk.Button(self.frm_move, text='Right', width=6, command=lambda: self.translateBboxHorizontally(1))
        self.btn_move_right.grid(column=2, row=2)
        # button to move left
        self.btn_move_left = tk.Button(self.frm_move, text='Left', width=6, command=lambda: self.translateBboxHorizontally(-1))
        self.btn_move_left.grid(column=0, row=2)
        # button to move down
        self.btn_move_down = tk.Button(self.frm_move, text='Down', width=6, command=lambda: self.translateBboxVertically(1))
        self.btn_move_down.grid(column=1, row=3)
        # button to move up
        self.btn_move_up = tk.Button(self.frm_move, text='Up', width=6, command=lambda: self.translateBboxVertically(-1))
        self.btn_move_up.grid(column=1, row=1)
        # frame to contain the control for expanding/contracting the selected bbox
        self.frm_transform = tk.Frame(self.frm_labeling)
        self.frm_transform.pack()
        # label for information
        self.lbl_transform = tk.Label(self.frm_transform, text='Control Bounding Box Morphology', width = 30)
        self.lbl_transform.grid(column=0, columnspan=3, row=0)
        # button to expand width
        self.btn_expand_width = tk.Button(self.frm_transform, text='Width+', width=6, command=lambda: self.changeBboxWidth(1))
        self.btn_expand_width.grid(column=2, row=2)
        # button to cotract width
        self.btn_contract_width = tk.Button(self.frm_transform, text='Width-', width=6, command=lambda: self.changeBboxWidth(-1))
        self.btn_contract_width.grid(column=0, row=2)
        # button to expand height
        self.btn_expand_height = tk.Button(self.frm_transform, text='Height+', width=6, command=lambda: self.changeBboxHeight(1))
        self.btn_expand_height.grid(column=1, row=3)
        # button to cotract height
        self.btn_contract_height = tk.Button(self.frm_transform, text='Height-', width=6, command=lambda: self.changeBboxHeight(-1))
        self.btn_contract_height.grid(column=1, row=1)
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
            # delete all entries in the detection listbox
            self.lbx_detected.delete('0', 'end')
            # delete all entries in the bbox list
            self._internal_detections = []
            height, width = self._internal_working_image_cv2.shape[:2]# gets the dimensions so we can determine the spawn point in canvas
            self.cnv_main.create_image(width/2, height/2, image=self._internal_working_image_tk)#Convert the image to tk usable and display in canvas. Spawned in top right corner, so canvas coords align with pixel coords of returned bboxes by model
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def createBbox(self, x, y, w, h, label): # method for creating new boundingboxes
        try:
            label = label + str(len(self._internal_detections))
            newBbox=core.bbox(x, y, w, h, self.cnv_main, label)
            self._internal_detections.append(newBbox) # append object to detection list
            self.lbx_detected.insert('end', newBbox.label)
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def changeBboxWidth(self, margin): # proxy to call the width change method on an element of the bbox list
        try:
            [elem.changeWidth(margin) for elem in self._internal_detections if elem.label == self.lbx_detected.get(self.lbx_detected.curselection())]
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def changeBboxHeight(self, margin): # proxy to call the height change method on an element of the bbox list
        try:
            [elem.changeHeight(margin) for elem in self._internal_detections if elem.label == self.lbx_detected.get(self.lbx_detected.curselection())]
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def translateBboxHorizontally(self, margin):  # proxy to call the horizontal translate method on an element of the bbox list
        try:
            [elem.translateHorizontally(margin) for elem in self._internal_detections if elem.label == self.lbx_detected.get(self.lbx_detected.curselection())]
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def translateBboxVertically(self, margin): # proxy to call the vertical translate method on an element of the bbox list
        try:
            [elem.translateVertically(margin) for elem in self._internal_detections if elem.label == self.lbx_detected.get(self.lbx_detected.curselection())]
        except Exception as error: # catch and call error handling
            self.handleError(error)

    def getCoordsFromCanvas(self, event): # method to be called on click into the canvas, pastes the coorods of click location into frame creator
        try:
            self._x_origin.set(event.x)
            self._y_origin.set(event.y)
        except Exception as error:  # catch and call error handling
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