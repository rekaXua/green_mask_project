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

#Default options
GBlur = 3
CannyTr1 = 1
CannyTr2 = 35
LowRange = 5
HighRange = 20
DetectionTr = 0.3

Prews = int(input("How many previews would you like to see (every closed preview will already save detected file): [0] ") or "0")

def change_set (message):
	global GBlur
	global CannyTr1
	global CannyTr2
	global LowRange
	global HighRange
	global DetectionTr
	
	change_set = input(message) or "n"
	if (change_set == "y") or (change_set == "Y"):
		GBlur = int(input('Enter the Gaussian Blur value: [' + str(GBlur) + '] ') or GBlur)
		CannyTr1 = int(input('Enter the Canny Edge Detector Treshold 1 value: [' + str(CannyTr1) + '] ') or CannyTr1)
		CannyTr2 = int(input('Enter the Canny Edge Detector Treshold 2 value: [' + str(CannyTr2) + '] ') or CannyTr2)
		LowRange = int(input('Enter the Minimal Resolution Of Patterns: [' + str(LowRange) + '] ') or LowRange)
		HighRange = int(input('Enter the Maximal Resolution Of Patterns: [' + str(HighRange) + '] ') or HighRange)
		DetectionTr = float(input('Enter the Detection Treshold value: [' + str(DetectionTr) + '] ') or DetectionTr)
		return "y"

#Create patterns
def patterns ():
	global LowRange
	global HighRange
	
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

change_set("Would you like to change default settings? [y/N] ")
patterns()

#Working with files
for f in files:
	try:
		while True:
			print("Working on " + f)
			#Dirty hack for non-typical images and non-unicode names (I blame CV2 for this)
			img_C = Image.open(f).convert("RGBA")
			x, y = img_C.size
			card = Image.new("RGBA", (x, y), (255, 255, 255, 3))
			card.paste(img_C, (0, 0, x, y), img_C)
			card.save('temp.png', format="png")
	
			img_rgb = cv2.imread('temp.png')
			img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
			img_gray = cv2.Canny(img_gray,CannyTr1,CannyTr2)
			img_gray = 255-img_gray
			img_gray = cv2.GaussianBlur(img_gray,(GBlur,GBlur),0)
#			cv2.imwrite('output_gray.png', img_gray)     #DEBUG

			#Detection
			for i in range(LowRange,HighRange+1):
				pattern_filename = "patterns/pattern"+str(i)+"x"+str(i)+".png"
				template = cv2.imread(pattern_filename, 0)
				w, h = template.shape[::-1]
			
				img_detection = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
				loc = np.where(img_detection >= DetectionTr)
				for pt in zip(*loc[::-1]):
#					cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), 1)     #DEBUG
					cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), -1)
#				cv2.imwrite('output_progress_'+str(i)+'.png', img_rgb)     #DEBUG

			#Previews
			if Prews > 0:
				cv2.imshow('Preview! Press any key or close to save', img_rgb)
#				cv2.imshow('preview_gray', img_gray)     #DEBUG
				cv2.waitKey(0)
				cv2.destroyAllWindows()
				if (change_set("Would you like to correct your settings? [y/N] ") == "y"):
					patterns()
					continue
				Prews -= 1

			os.replace('temp.png', f)
			#Change path to save folder
			f=f.replace("/decensor_input_original", "/decensor_input", 1)
			#Save file
			os.makedirs(os.path.dirname(f), exist_ok=True)
			cv2.imwrite('temp_out.png', img_rgb)     #still a hack for non-unicode names
			os.replace('temp_out.png', f)
			break
	except Exception as Exception:
		err_files.append(os.path.basename(f) + ": " + str(Exception))
		pass
	
#Error list	
if err_files:
	print("\n" + "Could not mask those files: ") 
	for f in err_files:
		print(f)
