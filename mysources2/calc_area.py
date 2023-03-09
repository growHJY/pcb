import cv2 as cv


def match_draw_area(pcb_path, calc_area_path):
    pcb_mat = cv.imread(pcb_path)
    calc_area_mat = cv.imread(calc_area_path)

    result = cv.matchTemplate(pcb_mat, calc_area_mat, cv.TM_CCORR_NORMED)

    min_v, max_v, min_l, max_l = cv.minMaxLoc(result)

    gauss = cv.GaussianBlur(calc_area_mat, (5, 5), sigmaX=1, sigmaY=1)
    gray = cv.cvtColor(gauss, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

    open_mor = cv.morphologyEx(binary, cv.MORPH_OPEN, (3, 3), iterations=4)

    _, contours, h = cv.findContours(open_mor, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
        x, y, w, h = cv.boundingRect(c)
        if w > 50:
            aw = round(1.2 * (w / 46), 2)
            ah = round(1.2 * (h / 46), 2)
            area = round(aw * ah, 3)
            cv.rectangle(pcb_mat, (x + max_l[0], y + max_l[1]), (x + max_l[0] + w, y + max_l[1] + h), (0, 255, 0), 3)

            font = cv.FONT_HERSHEY_SIMPLEX

            (font_size_w, font_size_h), _ = cv.getTextSize("hello", font, 2, 3)
            # 宽度 text
            middle_w = int(w / 2)
            cv.putText(pcb_mat, f"{aw}", (x + max_l[0] + middle_w, y + max_l[1]), font, 2, (255, 255, 255), 3)

            # 高度 text
            middle_h = int(h / 2)
            cv.putText(pcb_mat, f"{ah}", (x + max_l[0] - (font_size_w + 5), y + max_l[1] + middle_h), font, 2,
                       (255, 255, 255), 3)

            cv.imwrite(pcb_path, pcb_mat)


if __name__ == '__main__':
    match_draw_area(
        "C:/ssd/mysources2/pcb_imgs/1-pcb-area.bmp",
        "C:/ssd/mysources2/pcb_imgs/1-pcb-area_calc.bmp")
