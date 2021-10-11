import pandas as pd
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import datetime
import pytesseract

"""
Functions:
1.1  ReadImage : 讀取圖檔
1.2  CvtThresh : 轉換二元化
1.3  hProject : 將圖像進行 Horizontal Split
1.4  Pytesseract : Tesseract_OCR
1.5  Text_Replace : 對指定的文本進行特定文字的取代
1.6  TextSplit : 對指定文本在特定位置進行截斷並選取截斷後所需要的部分，
                 並去除頭尾空白空格
"""



def ReadImage(path):
    AllFiles = os.listdir(path)
    return [np.asarray(Image.open(path+AllFiles[i])) for i in range(len(AllFiles)) if '.jpg' in AllFiles[i]]

def CvtThresh(image,thresh = 0,maxval = 170):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray,thresh,maxval,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]

def hProject(binary):
    h, w = binary.shape
    hprojection = np.zeros(binary.shape, dtype=np.uint8)
    h_h = [0]*h
    for j in range(h):
        for i in range(w):
            if binary[j,i] == 0:
                h_h[j] += 1
    for j in range(h):
        for i in range(h_h[j]):
            hprojection[j,i] = 255
    return h_h

def Pytesseract(image):
    def Image_Pytesseract(image,dilate_size=(2,25),dilate_iter=3,
                      thresh=127,maxval=255,blur_size=(3,3),sigmaX=1,sigmaY=2):
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        dilate = cv2.dilate(gray,dilate_size,iterations = dilate_iter)
        thresh = cv2.threshold(dilate,thresh,maxval,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        gaussian = cv2.GaussianBlur(thresh,blur_size,sigmaX,sigmaY)
        return gaussian
    return pytesseract.image_to_string(Image_Pytesseract(image),config='--psm 6',lang='eng+tha')## thresh = 0,maxval=150

def Text_Replace(text,old,new):
    return text.replace(old,new)

def TextSplit(text,keywords,index):
    return text.split(keywords)[index].strip()
 