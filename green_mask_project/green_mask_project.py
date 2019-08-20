#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import glob
from PIL import Image

rootdir = "../decensor_input_original"
files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files=[]

#Options
GBlur = 3
CannyTr1 = 1
CannyTr2 = 35
LowRange = 5
HighRange = 20
DetectionTr = 0.3

change_set = raw_input("Would you like to change default settings? [y/N]") or "n"
if change_set == "y":
	GBlur = raw_input("Enter the Gaussian Blur value: [3]") or "3"
	CannyTr1 = raw_input("Enter the Canny Edge Detector Treshold 1 value: [1]") or "1"
	CannyTr2 = raw_input("Enter the Canny Edge Detector Treshold 2 value: [35]") or "35"
	LowRange = raw_input("Enter the Minimal Resolution Of Patterns: [5]") or "5"
	HighRange = raw_input("Enter the Maximal Resolution Of Patterns: [20]") or "20"
	DetectionTr = raw_input("Enter the Detection Treshold value: [0.3]") or "0.3"

#Create patterns
for masksize in range(LowRange, HighRange+1):
    maskimg = 2+masksize+masksize-1+2
    screen = (maskimg, maskimg)

    img = Image.new('RGB', screen, (0xff,0xff,0xff))

    pix = img.load()

    for i in range(2,maskimg,masksize-1):
        for j in range(2,maskimg,masksize-1):
            for k in range(0,maskimg):
                pix[i, k] = (0,0,0)
                pix[k, j] = (0,0,0)

    img.save("patterns/pattern"+str(masksize)+"x"+str(masksize)+".png")

#Working with files
for f in files:
	try:
		print(f)
		#Hack for non-typical images
		img_C = Image.open(f).convert("RGBA")
		x, y = img_C.size
		card = Image.new("RGBA", (x, y), (255, 255, 255, 3))
		card.paste(img_C, (0, 0, x, y), img_C)
		card.save(os.path.dirname(f) + '/temp.png', format="png")
		os.replace(os.path.dirname(f) + '/temp.png', f)
	
		img_rgb = cv2.imread(f)
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		img_gray = cv2.Canny(img_gray,CannyTr1,CannyTr2)
		img_gray = 255-img_gray
		img_gray = cv2.GaussianBlur(img_gray,(GBlur,GBlur),0)
#		cv2.imwrite('output_gray.png', img_gray)     #DEBUG

		#Detection
		for i in range(LowRange,HighRange+1):
			pattern_filename = "patterns/pattern"+str(i)+"x"+str(i)+".png"
			template = cv2.imread(pattern_filename, 0)
			w, h = template.shape[::-1]

			img_detection = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
			threshold = DetectionTr
			loc = np.where(img_detection >= threshold)
			for pt in zip(*loc[::-1]):
#				cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 1)     #DEBUG
				cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), -1)
#			cv2.imwrite('output_progress_'+str(i)+'.png', img_rgb)     #DEBUG
		#Change save path
		f=f.replace("/decensor_input_original", "/decensor_input", 1)
		#Preview
		cv2.imshow('window1', img_rgb)
#		cv2.imshow('window2', img_gray)     #DEBUG
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		#Save file
		os.makedirs(os.path.dirname(f), exist_ok=True)
		cv2.imwrite(os.path.dirname(f) + '/temp.png', img_rgb)     #hack for non-unicode chars
		os.replace(os.path.dirname(f) + '/temp.png', f)
	except Exception as Exception:
		err_files.append(os.path.basename(f) + ": " + str(Exception))
		pass
	
#Error list	
if err_files:
	print("\n" + "Could not mask those files: ") 
	for f in err_files:
		print(f)