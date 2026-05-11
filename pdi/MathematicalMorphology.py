import cv2

class MathematicalMorphology:

    def dilate(self, image, ee, iterations):
        return cv2.morphologyEx(image,cv2.MORPH_DILATE,ee,iterations=iterations)

    def erode(self, image, ee, iterations):
        return cv2.morphologyEx(image,cv2.MORPH_ERODE,ee,iterations=iterations)

    def open(self, image, ee, iterations):
        return cv2.morphologyEx(image,cv2.MORPH_OPEN,ee,iterations=iterations)

    def close(self, image, ee, iterations):
        return cv2.morphologyEx(image,cv2.MORPH_CLOSE,ee,iterations=iterations)