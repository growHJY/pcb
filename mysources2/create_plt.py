import os.path

import matplotlib.pyplot as plt


def get_plt_img(ok_num, ng_num):
    print("create_plt:",
          ok_num, ng_num)
    # 数据
    x = ['ok', 'ng']
    y = [ok_num, ng_num]

    # 生成柱状图
    plt.bar(x, y)

    # 添加标题和标签
    plt.title('PCB result')
    # plt.xlabel('X')
    # plt.ylabel('Y')

    save_path = "C:/ssd/mysources2/pcb_imgs/plt.png"
    if os.path.exists(save_path):
        os.remove(save_path)

    # 显示图像
    plt.savefig(save_path)

    plt.clf()


if __name__ == '__main__':
    get_plt_img(10, 20)
