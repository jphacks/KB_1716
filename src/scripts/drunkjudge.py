# -*- coding: utf-8 -*-
"""
2017/06/26
RGB値それぞれの画像
python 2.7.13
opencv 3.XX
numpy  1.12.1
"""
import numpy as np
import cv2
import sys

def drunkjudge(file_name):
        # 画像の読み込み
	img_color = cv2.imread(file_name)

        # RGB値をそれぞれ抽出
	imgR = img_color[:,:,2]
	imgG = img_color[:,:,1]
	imgB = img_color[:,:,0]
	
	average_color_per_row = np.average(img_color,axis=0)
	average_color = np.average(average_color_per_row, axis=0)
	average_color = np.uint8(average_color)
	
	average_sum = int(average_color[1])+int(average_color[0])+int(average_color[2])
	average_judge = (int(average_color[1])+int(average_color[0])) / float(average_color[2])
	
	#average_color_img = np.array([[average_color]*500]*500, np.uint8)

	#cv2.imshow('average',average_color_img)
	# 何かしらのキーを押せばwindowを閉じる
	#if cv2.waitKey(0):
	#	cv2.destroyAllWindows()
	if average_judge <= 1.2 :
		return -1
	elif average_judge <= 1.25 :
		return 0
	else :
		return 1


