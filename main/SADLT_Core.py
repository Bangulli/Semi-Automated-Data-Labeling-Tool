import torch

# This script is for the core functions, basically the backend
# put the methods for applying the neural net and saving and shit here
class bbox():
    def __init__(self, x, y, w, h, canvas, label, identifier, color, vis=False):
        """
        Initializes a bounding box object.

        Args:
            x (float): The x-coordinate of the bounding box.
            y (float): The y-coordinate of the bounding box.
            w (float): The width of the bounding box.
            h (float): The height of the bounding box.
            canvas: The canvas the rectangle is drawn in.
            label: The tag of the rectangle.
            identifier: The identifier of the bounding box.
            color: The color of the bounding box.
            vis (bool, optional): Whether the bounding box is visible. Defaults to False.
        """
        # Set class variables, the coordinates and dimensions are set in canvas coordinates.
        # Might need to change some things as image coordinates are usually inverted
        self.x = float(x) # the location on x axis (left right)
        self.y = float(y) # the location on y axis (up down)
        self.w = float(w) # the width (in y dim)
        self.h = float(h) # the height (in x dim)
        self.canvas = canvas # the canvas the rectangle is drawn in
        self.label = label # the tag of the rectangle
        self.identifier = identifier
        # create the textlabel in the canvas with background
        self.cnv_text = self.canvas.create_text(self.x+self.w/2, self.y+5, text=self.identifier)
        cnv_text_bg_x, cnv_text_bg_y, cnv_text_bg_x2, cnv_text_bg_y2 = self.canvas.bbox(self.cnv_text)
        self.cnv_text_w = cnv_text_bg_x2-cnv_text_bg_x
        self.cnv_text_h = cnv_text_bg_y2-cnv_text_bg_y
        self.canvas.coords(self.cnv_text, self.x + self.cnv_text_w / 2, self.y + self.cnv_text_h/2)
        self.cnv_text_bg = self.canvas.create_rectangle((self.x, self.y, self.x+self.cnv_text_w, self.y+self.cnv_text_h), fill=color, outline=color)
        self.canvas.tag_lower(self.cnv_text_bg, self.cnv_text)
        # create the bbox itself
        self.visu = vis if vis else canvas.create_rectangle(self.x, self.y, self.x+self.w, self.y+self.h, tags='bbox', outline=color) # the rectangle element of the canvas

    def changeWidth(self, margin):
        """
        Change the width of the object by the specified margin.

        Args:
            margin (int): The amount by which to expand or contract the width.

        Returns:
            None
        """
        # Update the width of the bounding box
        self.w += margin
        # Update the coordinates of the bounding box
        self.canvas.coords(self.visu, self.x, self.y, self.x+self.w, self.y+self.h)
        # Update the coordinates of the bounding box's text background
        self.canvas.coords(self.cnv_text_bg, self.x, self.y, self.x + self.cnv_text_w, self.y + self.cnv_text_h)
        # Update the coordinates of the bounding box's text
        self.canvas.coords(self.cnv_text, self.x + self.cnv_text_w / 2, self.y + self.cnv_text_h/2)

    def changeHeight(self, margin):
        """
        Change the height of the object by the specified margin.

        Args:
            margin (int): The amount by which to expand or contract the height.

        Returns:
            None
        """
        # Update the height of the bounding box
        self.h += margin
        # Update the coordinates of the bounding box
        self.canvas.coords(self.visu, self.x, self.y, self.x + self.w, self.y + self.h)
        # Update the coordinates of the bounding box's text background
        self.canvas.coords(self.cnv_text_bg, self.x, self.y, self.x + self.cnv_text_w, self.y + self.cnv_text_h)
        # Update the coordinates of the bounding box's text
        self.canvas.coords(self.cnv_text, self.x + self.cnv_text_w / 2, self.y + self.cnv_text_h/2)

    def translateHorizontally(self, margin):
        """
        Translates the object horizontally by the specified margin.

        Args:
            margin (int): The amount to move the object horizontally.

        Returns:
            None
        """
        # Update the x-coordinate of the bounding box
        self.x += margin
        # Update the coordinates of the bounding box
        self.canvas.coords(self.visu, self.x, self.y, self.x + self.w, self.y + self.h)
        # Update the coordinates of the bounding box's text background
        self.canvas.coords(self.cnv_text_bg, self.x, self.y, self.x + self.cnv_text_w, self.y + self.cnv_text_h)
        # Update the coordinates of the bounding box's text
        self.canvas.coords(self.cnv_text, self.x + self.cnv_text_w / 2, self.y + self.cnv_text_h/2)

    def translateVertically(self, margin):
        """
        Translates the bounding box vertically by the specified margin.

        Args:
            margin (int): The amount by which to translate the bounding box vertically.

        Returns:
            None
        """
        # Update the y-coordinate of the bounding box
        self.y += margin
        # Update the coordinates of the bounding box
        self.canvas.coords(self.visu, self.x, self.y, self.x + self.w, self.y + self.h)
        # Update the coordinates of the bounding box's text background
        self.canvas.coords(self.cnv_text_bg, self.x, self.y, self.x + self.cnv_text_w, self.y + self.cnv_text_h)
        # Update the coordinates of the bounding box's text
        self.canvas.coords(self.cnv_text, self.x + self.cnv_text_w / 2, self.y + self.cnv_text_h/2)

    def toString(self):
        """
        Returns a string representation of the bbox data.

        The returned string contains the label, x-coordinate, y-coordinate,
        width, and height of the bbox, formatted as "{label}, {x}, {y}, {w}, {h}".

        Returns:
            str: A string representation of the bbox data.
        """
        return str(self.label+', {}, {}, {}, {}'.format(self.x, self.y, self.w, self.h))

    def getStringFormat(self):
        """
        Returns a string that represents the .toString format in human readable.

        Returns:
            str: A string representing the format: 'label, x origin, y origin, width, height'
        """
        return 'label, x origin, y origin, width, height'

    def remove(self):
        """
        Removes the visual elements associated with the object from the canvas.
        """
        self.canvas.delete(self.visu)
        self.canvas.delete(self.cnv_text)
        self.canvas.delete(self.cnv_text_bg)



# Function to print a placeholder text
def lorem_ipsum():
    print('Lorem ipsum dolor sit amet, consectetur adipisici elit')



# Class for COCO detection using the yolov5s model
class COCODetection:
    def __init__(self, type='s') -> None:
        """
        Initialize the COCODetection class.

        Args:
            type (str): Type of the COCO detection model. Default is 's'.
        """
        self.type = type
        # Load the pretrained COCO detection model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5'+type, pretrained=True)
        # Get the class names from the model
        self.classes = self.model.names

    def detect(self, img):
        """
        Perform object detection on the input image.

        Args:
            img (str, image): Input image path or image.

        Returns:
            bboxes: List of bounding boxes.
        """
        result = self.model(img)
        return result.xyxy[0].tolist()

if __name__ == '__main__':
    coco = COCODetection()
    img = 'https://ultralytics.com/images/zidane.jpg'
    result = coco.detect(img)
    print(result)