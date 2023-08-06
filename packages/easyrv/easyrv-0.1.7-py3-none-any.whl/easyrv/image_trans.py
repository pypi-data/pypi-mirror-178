# -*- coding: utf-8 -*-
# 作者: xwy
# 时间: 2022/7/22 18:42
# 版本: python3.10
import cv2
import numpy as np


def img_resize(image, shape):
    """
    图像转换为指定大小的正方形
    :param image: 输入图像
    :param shape: 输出图像尺寸
    :return: 返回转换后的尺寸
    """
    img_in = image.copy()
    img_h, img_w = img_in.shape[:2]
    img_out = np.zeros([max(img_w, img_h), max(img_w, img_h), 3], dtype=np.uint8) + 128
    img_out[0:img_h, 0:img_w, 0:3] = img_in[0:img_h, 0:img_w, 0:3]
    img_out = cv2.resize(img_out, shape)
    return img_out
