# This script is for the core functions, basically the backend
# put the methods for applying the neural net and saving and shit here
class bbox():
    def __init__(self, x, y, w, h, canvas, label):
        # set class variables
        self.x = x # the location on x axis (left right)
        self.y = y # the location on y axis (up down)
        self.w = w # the width (in y dim)
        self.h = h # the height (in x dim)
        self.canvas = canvas
        self.label = label
        self.visu = canvas.create_rectangle(x, y, x+w, y+h)

    def changeWidth(self, margin):
        self.w += margin
        self.canvas.coords(self.visu, self.x, self.y, self.x+self.w, self.y+self.h)

def lorem_ipsum():
    print('Lorem ipsum dolor sit amet, consectetur adipisici elit')
