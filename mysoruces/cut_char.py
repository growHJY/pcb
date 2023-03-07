import random

import cv2 as cv
import time
import os

img = cv.imread("C:/ssd/mysoruces/result/6-pcb-area_char_area.png")

target_path = "C:/ssd/mysoruces/modexml/character/"

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

threshold, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

open_mor = cv.morphologyEx(binary, cv.MORPH_OPEN, (5, 5), iterations=3)

_, contours, hierarchy = cv.findContours(open_mor, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

pcb_char_zb = "C:/ssd/data/2/6_pcb_char_zb.txt"

if os.path.exists(pcb_char_zb):
    os.remove(pcb_char_zb)

offset = 20

for i, c in enumerate(contours):
    x, y, w, h = cv.boundingRect(c)

    with open(pcb_char_zb, "a") as f:
        f.write(f"{x},{y},{w},{h}\n")

    # cv.rectangle(img, (x,y),(x+w,y+h),(0,0,255),2)
    roi = img[y - offset:y + offset + h, x - offset:x + offset + w]
    # cv.imshow(f"{i}",roi)
    # cv.waitKey()
    cv.imwrite(target_path + f"{i}-{time.time()}-{random.randint(0, 100)}.png", roi)

# cv.imshow("img", img)
#
# cv.waitKey()
