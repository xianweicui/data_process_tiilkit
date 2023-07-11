import cv2


img_path = '/Users/admin/Desktop/huifeng/golf_image/1_1.jpg'
img = cv2.imread(img_path)
heigh, width = img.shape[:2]

print(heigh, width)