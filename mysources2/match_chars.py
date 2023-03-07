# 本模块用于匹配pcb字符区域的字符
import os

import cv2 as cv


def match_chars(input_chars_png_path, input_pcb_char_area_path, pcb_area, pcb_char_loc_txt):
    pcb_char_area_mat = cv.imread(input_pcb_char_area_path)

    pcb_area_mat = cv.imread(pcb_area)

    # 定位整块字符区域在pcb中的位置
    result = cv.matchTemplate(pcb_area_mat, pcb_char_area_mat, cv.TM_CCORR_NORMED)
    p_min_v, p_max_v, p_min_l, p_max_l = cv.minMaxLoc(result)

    gauss = cv.GaussianBlur(pcb_char_area_mat, (5, 5), sigmaX=1, sigmaY=1)
    gray = cv.cvtColor(gauss, cv.COLOR_BGR2GRAY)
    binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)[1]
    pcb_char_area_open_mor = cv.morphologyEx(binary, cv.MORPH_OPEN, (5, 5))

    chars_png_dir = os.listdir(input_chars_png_path)
    # todo 接下来的工作应该是处理循环的是字符的个数，而不是文件夹里图片的个数，因为会有一些重复的字符，会导致缺少识别的情况
    with open(pcb_char_loc_txt, "r") as f:
        zbs = f.readlines()

        match_result = []
        for zb in zbs:
            zb_x = int(zb.split(",")[0])
            zb_y = int(zb.split(",")[1])

            roi = pcb_char_area_open_mor[zb_y:zb_y + 64, zb_x:zb_x + 64]

            score_arr = []

            for char in chars_png_dir:
                char_mat = cv.imread(input_chars_png_path + char)
                char_name = char.split(".")[0]

                gauss = cv.GaussianBlur(char_mat, (5, 5), sigmaX=1, sigmaY=1)
                gray = cv.cvtColor(gauss, cv.COLOR_BGR2GRAY)
                binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)[1]
                char_open_mor = cv.morphologyEx(binary, cv.MORPH_OPEN, (5, 5))

                result = cv.matchTemplate(roi, char_open_mor, cv.TM_CCORR_NORMED)
                c_min_v, c_max_v, c_min_l, c_max_l = cv.minMaxLoc(result)
                # todo 判断时最好排序一下分数的高低情况，否则容易出现误判的情况
                score_arr.append({
                    "char": char_name,
                    "score": c_max_v,
                    "loc": (zb_x, zb_y)
                })

            max_score = 0
            max_index = -1

            for i, score in enumerate(score_arr):
                if score["score"] > max_score:
                    max_score = score['score']
                    max_index = i

            target_char = score_arr[max_index]

            match_result.append(target_char)

            cv.rectangle(pcb_area_mat, (target_char["loc"][0] + p_max_l[0], target_char["loc"][1] + p_max_l[1]),
                         (target_char["loc"][0] + p_max_l[0] + 64, target_char["loc"][1] + p_max_l[1] + 64),
                         (0, 0, 255), 4)
            cv.putText(pcb_area_mat, target_char["char"],
                       (target_char["loc"][0] + p_max_l[0], target_char["loc"][1] + p_max_l[1]),
                       cv.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 4)

        # rp = cv.resize(pcb_area_mat, (600,600))
        # cv.imshow("a",rp)
        # cv.waitKey()

        cv.imwrite(pcb_area, pcb_area_mat)

        for j in range(len(match_result) - 1):
            for i in range(len(match_result) - 1 - j):

                if match_result[i]["loc"][1] > match_result[i + 1]["loc"][1]:
                    temp = match_result[i]
                    match_result[i] = match_result[i + 1]
                    match_result[i + 1] = temp

        part1 = match_result[:int(len(match_result) / 2)]

        for j in range(len(part1) - 1):
            for i in range(len(part1) - 1 - j):

                if part1[i]["loc"][0] > part1[i + 1]["loc"][0]:
                    temp = part1[i]
                    part1[i] = part1[i + 1]
                    part1[i + 1] = temp

        part2 = match_result[int(len(match_result) / 2):]

        for j in range(len(part2) - 1):
            for i in range(len(part2) - 1 - j):

                if part2[i]["loc"][0] > part2[i + 1]["loc"][0]:
                    temp = part2[i]
                    part2[i] = part2[i + 1]
                    part2[i + 1] = temp

        res_arr = part1 + part2

        str_chars = ""
        for s in res_arr:
            str_chars += s['char'] + ' '

        return str_chars


if __name__ == '__main__':
    match_chars("C:/ssd/mysources2/pcb_imgs/characters/", "C:/ssd/mysources2/pcb_imgs/7-pcb-area_char_area.png"
                , "C:/ssd/mysources2/pcb_imgs/7-pcb-area.bmp",
                "C:/ssd/mysources2/pcb_imgs/7-pcb-loc.txt")
