from PyQt5.QtCore import QObject,Qt,pyqtSignal,pyqtSlot,QTimer,QSize,QTime
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,QFrame,QPushButton,QGridLayout
from PyQt5.QtWidgets import QSizePolicy,QComboBox,QLabel,QSpinBox,qApp,QTextEdit,QDoubleSpinBox
from PyQt5.QtGui import QTextCursor,QPixmap
import cv2,sys,datetime
import numpy as np
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
from ctypes import *
__libc = cdll.LoadLibrary('C:/ssd/DLL1.dll')

def predict(imgSrc: str, rectTxt: str, xml: str, classfyName: str, featureName: str, saveBMPfile: str,
            posFile: str) -> bool:
    __libc.predict.restype = c_bool
    return __libc.predict(bytes(imgSrc, "utf-8"), bytes(rectTxt, "utf-8"), bytes(xml, "utf-8"),
                          bytes(classfyName, "utf-8"), bytes(featureName, "utf-8"), bytes(saveBMPfile, "utf-8"),
                          bytes(posFile, "utf-8"))


class MainWidget(QWidget):
    def __init__(self):
        # self.setWindowFlag(Qt.FramelessWindowHint)
        super().__init__()
        self.__setUI()
        self.connectUsrAct()
    def __del__(self):
        super().deleteLater()
        camera.freeCamera()

    def __setUI(self):
        #左侧纵向布局
        leftLayout = QVBoxLayout()
        leftLayout.setSpacing(1)
        titleText="大赛测试"
        self.setWindowTitle(titleText)
        title=QLabel(titleText)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font: 26pt "Ubuntu";color:rgb(0,0,255);') 
        leftLayout.addWidget(title)
        
        tmp=QGridLayout()
        tmp.setVerticalSpacing(1)
        tmp.setHorizontalSpacing(1)
        tmp.setAlignment(Qt.AlignRight)
        self.labelPicOne=self.__createImgLabel("图像1")
        self.labelPicTwo=self.__createImgLabel("图像2")
        tmp.addWidget(self.labelPicOne,0,0)
        tmp.addWidget(self.labelPicTwo,0,1)
        leftLayout.addLayout(tmp)
        self.btnCamera = QPushButton("图片处理")
        self.exit = QPushButton("退出")
        hmm = QHBoxLayout()
        hmm.addWidget(self.btnCamera)
        hmm.addWidget(self.exit)
        leftLayout.addLayout(hmm)
        self.setLayout(leftLayout)
    def __createImgLabel(self,info,isExpanding=True):
        label=QLabel(info)
        label.setAlignment(Qt.AlignCenter)
        label.setFrameShape(QFrame.Box)
        label.setScaledContents(False)
        if isExpanding ==True:
            label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        return label
    def setLabelImage(self,label:QLabel,imageFile:str):
        bmp=QPixmap()
        if bmp.load(imageFile):
            label.setPixmap(bmp.scaledToHeight(label.height()-2))
        else:
            label.setText('加载失败:'+imageFile)
        label.repaint()
    def match_pcb(self,img: str, template: str, threshold: int, xshift: int, yshift: int, twudth, hh, imgDst):
        imgSrc = cv2.imread(img)
        imgtemplate = cv2.imread(template)
        # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(imgSrc, imgtemplate, cv2.TM_CCOEFF_NORMED)
        # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < threshold:
            return False
        else:
            # 匹配值转换为字符串
            # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
            # 对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
            strmin_val = str(max_val)
            imgSrc = imgSrc[max_loc[1] + yshift:max_loc[1] + yshift + hh,
                     max_loc[0] + xshift:max_loc[0] + xshift + twudth]
            cv2.imwrite(imgDst, imgSrc)
            return True
    def actBtnCapture(self):
        cameraPic = "C:/ssd/libmod/test.jpg"
        self.setLabelImage(self.labelPicOne, cameraPic)
        imgPCB = "C:/ssd/libmod/pcb.jpg"
        img2 = "C:/ssd/libmod/Configures/mark.jpg"
        bRet = self.match_pcb(cameraPic, img2,0.7, -370,-646,953,725, imgPCB)
        if bRet == False:
            print("PCB板定位失败！")
            return None
        predict("C:/ssd/libmod/pcb.jpg", "C:/ssd/libmod/Configures/roi/rect1.txt", "C:/ssd/libmod/knn_histgram.xml", "knn", "histgram", "C:/ssd/libmod/imgprocess.jpg", "C:/ssd/libmod/result.txt")
        self.setLabelImage(self.labelPicTwo,"C:/ssd/libmod/imgprocess.jpg")
    def connectUsrAct(self):
        self.exit.clicked.connect(self.close)
        self.btnCamera.clicked.connect(self.actBtnCapture)
def main():
    app = QApplication(sys.argv)
    w = MainWidget()
    w.resize(2000, 800)
    w.show()
    sys.exit(app.exec_())


main()