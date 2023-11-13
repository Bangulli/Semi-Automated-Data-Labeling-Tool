import torch

# This script is for the core functions, basically the backend
# put the methods for applying the neural net and saving and shit here
class bbox():
    def __init__(self, x, y, w, h, canvas, label, identifier, color, vis=False):
        # Set class variables, the coordinates and dimensions are set in canvas coordinates.
        # Might need to change some things as image coordinates are usually inverted
        self.x = float(x) # the location on x axis (left right)
        self.y = float(y) # the location on y axis (up down)
        self.w = float(w) # the width (in y dim)
        self.h = float(h) # the height (in x dim)
        self.canvas = canvas # the canvas the rectangle is drawn in
        self.label = label # the tag of the rectangle
        self.identifier = identifier
        self.visu = vis if vis else canvas.create_rectangle(self.x, self.y, self.x+self.w, self.y+self.h, tags='bbox', outline=color) # the rectangle element of the canvas

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

    def toString(self): # method to return the data that uniquely identifies a bbox as a string so it can be printed to a txt file
        # stand in for now, fit this to some adequate syntax later
        return str(self.label+', {}, {}, {}, {}'.format(self.x, self.y, self.w, self.h))

    def getStringFormat(self): # returns a string that represents the .toString format in human readable
        return 'label, x origin, y origin, width, height'

def lorem_ipsum():
    print('Lorem ipsum dolor sit amet, consectetur adipisici elit')



### create class for COCO detection from yolov5s model
class COCODetection:
    def __init__(self, type='s') -> None:
        self.type = type
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5'+type, pretrained=True)   # pretrained COCO detection model
        self.classes = self.model.names    # class names
    def detect(self, img):
        """_summary_

        Args:
            img (str, image): input image path or image

        Returns:
            bboxes: list of bounding boxes
        """
        result = self.model(img)
        return result.xyxy[0].tolist()

if __name__ == '__main__':
    coco = COCODetection()
    img = 'https://ultralytics.com/images/zidane.jpg'
    result = coco.detect(img)
    print(result)