import cv2 as cv


def template_pcb(source_path, save_path):
    # 裁剪pcb
    source = cv.imread(source_path)

    roi = source[532:2161 + 532, 637:2957 + 637]
    cv.imwrite(save_path, roi)

    # 裁剪字符部分
    pcb_char_roi_name = save_path.split("/")[-1].split(".")[0]
    pcb_char_save_path = save_path[:save_path.rindex("/")] + "/" + pcb_char_roi_name + "_char_area.png"

    # todo 这里要知道字符区域的值具体是从哪来的
    # 字符区域
    char_roi = roi[1222:1222 + 376, 354:1023 + 354]

    cv.imwrite(pcb_char_save_path, char_roi)

    # pcb测量面积区域
    # 348， 484， 1023， 525
    area_roi = roi[484:484+525, 384:384+1023]
    pcb_calc_area = save_path.split("/")[-1].split(".")[0]
    calc_area_path = save_path[:save_path.rindex("/")] + "/" + pcb_calc_area + "_calc.bmp"

    cv.imwrite(calc_area_path, area_roi)
    return pcb_char_save_path, save_path, calc_area_path

if __name__ == '__main__':
    template_pcb("C:/ssd/mysources2/pcb_imgs/pcb_img/7.bmp",
                 "C:/ssd/mysources2/pcb_imgs/7-pcb-area.bmp")
