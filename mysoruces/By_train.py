import imgproc

imgok = "C:/ssd/mysoruces/data/2/ok/"
imgng = "C:/ssd/mysoruces/data/2/ng/"
modexml = r'C:/ssd/mysoruces/modexml/knn_hog.xml'

imgproc.train_knn_hog(imgok, imgng, modexml)
