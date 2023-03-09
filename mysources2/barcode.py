import cv2 as cv

img = cv.imread("C:/ssd/mysources2/pcb_imgs/pcb_img/barcode.jpg")

bar_roi = img[900:900 + 163, 687:687 + 405]
cv.imshow("original", bar_roi)

gaussia = cv.GaussianBlur(bar_roi, (5, 5), sigmaX=1, sigmaY=1)

gray = cv.cvtColor(gaussia, cv.COLOR_BGR2GRAY)

binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)[1]

_, contours, h = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# 存储条形码条状数据
bar_arr = []
# 左边数据
bar_left = []
# 右边数据
bar_right = []

for c in contours:
    x, y, w, h = cv.boundingRect(c)

    # Y小于100视为条形码
    if y < 100:
        cv.rectangle(bar_roi, (x, y), (x + w, y + h), (0, 255, 0), 1)
        bar_arr.append((x, y, w, h))

# 对在条形码数组内数据进行x排序，使得码的数据从左右到依次排好
for i in range(len(bar_arr) - 1):
    for j in range(len(bar_arr) - i - 1):
        if bar_arr[j][0] > bar_arr[j + 1][0]:
            temp = bar_arr[j]
            bar_arr[j] = bar_arr[j + 1]
            bar_arr[j + 1] = temp

# 中间的分割符
middle_bar_index = -1

for i in range(2, len(bar_arr)):
    if bar_arr[i][3] > 140:
        middle_bar_index = i
        break

A_O_DICT = {
    "0001101": "0", "0011001": "1", "0010011": "2", "0111101": "3", "0100011": "4", "0110001": "5",
    "0101111": "6",
    "0111011": "7", "0110111": "8", "0001011": "9"
}
B_E_DICT = {
    "0100111": "0", "0110011": "1", "0011011": "2", "0100001": "3", "0011101": "4", "0111001": "5",
    "0000101": "6",
    "0010001": "7", "0001001": "8", "0010111": "9"
}
# oe 字典
O_E_DICT = {
    "OOOOOO": "0", "OOEOEE": "1", "OOEEOE": "2", "OOEEEO": "3", "OEOOEE": "4", "OEEOOE": "5", "OEEEOO": "6",
    "OEOEOE": "7", "OEOEEO": "8", "OEEOEO": "9"
}

# 右侧偶性字符字典
C_E_DICT = {
    "1110010": "0",
    "1100110": "1",
    "1101100": "2",
    "1000010": "3",
    "1011100": "4",
    "1001110": "5",
    "1010000": "6",
    "1000100": "7",
    "1001000": "8",
    "1110100": "9",
}

# 奇偶排列数组
oe_arr = []

# 左边条形码数据
bar_left = bar_arr[:middle_bar_index + 1]

left_code = ""

# 条形码单更线的宽度
line_width = 3
# 计算宽度
for i in range(len(bar_left) - 1):
    black_bar = int(bar_left[i][2] / line_width)
    if black_bar > 4:
        black_bar = 4
    for b in range(black_bar):
        left_code += "1"
    white_bar = int((bar_left[i + 1][0] - (bar_left[i][0] + bar_left[i][2])) / line_width)
    if white_bar > 4:
        white_bar = 4
    for w in range(white_bar):
        left_code += "0"

left_code = left_code[3:-1]
count = int(len(left_code) / 7)

# 左侧结果

# 这个变量是保存最后解码出来的数字
left_num = ""
for i in range(count):
    left_res = ""
    for s in left_code[i * 7:i * 7 + 7]:
        left_res += s

    if A_O_DICT.get(left_res) is not None:
        oe_arr.append("O")
        left_num += A_O_DICT.get(left_res)
    if B_E_DICT.get(left_res) is not None:
        oe_arr.append("E")
        left_num += B_E_DICT.get(left_res)

# 这个变量表示由左侧数据推算出来的OE值
OEN = O_E_DICT.get("".join(oe_arr))

# 右侧条形码数据
bar_right = bar_arr[middle_bar_index + 2:]
# 计算宽度
right_code = ""
for i in range(len(bar_right) - 1):
    black_bar = int(bar_right[i][2] / line_width)
    if black_bar > 4:
        black_bar = 4
    for b in range(black_bar):
        right_code += "1"

    white_bar = int((bar_right[i + 1][0] - (bar_right[i][0] + bar_right[i][2])) / line_width)
    if white_bar > 4:
        white_bar = 4
    for w in range(white_bar):
        right_code += "0"

right_code = right_code[:-2]
# 右侧最终结果
count = int(len(right_code) / 7)

# 这个变量是保存最后解码出来的数字
right_num = ""
for i in range(count):
    right_res = ""
    for s in right_code[i * 7:i * 7 + 7]:
        right_res += s
    decode = C_E_DICT.get(right_res)
    right_num += decode

print(OEN + left_num + right_num)
