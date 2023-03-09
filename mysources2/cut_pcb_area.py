import os

import cv2 as cv


def template_pcb(source_path, save_path, template_path):
    # 裁剪pcb
    source = cv.imread(source_path)
    template_mat = cv.imread(template_path)

    result = cv.matchTemplate(source, template_mat, cv.TM_CCORR_NORMED)

    min_v, max_v, min_l, max_l = cv.minMaxLoc(result)

    # 这个是模板在未裁剪区域的坐标
    template_x, template_y = max_l[0], max_l[1]

    # 读取模板在pcb(裁剪好的)中的位置
    cut_template_x, cut_template_y = 0, 0
    with open("C:/ssd/mysources2/pcb_imgs/template_loc.txt", "r") as f:
        line = f.readline()
        cut_template_x = int(line.split(",")[0])
        cut_template_y = int(line.split(",")[1])

    # todo 这个值需要给我
    pcb_w, pcb_h = 2888, 2096

    with open("C:/ssd/mysources2/pcb_imgs/PCB_loc.txt", "r") as f:
        line = f.readline()
        pcb_x = int(line.split(",")[0])
        pcb_y = int(line.split(",")[1])

    roi = source[template_y - cut_template_y:pcb_h + pcb_y, template_x - cut_template_x:pcb_w + pcb_x]

    cv.imwrite(save_path, roi)

    # 裁剪字符部分
    cut_char_area_x, cut_char_area_y, cut_char_area_w, cut_char_area_h = 0, 0, 0, 0
    with open("C:/ssd/mysources2/pcb_imgs/char_area_loc.txt", "r") as f:
        line = f.readline()
        cut_char_area_x = int(line.split(",")[0])
        cut_char_area_y = int(line.split(",")[1])
        cut_char_area_w = int(line.split(",")[2])
        cut_char_area_h = int(line.split(",")[3])

    pcb_char_roi_name = save_path.split("/")[-1].split(".")[0]
    pcb_char_save_path = save_path[:save_path.rindex("/")] + "/" + pcb_char_roi_name + "_char_area.png"

    # 字符区域
    char_roi = roi[cut_char_area_y:cut_char_area_y + cut_char_area_h, cut_char_area_x:cut_char_area_x + cut_char_area_w]

    cv.imwrite(pcb_char_save_path, char_roi)

    # pcb测量面积区域
    cut_calc_area_x, cut_calc_area_y, cut_calc_area_w, cut_calc_area_h = 0, 0, 0, 0
    with open("C:/ssd/mysources2/pcb_imgs/calc_area_loc.txt", "r") as f:
        line = f.readline()
        cut_calc_area_x = int(line.split(",")[0])
        cut_calc_area_y = int(line.split(",")[1])
        cut_calc_area_w = int(line.split(",")[2])
        cut_calc_area_h = int(line.split(",")[3])
    area_roi = roi[cut_calc_area_y:cut_calc_area_y + cut_calc_area_h, cut_calc_area_x:cut_calc_area_x + cut_calc_area_w]

    pcb_calc_area = save_path.split("/")[-1].split(".")[0]
    calc_area_path = save_path[:save_path.rindex("/")] + "/" + pcb_calc_area + "_calc.bmp"

    cv.imwrite(calc_area_path, area_roi)
    return pcb_char_save_path, save_path, calc_area_path


if __name__ == '__main__':
    for i in range(1, 6):
        template_pcb(f"C:/ssd/mysources2/pcb_imgs/pcb_img/{i}.bmp",
                     f"C:/ssd/mysources2/pcb_imgs/{i}-pcb-area.bmp",
                     "C:/ssd/mysources2/pcb_imgs/template.bmp")
