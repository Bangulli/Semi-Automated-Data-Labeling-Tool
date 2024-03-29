import tkinter as tk
import SADLT_Core as core
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
import numpy as np

import os
import cv2
import datetime
import random

from SADLT_Core import COCODetection

# The main script for the GUI and controls of the application
# This is where the Core methods are used
# (S)emi (A)utomated (D)ata (L)abeling (T)ool

class SADLT(tk.Tk):
    ### The main class for the application
    def __init__(self): # Constructor
        tk.Tk.__init__(self) # Call constructor inherited from tk to create window

        # Initialize the background file that logs errors.
        self.logger = open(os.path.join(os.getcwd(), 'SADLT_Log_'+datetime.datetime.now().strftime('%d%m%y_%H-%M-%S')+'.txt'), 'w')

        # init the AI model
        self.model = COCODetection()
        # list of colors for the bboxes
        self.colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(len(self.model.classes))]
        # the list of possible labels
        self._label_types = list(self.model.classes.values()) # stand in, later call this from the actual used net

        # init internal variables
        self._internal_cwd_path = os.getcwd() # stores the current working directory from which images are loaded
        self._internal_working_image_cv2 = None
        self._internal_working_image_tk = None
        self._internal_working_label = None
        self._internal_detections = []
        self.previous_selection = None
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

    def create_widgets(self):
        """
        Method for creating the widgets and packing them into the app.
        """
        self.lbl_failState = tk.Label(self, text='', width=10)
        self.lbl_failState.pack()

        # main frame setup
        self.frm_display = tk.Frame(self)
        self.frm_display.pack()

        # subframe for file loading and selection
        self.frm_file_loader = tk.Frame(self.frm_display)
        self.frm_file_loader.pack(side=tk.LEFT, anchor=tk.N)
        # list of png, jpg and jpeg files in the selected directory, select single images to load them into the canvas
        self.lbx_files = tk.Listbox(self.frm_file_loader, height=20, width=40, selectmode=tk.SINGLE, exportselection=False)
        self.lbx_files.bind('<<ListboxSelect>>', self.lbx_files_on_select)
        self.lbx_files.pack()
        # the button to trigger file dialogue
        self.btn_select_working_directory = tk.Button(self.frm_file_loader, text='Browse', command=self.browseFiles)
        self.btn_select_working_directory.pack()
        # button to trigger the processing of a single image

        # the main canvas for display options
        self.cnv_main = tk.Canvas(self.frm_display, width=1026, height=1026, bg='SystemButtonFace')
        self.cnv_main.bind('<Button-1>', self.getCoordsFromCanvas)
        self.cnv_main.bind("<ButtonPress-1>", self.on_button_press)
        self.cnv_main.bind("<B1-Motion>", self.on_move_press)
        self.cnv_main.bind("<ButtonRelease-1>", self.on_button_release)
        self.cnv_main.pack(side=tk.LEFT)

        # sub frame for controls of labeling tools
        self.frm_labeling = tk.Frame(self.frm_display)
        self.frm_labeling.pack(side=tk.LEFT, anchor=tk.N)
        # listbox that contains the found frames. select one for further processing. 
        self.lbx_detected = tk.Listbox(self.frm_labeling, height=20, width=40, selectmode=tk.SINGLE, exportselection=False)
        self.lbx_detected.pack()
        # frame for the creation controls
        self.frm_creation = tk.Frame(self.frm_labeling)
        self.frm_creation.pack()
        # button to use yolov5 model to detect objects in the image
        self.btn_yolo = tk.Button(self.frm_labeling, text='COCO Detection', command=self.coco_detection)
        self.btn_yolo.pack()
        # button to delete a label
        self.btn_delete = tk.Button(self.frm_labeling, text='Delete Selected', command=self.delete_selected_item)
        self.btn_delete.pack()
        # button to clear labels
        self.btn_clear = tk.Button(self.frm_labeling, text='Clear Labels', command=self.clear_labels)
        self.btn_clear.pack()
        # button to save all the data to a txt file
        self.btn_save_labels = tk.Button(self.frm_labeling, text='Save', command=self.saveLabels)
        self.btn_save_labels.pack()
        # frame to contain the control for moving the selected bbox
        self.frm_move = tk.Frame(self.frm_labeling)
        self.frm_move.pack()

        self.lbl_move = tk.Label(self.frm_move, text='Control Bounding Box position', width=30)
        self.lbl_move.grid(columnspan=3, column=0, row=0)
        # button to move right
        self.btn_move_right = tk.Button(self.frm_move, text='Right', width=6,
                                        command=lambda: self.translateBboxHorizontally(1))
        self.btn_move_right.grid(column=2, row=2)
        # button to move left
        self.btn_move_left = tk.Button(self.frm_move, text='Left', width=6,
                                       command=lambda: self.translateBboxHorizontally(-1))
        self.btn_move_left.grid(column=0, row=2)
        # button to move down
        self.btn_move_down = tk.Button(self.frm_move, text='Down', width=6,
                                       command=lambda: self.translateBboxVertically(1))
        self.btn_move_down.grid(column=1, row=3)
        # button to move up
        self.btn_move_up = tk.Button(self.frm_move, text='Up', width=6,
                                     command=lambda: self.translateBboxVertically(-1))
        self.btn_move_up.grid(column=1, row=1)
        # frame to contain the control for expanding/contracting the selected bbox
        self.frm_transform = tk.Frame(self.frm_labeling)
        self.frm_transform.pack()
        # label for information
        self.lbl_transform = tk.Label(self.frm_transform, text='Control Bounding Box Morphology', width=30)
        self.lbl_transform.grid(column=0, columnspan=3, row=0)
        # button to expand width
        self.btn_expand_width = tk.Button(self.frm_transform, text='Width+', width=6,
                                          command=lambda: self.changeBboxWidth(1))
        self.btn_expand_width.grid(column=2, row=2)
        # button to cotract width
        self.btn_contract_width = tk.Button(self.frm_transform, text='Width-', width=6,
                                            command=lambda: self.changeBboxWidth(-1))
        self.btn_contract_width.grid(column=0, row=2)
        # button to expand height
        self.btn_expand_height = tk.Button(self.frm_transform, text='Height+', width=6,
                                           command=lambda: self.changeBboxHeight(1))
        self.btn_expand_height.grid(column=1, row=3)
        # button to cotract height
        self.btn_contract_height = tk.Button(self.frm_transform, text='Height-', width=6,
                                             command=lambda: self.changeBboxHeight(-1))
        self.btn_contract_height.grid(column=1, row=1)
    
    def lbx_files_on_select(self, event):
        """Event handler for the file listbox

        Args:
            event (event): triggered event
        """
        # delete all entries in the detection listbox
        current_selection = self.lbx_files.curselection()
        if (current_selection != self.previous_selection or self.previous_selection == None) and len(current_selection):
            self.clear_labels() # clear all labels
            self.loadImage()
            self.loadLabels()
            self.lbl_failState.config(text='', width=10, background='SystemButtonFace')
        self.previous_selection = current_selection

    def delete_selected_item(self):
        """Delete the selected item from the listbox
        """
        selected = self.lbx_detected.curselection()
        if selected:
            # delete the bbox from the canvas and the listbox
            index = selected[0]
            self.lbx_detected.delete(selected)
            # remove the bbox fr1om the canvas
            self._internal_detections[index].remove()
            self._internal_detections.pop(index)
    
    def clear_labels(self):
        """Clear all current bboxes
        """
        # delete all bbox
        [elem.remove() for elem in self._internal_detections]
        # clear list box
        self.lbx_detected.delete('0', 'end')
        self._internal_detections = []
    
    def on_button_press(self, event):
        """
        Event handler for button press event.

        Args:
            event (Event): The button press event.

        Returns:
            None
        """
        self.current_class = None
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        # if not self.rect:
        self.current_rect = self.cnv_main.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', tags='bbox')

    def on_move_press(self, event):
        """
        Handles the event when the mouse is moved while being pressed.

        Args:
            event (tkinter.Event): The event object containing information about the mouse movement.

        Returns:
            None
        """
        curX, curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.cnv_main.coords(self.current_rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        """
        Handle the button release event.

        Args:
            event (tkinter.Event): The event object containing information about the button release.

        Returns:
            None
        """
        # save mouse drag end position
        curX, curY = (event.x, event.y)
        # create the drop down menu
        self.create_dropdown_popup(curX, curY)
    
    def drop_down_select_cb(self, event, popup_window, curX, curY):
        """Drop down menu to select class

        Args:
            event (event): triggered event
            popup_window (toplevel): popup window
            curX (x coord): mouse's x postition after release
            curY (y coord): mouse's y postition after release
        """
        # get the selected class name
        self.current_class = event.widget.get()
        # destroy the popup window
        popup_window.destroy()
        # change the color of the bbox to the color of the class
        self.cnv_main.itemconfig(self.current_rect, outline=self.colors[self._label_types.index(self.current_class)])
        # create the bbox
        self.createBbox(self.start_x, self.start_y, curX - self.start_x, curY - self.start_y, self.current_class, vis=self.current_rect)
    
    def drop_down_on_close(self, popup_window):
        """
        Drop down menu action on close.

        This method is called when the drop-down menu is closed. It destroys the popup window
        and deletes the current rectangle from the canvas.

        Parameters:
            popup_window (Tkinter.Toplevel): The popup window to be destroyed.

        Returns:
            None
        """
        # destroy the popup window
        popup_window.destroy()
        # delete the current rectangle
        self.cnv_main.delete(self.current_rect)
        
    def create_dropdown_popup(self, curX, curY):
        """
        Create a dropdown popup window with a combobox.

        Parameters:
        - curX (int): The x-coordinate of the current position.
        - curY (int): The y-coordinate of the current position.
        """
        # Create a new top-level window
        popup = tk.Toplevel()
        # Create a variable to hold the selected option
        selected_option = tk.StringVar()
        # Create the combobox
        combobox = ttk.Combobox(popup, textvariable=selected_option, height=10)
        # Add some options
        combobox['values'] = self._label_types
        # Set the default option
        combobox.current(0)
        combobox.bind("<<ComboboxSelected>>", lambda event: self.drop_down_select_cb(event, popup_window=popup, curX=curX, curY=curY))
        popup.protocol("WM_DELETE_WINDOW", lambda: self.drop_down_on_close(popup))
        # Pack the combobox
        combobox.pack()

    def browseFiles(self):
        """
        Method for file browsing. The path gets returned to a class attribute.
        """
        filename = filedialog.askdirectory(initialdir=self._internal_cwd_path, title="Select a File")
        # save the path to the internal variable
        self._internal_cwd_path = filename
        # delete all entries in the listbox
        self.lbx_files.delete('0', 'end')
        # put all the files within on the listbox
        [self.lbx_files.insert('end', elem) for elem in os.listdir(self._internal_cwd_path) if elem.endswith('.png') or elem.endswith('.jpg') or elem.endswith('.jpeg')]


    def loadImage(self): # method for image loading, sets the internal variables for tk and cv2 format images
        # try:
        self._internal_working_image_cv2 = cv2.imread(os.path.join(self._internal_cwd_path, self.lbx_files.get(self.lbx_files.curselection()))) # load the image from disk using opencv
        self._internal_working_image_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self._internal_working_image_cv2, cv2.COLOR_BGR2RGB))) # write to a variable so the canvas has a constnat reference to display the image
        height, width = self._internal_working_image_cv2.shape[:2]# gets the dimensions so we can determine the spawn point in canvas
        self.cnv_main.create_image(width/2, height/2, image=self._internal_working_image_tk)#Convert the image to tk usable and display in canvas. Spawned in top right corner, so canvas coords align with pixel coords of returned bboxes by model
        # except Exception as error: # catch and call error handling
        #     self.handleError(error)
        
    def loadLabels(self): 
            """Load the labels from a txt file.

            This method reads a txt file containing labels and creates bounding boxes based on the information in the file.
            Each line in the file represents a label with its corresponding coordinates and dimensions.

            Raises:
                Any exception that occurs during the file reading process will be raised.

            """
            # try:
            self._internal_working_label = os.path.splitext(os.path.join(self._internal_cwd_path, self.lbx_files.get(self.lbx_files.curselection())))[0] + '_Labels.txt' # load the label from disk using opencv
            if os.path.isfile(self._internal_working_label):
                lines = open(self._internal_working_label, 'r').readlines() # open the file
                for i, line in enumerate(lines): # iterate over the lines in the file
                    if i == 0:
                        continue  
                    label, x_origin, y_origin, width, height = line.split(',')
                    self.createBbox(x_origin, y_origin, width, height, label) # create a bbox for each line in the file          
            # except Exception as error: # catch and call error handling
            #     self.handleError(error)
        
    def createBbox(self, x, y, w, h, label, vis=False):
        """
        Method for creating new bounding boxes.

        Parameters:
        - x: The x-coordinate of the bounding box.
        - y: The y-coordinate of the bounding box.
        - w: The width of the bounding box.
        - h: The height of the bounding box.
        - label: The label of the bounding box.
        - vis: A boolean indicating whether the bounding box should be visible or not. Default is False.
        """
        identifier = label + str(len(self._internal_detections))
        newBbox = core.bbox(x, y, w, h, self.cnv_main, label, identifier, self.colors[self._label_types.index(label)], vis)
        self._internal_detections.append(newBbox)
        self.lbx_detected.insert('end', newBbox.identifier)


    def getCoordsFromCanvas(self, event):
        """
        Method to be called on click into the canvas.
        Pastes the coordinates of the click location into the frame creator.

        Args:
            event: The event object containing information about the click event.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        self._x_origin.set(event.x)
        self._y_origin.set(event.y)


    def changeBboxHeight(self, margin):
        """
        Changes the height of the selected bounding box by the specified margin.

        Args:
            margin (float): The margin by which to change the height of the bounding box.

        Returns:
            None
        """
        selected = self.lbx_detected.curselection()
        if selected:
            index = selected[0]
            self._internal_detections[index].changeHeight(margin)

    def changeBboxWidth(self, margin):
        """
        Change the width of the bounding box for the selected detection.

        Args:
            margin (int): The amount by which to change the width of the bounding box.

        Returns:
            None
        """
        selected = self.lbx_detected.curselection()
        if selected:
            index = selected[0]
            self._internal_detections[index].changeWidth(margin)

    def translateBboxHorizontally(self, margin):
        """
        Translates the bounding box horizontally by the specified margin.

        Args:
            margin (int): The amount by which to translate the bounding box horizontally.

        Returns:
            None
        """
        selected = self.lbx_detected.curselection()
        if selected:
            index = selected[0]
            self._internal_detections[index].translateHorizontally(margin)

    def translateBboxVertically(self, margin):
        """
        Translates the bounding box vertically by the specified margin.

        Args:
            margin (int): The amount by which to translate the bounding box vertically.

        Returns:
            None
        """
        selected = self.lbx_detected.curselection()
        if selected:
            index = selected[0]
            self._internal_detections[index].translateVertically(margin)

    def saveLabels(self):
        """
        Saves the labels to a file, with a name fitting the corresponding image.
        """
        # try:
        imname = self.lbx_files.get(self.lbx_files.curselection()).removesuffix('.png').removesuffix('.jpg').removesuffix('.jpeg') # get image name without file extension
        with open(os.path.join(self._internal_cwd_path, imname+'_Labels.txt'), 'w') as file: # create new txt file with a fitting name
            file.write(self._internal_detections[0].getStringFormat()+'\n') # write the format to the file
            [file.write(elem.toString()+'\n') for elem in self._internal_detections] # write the data of all bboxes to the file, fitting the previously stated format
            file.close() # close file
        self.lbl_failState.config(text='Success', bg='green', width=10)
        # except Exception as error:  # catch and call error handling
        #     self.handleError(error)

    def coco_detection(self):
        """Predict bboxes using the COCO detection model from loaded image and display them in the canvas
        """
        self.cnv_main.delete('bbox')
        result = self.model.detect(self._internal_working_image_cv2)
        [self.createBbox(elem[0], elem[1], elem[2]-elem[0], elem[3]-elem[1], self.model.classes[int(elem[5])]) for elem in result]


# Mainloop. When the script is called this part of the script runs
if __name__ == '__main__':
    app = SADLT() # init class instance
    app.state('zoomed') # open in fullscreen mode
    app.title('SADLT - (S)emi (A)utomated (D)ata (L)abeling (T)ool') # set the name
    app.mainloop() # call mainloop
