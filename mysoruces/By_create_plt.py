import matplotlib.pyplot as plt


def get_plt_img(ok_num, ng_num):
    # 数据
    x = ['ok', 'ng']
    y = [ok_num, ng_num]

    # 生成柱状图
    plt.bar(x, y)

    # 添加标题和标签
    plt.title('Bar Chart')
    plt.xlabel('X')
    plt.ylabel('Y')

    # 显示图像
    plt.savefig("./img/plt.png")


if __name__ == '__main__':
    get_plt_img(10, 20)
