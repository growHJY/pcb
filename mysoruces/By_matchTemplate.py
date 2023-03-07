import cv2 as cv


def template_pcb(template_path, source_path, save_path):
    # 裁剪pcb
    template = cv.imread(template_path)
    source = cv.imread(source_path)
    result = cv.matchTemplate(source, template, cv.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    h, w = template.shape[:2]
    loc = max_loc

    # cv.rectangle(source, loc, (loc[0] + w, loc[1] + h), (0, 0, 255), 10)

    roi = source[532:2161 + 532, 637:2957 + 637]
    cv.imwrite(save_path, roi)

    # 裁剪字符部分
    pcb_char_roi_name = save_path.split("/")[-1].split(".")[0]
    pcb_char_save_path = save_path[:save_path.rindex("/")] + "/" + pcb_char_roi_name + "_char_area.png"

    char_roi = roi[1222:1222 + 376, 354:1023 + 354]
    # cv.imshow("char_roi", char_roi)
    # cv.waitKey()
    cv.imwrite(pcb_char_save_path, char_roi)
    return pcb_char_save_path, save_path


if __name__ == '__main__':
    template_pcb("C:/ssd/mysoruces/img/template.png", "C:/ssd/mysoruces/img/6.bmp",
                 "C:/ssd/mysoruces/result/6-pcb-area.png")
