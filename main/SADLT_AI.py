import torch

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