import math
import random

import cv2
import numpy as np
import requests
from PIL import ImageFont, ImageDraw

img_path = 'test.jpg'
img = cv2.imread(img_path)
heigh, width = img.shape[:2]
# 缩小
# 双三次插值
img_resize = cv2.resize(img, (heigh, width), interpolation=cv2.INTER_AREA)

# 放大
img_resize = cv2.resize(img, (heigh, width), interpolation=cv2.INTER_LINEAR)


cv2.imwrite('img_resize.jpg', img_resize)



def standard_resize(img, resize_width, resize_height, transform_info=False, pad_value=0, pad_style='center'):
    """
    不改变图片宽高比，对图片进行缩放
    :param img:
    :param resize_height:
    :param resize_width:
    :param transform_info: False 仅返回变换后的图片 True 返回图片缩放率和填充像素， ratio_w, ratio_h, pad_w, pad_h
    :param pad_value 填充像素值
    :param pad_style 填充方式 center, right, left, random_w
    :return:
    """

    def resize(img, flag):
        scale_h = resize_height if flag == 0 else round(resize_width / w * h)
        scale_w = round(resize_height / h * w) if flag == 0 else resize_width
        img = cv2.resize(img, (scale_w, scale_h), interpolation=cv2.INTER_AREA)
        ratio_h = scale_h / h
        ratio_w = scale_w / w
        return img, ratio_w, ratio_h

    def pad(img):
        pad_img = np.zeros([resize_height, resize_width, 3], dtype=np.uint8) + pad_value
        pad_width = max(resize_width - img.shape[1], 0)
        pad_height = max(resize_height - img.shape[0], 0)
        if pad_style == 'center':
            s_h = math.ceil(pad_height / 2)
            s_w = math.ceil(pad_width / 2)
        elif pad_style == 'right':
            s_h = 0
            s_w = 0
        elif pad_style == 'random_w':
            s_w = random.randint(0, pad_width)
            s_h = math.ceil(pad_height / 2)
        else:
            s_h = pad_height
            s_w = pad_width
        pad_img[s_h:s_h + img.shape[0], s_w:s_w + img.shape[1], :] = img
        return pad_img, s_h, s_w

    h, w = img.shape[:2]
    ratio_w, ratio_h = 1, 1
    # 两个都大, 图片缩放按照差距较大的那个标准，然后对差距较大的做填充
    if h > resize_height and w > resize_width:
        flag = 0 if resize_height / h < resize_width / w else 1
        img, ratio_w, ratio_h = resize(img, flag)

    # 两个都小，图片填充
    elif w <= resize_width and h <= resize_height:
        pass

    # 其中一个大，其中一个小, 对大的那个做缩放，小的做填充
    else:
        flag = 0 if h - resize_height > w - resize_width else 1
        img, ratio_w, ratio_h = resize(img, flag)

    img, pad_h, pad_w = pad(img)

    if transform_info:
        return img, ratio_w, ratio_h, pad_w, pad_h
    return img


