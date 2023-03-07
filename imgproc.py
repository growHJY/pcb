from ctypes import *
from os import path
import time,os
import numpy as np
import math
import random
import glob
import cv2

__libFile = "C:/ssd/DLL1.dll"
__libc = cdll.LoadLibrary(__libFile)


#模块1
# 图像光照均衡增强
def unevenLightCompensate_core(img,blockSize):
    if img.ndim == 3:
	    imgDst = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
 	    imgDst = img.copy()
    print(imgDst[0])
    average = cv2.mean(imgDst)[0]
    rows = imgDst.shape[0]
    cols = imgDst.shape[1]
    rows_new = math.ceil(rows)//blockSize
    cols_new = math.ceil(cols)//blockSize
    #创建全0矩阵
    blockImage = np.zeros((rows_new,cols_new),dtype=np.float32)
    for i in range(0,rows_new):
        for j in range(0,cols_new):
            rowmin = i*blockSize
            rowmax = (i+1)*blockSize
            if rowmax > rows:
                rowmax = rows
            colmin = j * blockSize
            colmax = (j+1)*blockSize
            if colmax > cols:
                colmax = cols
            imageROI = imgDst[rowmin:rowmax,colmin:colmax]
            temaver = np.mean(imageROI)
            blockImage[i,j]=temaver
    blockImage = blockImage - average
    blockImage2 = cv2.resize(blockImage,(cols,rows),cv2.INTER_CUBIC)
    image2 = imgDst.astype(np.float32)
    dst = image2 - blockImage2
    dst = dst.astype(np.uint8)
    return dst
    
        
def unevenLightCompensate(imgSrc:str, blockSize:int,imgDst:str):
    img=cv2.imread(imgSrc,cv2.IMREAD_COLOR)
    if img is None:
        print("unevenLightCompensate()函数 图像为空")
        return False
    if len(img.shape) == 2:		
        matimgDst = unevenLightCompensate_core(img,blockSize)
    elif  len(img.shape) == 3:	
        channels = img.shape[2]	#第三维度表示通道，应为3
        #rgb图像转换为hsv图像
        image_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #分离hsv彩色图像的h,s,v三通道
        channels = cv2.split(image_hsv)
        channels1 = channels[0]
        channels2 = channels[1]
        channels3 = channels[2]
        #只对v通道亮度空间进行光照均衡
        channel_new=unevenLightCompensate_core(channels3, blockSize)
        img=cv2.merge([channels1,channels2,channel_new])
        matimgDst = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    else:	#异常维度，不是图片了
        return False
    cv2.imwrite(imgDst,matimgDst)
    return True



# 模块2、 特征提取与分类器设计模块
# 2.1 使用4种分类器训练hog特征
# bool train_knn_hog(char *imgOk, char *imgNG, char *xml);


def train_knn_hog(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_knn_hog.restype = c_bool
    return __libc.train_knn_hog(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_svm_hog(char *imgOk, char *imgNG, char *xml);


def train_svm_hog(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_svm_hog.restype = c_bool
    return __libc.train_svm_hog(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_adaboost_hog(char *imgOk, char *imgNG, char *xml);


def train_adaboost_hog(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_adaboost_hog.restype = c_bool
    return __libc.train_adaboost_hog(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_randomTrees_hog(char *imgOk, char *imgNG, char *xml);


def train_randomTrees_hog(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_randomTrees_hog.restype = c_bool
    return __libc.train_randomTrees_hog(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# 2.2 使用4种分类器训练颜色直方图特征
# bool train_knn_histgram(char *imgOk, char *imgNG, char *xml);


def train_knn_histgram(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_knn_histgram.restype = c_bool
    return __libc.train_knn_histgram(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_svm_histgram(char *imgOk, char *imgNG, char *xml);


def train_svm_histgram(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_svm_histgram.restype = c_bool
    return __libc.train_svm_histgram(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_adaboost_histgram(char *imgOk, char *imgNG, char *xml);


def train_adaboost_histgram(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_adaboost_histgram.restype = c_bool
    return __libc.train_adaboost_histgram(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_randomTrees_histgram(char *imgOk, char *imgNG, char *xml);


def train_randomTrees_histgram(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_randomTrees_histgram.restype = c_bool
    return __libc.train_randomTrees_histgram(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# 2.3 使用4种分类器训练glcm纹理特征
# bool train_knn_glcm(char *imgOk, char *imgNG, char *xml);


def train_knn_glcm(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_knn_glcm.restype = c_bool
    return __libc.train_knn_glcm(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_svm_glcm(char *imgOk, char *imgNG, char *xml);


def train_svm_glcm(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_svm_glcm.restype = c_bool
    return __libc.train_svm_glcm(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_adaboost_glcm(char *imgOk, char *imgNG, char *xml);


def train_adaboost_glcm(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_adaboost_glcm.restype = c_bool
    return __libc.train_adaboost_glcm(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_randomTrees_glcm(char *imgOk, char *imgNG, char *xml);


def train_randomTrees_glcm(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_randomTrees_glcm.restype = c_bool
    return __libc.train_randomTrees_glcm(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# 2.4 使用4种分类器训练elbp局部二值模式特征
# bool train_knn_elbp(char *imgOk, char *imgNG, char *xml);


def train_knn_elbp(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_knn_elbp.restype = c_bool
    return __libc.train_knn_elbp(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_svm_elbp(char *imgOk, char *imgNG, char *xml);


def train_svm_elbp(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_svm_elbp.restype = c_bool
    return __libc.train_svm_elbp(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_adaboost_elbp(char *imgOk, char *imgNG, char *xml);


def train_adaboost_elbp(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_adaboost_elbp.restype = c_bool
    return __libc.train_adaboost_elbp(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_randomTrees_elbp(char *imgOk, char *imgNG, char *xml);


def train_randomTrees_elbp(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_randomTrees_elbp.restype = c_bool
    return __libc.train_randomTrees_elbp(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# 2.5 使用4种分类器训练gabor纹理特征
# bool train_knn_garbor(char *imgOk, char *imgNG, char *xml);


def train_knn_garbor(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_knn_garbor.restype = c_bool
    return __libc.train_knn_garbor(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_svm_garbor(char *imgOk, char *imgNG, char *xml);


def train_svm_garbor(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_svm_garbor.restype = c_bool
    return __libc.train_svm_garbor(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_adaboost_garbor(char *imgOk, char *imgNG, char *xml);


def train_adaboost_garbor(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_adaboost_garbor.restype = c_bool
    return __libc.train_adaboost_garbor(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))

# bool train_randomTrees_garbor(char *imgOk, char *imgNG, char *xml);


def train_randomTrees_garbor(imgOk: str, imgNG: str, xml: str) -> bool:
    __libc.train_randomTrees_garbor.restype = c_bool
    return __libc.train_randomTrees_garbor(bytes(imgOk, "utf-8"), bytes(imgNG, "utf-8"), bytes(xml, "utf-8"))





# 识别当前图像是否存在缺陷，选择的特征提取方法featureName, 分类器classfyName
# classfyName 分类器类型 “knn”  “svm”      “adaboost”  “randomtrees”
# featureName 特征类型   “hog”  “histgram” “glcm”  “elbp”   “garbor”
# bool predict(char *imgSrc, char *rectTxt, char *xml, char *classfyName, char *featureName, char *saveBMPfile, char *posFile);


def predict(imgSrc: str, rectTxt: str, xml: str, classfyName: str, featureName: str, saveBMPfile: str, posFile: str) -> bool:
    __libc.predict.restype = c_bool
    return __libc.predict(bytes(imgSrc, "utf-8"), bytes(rectTxt, "utf-8"), bytes(xml, "utf-8"), bytes(classfyName, "utf-8"), bytes(featureName, "utf-8"), bytes(saveBMPfile, "utf-8"), bytes(posFile, "utf-8"))


def match_pcb(img: str, template: str, threshold: int, xshift: int, yshift: int, twudth: int, hh: int, imgDst: str):
    imgSrc = cv2.imread(img)
    print(imgSrc.shape)
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


if __name__ == '__main__':
    imgok = "./data/2/ok"
    imgng = "./data/2/ng"
    modexml = './modexml/knn_hog.xml'

    train_knn_hog(imgok, imgng, modexml)