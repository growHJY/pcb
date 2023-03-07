import libs.imgproc as imgproc

pcb_path = "C:/ssd/mysources2/pcb_imgs/5-pcb-area.png"
pcb_zb = "C:/ssd/mysources2/data/2/1.txt"
xml_file = "C:/ssd/mysources2/train_res/5-pcb-knn-hog.xml"
classfyName = "knn"
featureName = "hog"
result_pcb_path = "C:/ssd/mysources2/train_res/5-pcb-res.bmp"
posFile = "C:/ssd/mysources2/train_res/5-pcb-info.txt"

imgproc.predict(pcb_path, pcb_zb, xml_file, classfyName, featureName, result_pcb_path, posFile)
