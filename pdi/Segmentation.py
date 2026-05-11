import cv2
import numpy as np

class Segmentation:

    def florByMM(self, image, conn):
        #Conversión a HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        #Ecualización y blur
        v = cv2.equalizeHist(v)
        hsv = cv2.merge([h, s, v])
        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        #Máscara principal
        lower = np.array([0, 0, 159])
        upper = np.array([179, 255, 255])
        mask_main = cv2.inRange(hsv, lower, upper)

        #máscara de ruido (la que te faltaba)
        lower_noise = np.array([30, 0, 0])
        upper_noise = np.array([179, 255, 161])
        mask_noise = cv2.inRange(hsv, lower_noise, upper_noise)

        #Eliminación de ruido
        mask = cv2.bitwise_and(mask_main, cv2.bitwise_not(mask_noise))

        #Elemento estructurante
        ee = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

        #Morfología matemática
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, ee, iterations=6)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, ee, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ee, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, ee, iterations=1)

        mask = mask.astype(np.uint8)

        result = cv2.bitwise_and(image, image, mask=mask)
        imageContours = conn.getContoursWithMask(image, mask)

        return result, mask, imageContours
    
    def florByMaxMin(self, image, filtroMin, filtroMax, conn):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        v = cv2.equalizeHist(v)
        hsv = cv2.merge([h, s, v])

        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        mask = cv2.inRange(hsv, np.array([0, 0, 159]), np.array([179, 255, 255]))

        # ruido
        maskRuido = cv2.inRange(hsv, np.array([30, 0, 0]), np.array([179, 255, 161]))
        mask = cv2.bitwise_and(mask, cv2.bitwise_not(maskRuido))

        # FILTRO ITERATIVO
        for _ in range(4):
            mask = filtroMin(mask, 11)
            mask = filtroMax(mask, 11)

        mask = cv2.medianBlur(mask, 47)

        result = cv2.bitwise_and(image, image, mask=mask)

        imageContours = conn.getContoursWithMask(image, mask, k=-10)

        return result, mask, imageContours


    # =========================
    # PISTILO MM + CONTORNOS
    # =========================
    def pistiloByMM(self, image, conn):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        v = cv2.equalizeHist(v)
        hsv = cv2.merge([h, s, v])

        hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

        mask = cv2.inRange(hsv, np.array([16, 0, 239]), np.array([26, 255, 255]))

        ee = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, ee, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, ee, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ee, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, ee, iterations=1)

        result = cv2.bitwise_and(image, image, mask=mask)

        imageContours = conn.getContoursWithMask(image, mask)

        return result, mask, imageContours
