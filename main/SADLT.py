import tkinter as tk

# The main script for the GUI and controls of the application
# This is where the Core methods are used
# (S)emi (A)utomated (D)ata (L)abeling (T)ool

class SADLT(tk.Tk):
    def __init__(self): # Constructor
        tk.Tk.__init__(self) # Call constructor inherited from tk
        # everything else we need to do for the app here
        self.create_widgets()
        self.pack_widgets()

    def create_widgets(self): # method for creating the widgets and packing them into the app
        self.lbl_msg = tk.Label(self, text='Template Application')
        self.btn_quit = tk.Button(self, text='Exit', command=self.quit)

    def pack_widgets(self):
        self.lbl_msg.pack()
        self.btn_quit.pack()

if __name__ == '__main__':
    app = SADLT()
    app.title('Template')
    app.mainloop()