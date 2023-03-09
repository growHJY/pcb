from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cut_pcb_area as my_template
import create_plt as my_plt
import cut_pcb_chars as cut_chars
import imgproc
import count_ok_ng as my_count
import os
import match_chars as my_mc
import sys
import calc_area as calc


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
        bg_pixmap = QPixmap("./login/dialog.png").scaled(800, 600)
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


# 用于保存选择图片的变量
img_path = ""


class show_select_file_window(QMainWindow):
    def __init__(self, parent):
        global img_path
        super(show_select_file_window, self).__init__(parent)
        file_path, _ = QFileDialog.getOpenFileName(caption="选择文件", filter="ALL Files(*.*)")
        img_path = file_path


class MainUI(QMainWindow):
    def __init__(self, parent):
        super(MainUI, self).__init__(parent)
        self.p1_pixmap = QPixmap
        self.p1_img_label = QLabel
        self.vbox = QVBoxLayout
        self.p3_pcb_char = QLabel
        self.char_res = []
        self.p3_pcb_count = QLabel
        self.p3_label = QLabel
        self.p4_pixmap = None
        self.p4_img_label = None
        self.p2_img_label = None
        self.p2_pixmap = None
        self.pcb_ok = 0
        self.pcb_ng = 0
        self.handle_pcb = "C:/ssd/mysources2/pcb_imgs/pcb_img/1.bmp"
        self.gsjy_template = "C:/ssd/mysources2/pcb_imgs/template.png"
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

        self.p1_img_label = QLabel()
        self.p1_img_label.setScaledContents(True)
        self.p1_pixmap = QPixmap(self.handle_pcb)
        self.p1_img_label.setMaximumSize(600, 600)
        self.p1_img_label.setPixmap(self.p1_pixmap)
        self.p1_img_label.setStyleSheet('border: 2px solid black; padding:5px')
        self.p1_img_label.setMinimumSize(600, 600)
        grid.addWidget(self.p1_img_label, 0, 0)

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
        count = my_count.count_ok_ng(path)
        # print(count)
        self.pcb_ok = count[0]
        self.pcb_ng = count[1]

        self.p3_pcb_count.setText(f"电路板统计 ok={self.pcb_ok},ng={self.pcb_ng}")

    def start_click(self):
        pcb_area_img = f"C:/ssd/mysources2/pcb_imgs/{self.handle_pcb[self.handle_pcb.rfind('/') + 1:self.handle_pcb.rfind('.')]}-pcb-area.bmp"
        pcb_char_loc_txt = f"C:/ssd/mysources2/pcb_imgs/{self.handle_pcb[self.handle_pcb.rfind('/') + 1:self.handle_pcb.rfind('.')]}-pcb-loc.txt"

        # 定位裁剪pcb
        char_area_p, pcb_area_p, calc_area_p = my_template.template_pcb(self.handle_pcb, pcb_area_img,
                                                                        "C:/ssd/mysources2/pcb_imgs/template.bmp")

        cut_chars.cut_chars("C:/ssd/mysources2/pcb_imgs/characters", char_area_p, pcb_char_loc_txt)

        posFile = "C:/ssd/mysources2/train_res/pcb-predict-res.txt"

        if os.path.exists(posFile):
            os.remove(posFile)

        predict_list = []

        data_id = 1
        classfyName = "knn"
        featureName = "hog"
        pcb_zb = f"C:/ssd/mysources2/data/{data_id}/{data_id}.txt"
        xml_file = f"C:/ssd/mysources2/train_res/{data_id}-{classfyName}-{featureName}.xml"
        result = imgproc.predict(pcb_area_p, pcb_zb, xml_file, classfyName, featureName, pcb_area_p, posFile)
        predict_list.append(result)

        data_id = 2
        classfyName = "knn"
        featureName = "hog"
        pcb_zb = f"C:/ssd/mysources2/data/{data_id}/{data_id}.txt"
        xml_file = f"C:/ssd/mysources2/train_res/{data_id}-{classfyName}-{featureName}.xml"
        result = imgproc.predict(pcb_area_p, pcb_zb, xml_file, classfyName, featureName, pcb_area_p, posFile)
        predict_list.append(result)

        data_id = 3
        classfyName = "knn"
        featureName = "hog"
        pcb_zb = f"C:/ssd/mysources2/data/{data_id}/{data_id}.txt"
        xml_file = f"C:/ssd/mysources2/train_res/{data_id}-{classfyName}-{featureName}.xml"
        result = imgproc.predict(pcb_area_p, pcb_zb, xml_file, classfyName, featureName, pcb_area_p, posFile)
        predict_list.append(result)

        data_id = 4
        classfyName = "knn"
        featureName = "hog"
        pcb_zb = f"C:/ssd/mysources2/data/{data_id}/{data_id}.txt"
        xml_file = f"C:/ssd/mysources2/train_res/{data_id}-{classfyName}-{featureName}.xml"
        result = imgproc.predict(pcb_area_p, pcb_zb, xml_file, classfyName, featureName, pcb_area_p, posFile)
        predict_list.append(result)

        data_id = 5
        classfyName = "knn"
        featureName = "hog"
        pcb_zb = f"C:/ssd/mysources2/data/{data_id}/{data_id}.txt"
        xml_file = f"C:/ssd/mysources2/train_res/{data_id}-{classfyName}-{featureName}.xml"
        result = imgproc.predict(pcb_area_p, pcb_zb, xml_file, classfyName, featureName, pcb_area_p, posFile)
        predict_list.append(result)

        for r in predict_list:
            if r:
                if result:
                    self.p3_label.setText("电路板信息: ok")
                    self.count_ok_ng(posFile)
            else:
                self.p3_label.setText("电路板信息: ng")

        # 字符识别
        self.char_res = my_mc.match_chars("C:/ssd/mysources2/pcb_imgs/characters/", char_area_p, pcb_area_p,
                                          pcb_char_loc_txt)

        # 面积测量
        calc.match_draw_area(pcb_area_p, calc_area_p)

        self.p3_pcb_char.setText(f"字符识别:{self.char_res}, 长度：{int(len(self.char_res) / 2)}")

        self.p2_pixmap = QPixmap(pcb_area_p)
        self.p2_img_label.setPixmap(self.p2_pixmap)

        my_plt.get_plt_img(self.pcb_ok, self.pcb_ng)

        self.p4_pixmap = QPixmap("C:/ssd/mysources2/pcb_imgs/plt.png")
        self.p4_img_label.setPixmap(self.p4_pixmap)

    def selectFile(self):
        global img_path
        ss = show_select_file_window(self)
        ss.show()
        ss.hide()

        self.handle_pcb = img_path
        self.p1_pixmap = QPixmap(self.handle_pcb)
        self.p1_img_label.setPixmap(self.p1_pixmap)

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
        select_file = QPushButton("选择照片")

        select_file.clicked.connect(self.selectFile)

        content.addWidget(begin_btn)
        content.addWidget(stop_btn)
        content.addWidget(photo_btn)
        content.addWidget(exit_btn)
        content.addWidget(select_file)

        return content


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    app.exec()
