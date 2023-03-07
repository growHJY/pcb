import imgproc

zb1 = "C:/ssd/data/2/1.txt"
mx1 = "C:/ssd/mysoruces/modexml/knn_hog.xml"
jg1 = "C:/ssd/mysoruces/result/1.txt"

imgproc.predict("C:/ssd/mysoruces/img/dest.bmp", zb1, mx1, "knn", "hog", "C:/ssd/mysoruces/result/dest.bmp", jg1)
print()