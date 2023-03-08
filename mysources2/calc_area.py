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
            # print(w, h)
            # print(f"w = {1.2*(w/46)} mm")
            # print(f"h = {1.2*(h/46)} mm")
            aw = 1.2 * (w / 46)
            ah = 1.2 * (h / 46)
            area = round(aw * ah, 3)
            cv.rectangle(pcb_mat, (x + max_l[0], y + max_l[1]), (x + max_l[0] + w, y + max_l[1] + h), (0, 255, 0), 3)
            cv.putText(pcb_mat, f"{area}", (x + max_l[0] - 5, y + max_l[1]), cv.FONT_HERSHEY_SIMPLEX, 2.0,
                       (255, 255, 255),
                       3)

    # cv.imwrite(pcb_path, pcb_mat)
    ri = cv.resize(pcb_mat, (600, 600))
    cv.imshow("img", ri)
    cv.waitKey()


if __name__ == '__main__':
    match_draw_area(
        "C:/ssd/mysources2/pcb_imgs/5-pcb-area.bmp",
        "C:/ssd/mysources2/pcb_imgs/5-pcb-area_calc.bmp")
