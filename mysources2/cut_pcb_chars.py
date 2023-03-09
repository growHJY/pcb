# 本模块用于裁剪pcb字符模板
import os.path
import time
import cv2 as cv

pcb_id = "5"


def cut_chars(out_put_chars, in_put_pcb_char, pcb_char_loc_txt):
    in_put_img = cv.imread(in_put_pcb_char)

    gauss = cv.GaussianBlur(in_put_img, (5, 5), sigmaX=1, sigmaY=1)

    gray = cv.cvtColor(gauss, cv.COLOR_BGR2GRAY)

    binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)[1]

    open_mor = cv.morphologyEx(binary, cv.MORPH_OPEN, (5, 5))

    _, contours, h = cv.findContours(open_mor, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if os.path.exists(pcb_char_loc_txt):
        os.remove(pcb_char_loc_txt)

    for c in contours:
        x, y, w, h = cv.boundingRect(c)
        char_roi = in_put_img[y:y + 80, x:x + 80]
        # cv.imwrite(f"{out_put_chars}/{time.time()}.png", char_roi)
        time.sleep(0.001)
        with open(pcb_char_loc_txt, "a") as f:
            f.write(f"{x},{y},{w},{h}\n")


if __name__ == '__main__':
    for i in range(1, 6):
        cut_chars("C:/ssd/mysources2/pcb_imgs/characters/", f"C:/ssd/mysources2/pcb_imgs/{i}-pcb-area_char_area.png",
                  f"C:/ssd/mysources2/pcb_imgs/{i}-pcb-loc.txt")
    print("cut finish")
