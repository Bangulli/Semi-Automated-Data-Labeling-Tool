# This script is for the core functions, basically the backend
# put the methods for applying the neural net and saving and shit here
class bbox():
    def __init__(self, x, y, w, h, canvas, label):
        # Set class variables, the coordinates and dimensions are set in canvas coordinates.
        # Might need to change some things as image coordinates are usually inverted
        self.x = x # the location on x axis (left right)
        self.y = y # the location on y axis (up down)
        self.w = w # the width (in y dim)
        self.h = h # the height (in x dim)
        self.canvas = canvas # the canvas the rectangle is drawn in
        self.label = label # the tag of the rectangle
        self.visu = canvas.create_rectangle(x, y, x+w, y+h) # the rectangle element of the canvas

    def changeWidth(self, margin):# expand/contract horizontally
        self.w += margin
        self.canvas.coords(self.visu, self.x, self.y, self.x+self.w, self.y+self.h)

    def changeHeight(self, margin):# expand/contract vertically
        self.h += margin
        self.canvas.coords(self.visu, self.x, self.y, self.x + self.w, self.y + self.h)

    def translateHorizontally(self, margin):# move horizontally
        self.x += margin
        self.canvas.coords(self.visu, self.x, self.y, self.x + self.w, self.y + self.h)

    def translateVertically(self, margin):# move vertically
        self.y += margin
        self.canvas.coords(self.visu, self.x, self.y, self.x + self.w, self.y + self.h)

def lorem_ipsum():
    print('Lorem ipsum dolor sit amet, consectetur adipisici elit')
