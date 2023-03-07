import os
import cv2 as cv


# 字符识别模块
def template_char(char_path, pcb_area_path, pcb_char_area, char_zb_txt_path):
    """
    字符识别模块
    :param char_path: 字符文件路径
    :param pcb_area_path: (整块)pcb路径
    :param pcb_char_area: pcb板字符区域路径
    :param char_zb_txt_path: 字符坐标路径
    """
    thresh = 0.9
    # 截取偏移量q
    offset = 0
    # 字符图片的文件数组
    chars_dir = os.listdir(char_path)

    # pcb字符区域的图像(测试用)
    char_area = cv.imread(pcb_char_area)

    # 整块pcb
    pcb_area = cv.imread(pcb_area_path)

    # 获取到整个字符区域在整块pcb板中的位置
    r = cv.matchTemplate(pcb_area, char_area, cv.TM_CCORR_NORMED)
    r_min_v, r_max_v, r_min_l, r_max_l = cv.minMaxLoc(r)

    with open(char_zb_txt_path, "r") as f:
        zbs = f.readlines()

        for char in chars_dir:
            char_name = char.split(".")[0]
            char_template = cv.imread(char_path + char)

            score_arr = []
            c_shape = char_template.shape[:2]
            for zb in zbs:
                x = int(zb[:-1].split(",")[0])
                y = int(zb[:-1].split(",")[1])
                w = int(zb[:-1].split(",")[2])
                h = int(zb[:-1].split(",")[3])
                # print(char_template.shape[0], h)

                char_roi = cv.imread(pcb_char_area)[y:y + h, x:x + w]
                cr = char_roi
                if w > c_shape[1] or h > c_shape[0]:
                    cr = cv.resize(char_roi, (c_shape[1], c_shape[0]))
                result = cv.matchTemplate(char_template, cr, cv.TM_CCORR_NORMED)
                # 这个值实在 char_roi 中匹配获得的
                roi_min_v, roi_max_v, roi_min_l, roi_max_l = cv.minMaxLoc(result)

                score_arr.append(
                    {
                        "score": roi_max_v,
                        "loc": (x, y, w, h),
                        "char": char_name
                    }
                )
            print(score_arr)

            max_score = score_arr[0]["score"]
            max_index = 0
            for index, ele in enumerate(score_arr):
                if ele["score"] > max_score:
                    max_score = ele['score']
                    max_index = index

            mx = score_arr[max_index]["loc"][0]
            my = score_arr[max_index]["loc"][1]
            mw = score_arr[max_index]["loc"][2]
            mh = score_arr[max_index]["loc"][3]
            mn = score_arr[max_index]["char"]

            if max_score > thresh:
                cv.putText(char_area, mn, (mx, my), cv.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2)
                cv.rectangle(char_area, (mx, my), (mx + mw, my + mh), (0, 0, 255), 3)

            print(score_arr[max_index])
            cv.imshow("pcb", char_area)
            cv.waitKey()
        # cv.imwrite(pcb_area_path, pcb_area)


if __name__ == '__main__':
    template_char("C:/ssd/mysoruces/modexml/character/", "C:/ssd/mysoruces/result/6-pcb-area.png"
                  , "C:/ssd/mysoruces/result/6-pcb-area_char_area.png", "C:/ssd/data/2/6_pcb_char_zb.txt")
