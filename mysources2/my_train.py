import libs.imgproc as imgproc
import cv2
import os

img_list = os.listdir("C:/ssd/mysources2/data/8/ng/")
for img in img_list:
    img_read = cv2.imread("C:/ssd/mysources2/data/8/ng/"+img)
    img_gray = cv2.cvtColor(img_read,cv2.COLOR_BGR2GRAY)
    img_thre = cv2.threshold(img_gray,150,255,cv2.THRESH_BINARY)[1]

    cv2.imshow("a", img_thre)
    cv2.waitKey()



# part_id = 4
# img_ok = f"C:/ssd/mysources2/data/{part_id}/ok/"
# img_ng = f"C:/ssd/mysources2/data/{part_id}/ng/"
# xml_path = f"C:/ssd/mysources2/train_res/{part_id}-knn-hog.xml"
#
# imgproc.train_knn_hog(img_ok, img_ng, xml_path)
