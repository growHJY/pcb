from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import By_matchTemplate as my_template
import By_create_plt as my_plt
import imgproc
import By_count_ok_ng as my_count
import os
import match_char as my_mc
import sys


class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.password_edit = None
        self.username_edit = None
        self.USERNAME = "GSJY"
        self.PASSWORD = "123456"

        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        # 设置背景图
        bg_pixmap = QPixmap("./test/dialog.png").scaled(800, 600)
        bg_palette = QPalette()
        bg_palette.setBrush(QPalette.Background, QBrush(bg_pixmap))
        self.setPalette(bg_palette)

        content = QVBoxLayout()

        form = self.login_form()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(form)
        hbox.addStretch(1)

        content.addStretch(1)
        content.addLayout(hbox)
        content.addStretch(1)

        self.setLayout(content)

    def login_form(self) -> QFormLayout:
        form = QFormLayout()

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.username_edit.setText(self.USERNAME)
        self.password_edit.setText(self.PASSWORD)
        self.password_edit.setEchoMode(QLineEdit.Password)

        form.addRow("用户名：", self.username_edit)
        form.addRow("密码：", self.password_edit)

        login_btn = QPushButton("登录")
        cancel_btn = QPushButton("取消")
        login_btn.clicked.connect(self.check_login)

        login_h_box = QHBoxLayout()
        login_h_box.addWidget(login_btn)
        login_h_box.addWidget(cancel_btn)
        form.addRow(login_h_box)

        return form

    def check_login(self):
        if self.USERNAME == self.username_edit.text() and self.PASSWORD == self.password_edit.text():
            print("login success")
            mainui = MainUI(self)
            mainui.show()
            self.hide()
        else:
            print("login fail")


class MainUI(QMainWindow):
    def __init__(self, parent):
        super(MainUI, self).__init__(parent)
        self.vbox = QVBoxLayout
        self.p3_pcb_char = QLabel
        self.char_list = []
        self.p3_pcb_count = QLabel
        self.p3_label = QLabel
        self.p4_pixmap = None
        self.p4_img_label = None
        self.p2_img_label = None
        self.p2_pixmap = None
        self.pcb_ok = 0
        self.pcb_ng = 0
        self.handle_pcb = "./img/5.bmp"
        self.initUI()

    def initUI(self):
        main_widget = QWidget()

        content_layout = self.content_ui()
        main_widget.setLayout(content_layout)

        self.setCentralWidget(main_widget)

    def content_ui(self) -> QVBoxLayout:
        content = QVBoxLayout()

        title = "广东省2022年度工业互联网边缘计算大赛"
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size:30px; color:blue")
        title_label.setAlignment(Qt.AlignHCenter)
        content.addWidget(title_label)

        content.addLayout(self.grid_layout())
        content.addLayout(self.port_inf())
        return content

    def grid_layout(self) -> QGridLayout:
        grid = QGridLayout()

        p1_img_label = QLabel()
        p1_img_label.setScaledContents(True)
        p1_pixmap = QPixmap(self.handle_pcb)
        p1_img_label.setMaximumSize(600, 600)
        p1_img_label.setPixmap(p1_pixmap)
        p1_img_label.setStyleSheet('border: 2px solid black; padding:5px')
        p1_img_label.setMinimumSize(600, 600)
        grid.addWidget(p1_img_label, 0, 0)

        self.p2_img_label = QLabel()
        self.p2_img_label.setScaledContents(True)
        self.p2_pixmap = QPixmap()
        self.p2_img_label.setMaximumSize(600, 600)
        self.p2_img_label.setPixmap(self.p2_pixmap)
        self.p2_img_label.setStyleSheet('border: 2px solid black; padding:5px')
        self.p2_img_label.setMinimumSize(600, 600)
        grid.addWidget(self.p2_img_label, 0, 1)

        self.vbox = QVBoxLayout()
        self.p3_label = QLabel("电路板信息: 等待识别...")
        self.p3_pcb_count = QLabel("电路板统计 ok=0,ng=0")
        self.p3_pcb_char = QLabel("字符识别")
        self.vbox.addWidget(self.p3_label)
        self.vbox.addWidget(self.p3_pcb_count)
        self.vbox.addWidget(self.p3_pcb_char)
        grid.addLayout(self.vbox, 1, 0)

        self.p4_img_label = QLabel()
        self.p4_img_label.setScaledContents(True)
        self.p4_pixmap = QPixmap()
        self.p4_img_label.setMaximumSize(600, 600)
        self.p4_img_label.setPixmap(self.p4_pixmap)
        self.p4_img_label.setStyleSheet('border: 2px solid black; padding:5px')
        self.p4_img_label.setMinimumSize(600, 600)
        grid.addWidget(self.p4_img_label, 1, 1)

        grid.setContentsMargins(10, 10, 10, 10)
        return grid

    def count_ok_ng(self, path):
        count = my_count.count_ok_ng("C:/ssd/mysoruces/result/1.txt")
        print(count)
        self.pcb_ok = count[0]
        self.pcb_ng = count[1]

        self.p3_pcb_count.setText(f"电路板统计 ok={self.pcb_ok},ng={self.pcb_ng}")

    def start_click(self):
        wait_handle = "C:/ssd/mysoruces/result/pcb_img.bmp"

        # 定位pcb
        a, b = my_template.template_pcb("./img/template.png", self.handle_pcb, wait_handle)

        zb1 = "C:/ssd/data/2/1.txt"
        mx1 = "C:/ssd/mysoruces/modexml/knn_hog.xml"
        jg1 = "C:/ssd/mysoruces/result/1.txt"
        # result_img = "C:/ssd/mysoruces/result/dest.bmp"
        result_txt_path = "C:/ssd/mysoruces/result/1.txt"

        if os.path.exists(result_txt_path):
            os.remove(result_txt_path)

        result = imgproc.predict(wait_handle, zb1, mx1, "knn", "hog", wait_handle, jg1)

        if result:
            self.p3_label.setText("电路板信息: ok")
            self.count_ok_ng(result_txt_path)
        else:
            self.p3_label.setText("电路板信息: ng")

        # 字符识别
        self.char_list = my_mc.template_char("C:/ssd/mysoruces/modexml/character/", wait_handle,a)

        char_str = ""
        for c in self.char_list:
            char_str += c + " "

        self.p3_pcb_char.setText(f"字符识别:{char_str}, 长度：{len(self.char_list)}")

        self.p2_pixmap = QPixmap(wait_handle)
        self.p2_img_label.setPixmap(self.p2_pixmap)

        my_plt.get_plt_img(self.pcb_ok, self.pcb_ng)
        self.p4_pixmap = QPixmap("./img/plt.png")
        self.p4_img_label.setPixmap(self.p4_pixmap)

    def port_inf(self) -> QHBoxLayout:
        content = QHBoxLayout()

        modbus_port = QLabel("ModBus端口:")
        modbus_port_combo = QComboBox()
        modbus_port_combo.addItems([f"COM{i}" for i in range(1, 4)])

        content.addWidget(modbus_port)
        content.addWidget(modbus_port_combo)

        robot_port = QLabel("ModBus端口:")
        robot_port_combo = QComboBox()
        robot_port_combo.addItems([f"COM{i}" for i in range(1, 4)])

        content.addWidget(robot_port)
        content.addWidget(robot_port_combo)

        begin_btn = QPushButton("开始")
        begin_btn.clicked.connect(self.start_click)
        stop_btn = QPushButton("停止")
        photo_btn = QPushButton("手动拍照")
        exit_btn = QPushButton("退出程序")

        content.addWidget(begin_btn)
        content.addWidget(stop_btn)
        content.addWidget(photo_btn)
        content.addWidget(exit_btn)

        return content


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    app.exec()
