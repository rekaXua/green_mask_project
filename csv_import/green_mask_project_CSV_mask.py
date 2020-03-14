#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import csv
import numpy as np
import os
import glob
from PIL import Image

#You can change those folder paths
rootdir = "./decensor_input_original"
outdir = "./decensor_masks"
pattdir = "./patterns"
os.makedirs(rootdir, exist_ok=True)
os.makedirs(outdir, exist_ok=True)
os.makedirs(pattdir, exist_ok=True)

#Default options
GBlur = 3
CannyTr1 = 30
CannyTr2 = 20
LowRange = 4
HighRange = 20
DetectionTr = 0.32
rgbvals = 255, 255, 255

files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files=[]

Prews = int(input("How many previews would you like to see (Every closed preview will already save detected file): [0] ") or "0")

	
def change_set (message):
	global GBlur
	global CannyTr1
	global CannyTr2
	global LowRange
	global HighRange
	global DetectionTr
	
	change_set = input(message) or "n"
	if (change_set == "y") or (change_set == "Y"):
		GBlur = int(input('Enter the Gaussian Blur value: (small odd number) [' + str(GBlur) + '] ') or GBlur)
		CannyTr1 = int(input('Enter the Canny Edge Detector Treshold 1 value: (1~200+, I also like it on 100) [' + str(CannyTr1) + '] ') or CannyTr1)
		CannyTr2 = int(input('Enter the Canny Edge Detector Treshold 2 value: (1~200+) [' + str(CannyTr2) + '] ') or CannyTr2)
		LowRange = int(input('Enter the Minimal Resolution Of Patterns: (3-Maximal Resolution) [' + str(LowRange) + '] ') or LowRange)
		HighRange = int(input('Enter the Maximal Resolution Of Patterns: (Minimal Resolution-20+, depends on resolution of image)[' + str(HighRange) + '] ') or HighRange)
		DetectionTr = float(input('Enter the Detection Treshold value: (0.00-1.00) [' + str(DetectionTr) + '] ') or DetectionTr)
		return "y"

#Create patterns
def patterns ():
	global LowRange
	global HighRange
	
	for masksize in range(LowRange, HighRange+1):
		maskimg = 2+masksize+masksize-1+2
		screen = (maskimg, maskimg)

		img = Image.new('RGB', screen, (255,255,255))

		pix = img.load()

		for i in range(2,maskimg,masksize-1):
			for j in range(2,maskimg,masksize-1):
				for k in range(0,maskimg):
					pix[i, k] = (0,0,0)
					pix[k, j] = (0,0,0)

		img.save(pattdir+"/pattern"+str(masksize)+"x"+str(masksize)+".png")

change_set("Would you like to change default settings? [y/N] ")
patterns()

#Working with files
with open('example.csv', 'w', newline='', encoding='utf-8') as f_output:     #CSV
	csv_output = csv.writer(f_output, quoting=csv.QUOTE_NONE, quotechar="", delimiter=",", escapechar=' ')     #CSV
	csv_output.writerow(['filename','file_size','file_attributes','region_count','region_id','region_shape_attributes','region_attributes'])     #CSV
	for f in files:
		try:
			while True:
				print("Working on " + f)

				img_C = Image.open(f).convert("RGB")
				x, y = img_C.size
				card = np.array(Image.new("RGB", (x, y), (rgbvals)))
				img_C = np.array(img_C) 
				img_rgb = img_C[:, :, ::-1].copy() 

				img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
				img_gray = cv2.Canny(img_gray,CannyTr1,CannyTr2)
				img_gray = 255-img_gray
				img_gray = cv2.GaussianBlur(img_gray,(GBlur,GBlur),0)

				req=[]
				#Detection
				for i in range(LowRange,HighRange+1):
					pattern_filename = pattdir+"/pattern"+str(i)+"x"+str(i)+".png"
					template = cv2.imread(pattern_filename, 0)
					w, h = template.shape[::-1]
				
					img_detection = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
					loc = np.where(img_detection >= DetectionTr)
					for pt in zip(*loc[::-1]):
						req.append([pt[0], pt[1], pt[0] + w, pt[1] + h])
						#cv2.rectangle(card, pt, (pt[0] + w, pt[1] + h), (0,255,0,255), -1)     #You can change here the color of the mask
				result, _ = cv2.groupRectangles(np.array(req).tolist(),0,0.01)
				for x1,y1,x2,y2 in result:
					cv2.rectangle(card,(x1,y1),(x2,y2),(0,255,0),-1)
				card = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
				ret, card = cv2.threshold(card,254,255,cv2.THRESH_BINARY_INV)
				conturs, _ = cv2.findContours(card,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)    #cv2.CHAIN_APPROX_SIMPLE, cv2.CHAIN_APPROX_TC89_L1, cv2.CHAIN_APPROX_TC89_KCOS
				#print(len(conturs))    #DEBUG
				outputBoxes = []
				for idx,conturJ in enumerate(conturs):
					outputX = []
					outputY = []
					for temp in conturJ:
						outputX.append(temp[0][0])
						outputY.append(temp[0][1])
					cv2.rectangle(img_rgb, cv2.boundingRect(conturs[idx]), (0,255,0), 1)
					outputBoxes.append(cv2.boundingRect(conturs[idx]))
					csv_output.writerow([os.path.basename(f), os.stat(f).st_size, '"{}"', len(conturs), idx, '"{""name"":""polygon""','""all_points_x"":' + str(outputX), '""all_points_y"":' + str(outputY) + '}"', '"{}"'])     #CSV

				#Previews
				if Prews > 0:
					cv2.imshow('Preview! Press any key or close to save', img_rgb)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
					if (change_set("Would you like to correct your settings? [y/N] ") == "y"):
						patterns()
						continue
					Prews -= 1

				#Change path to save folder
				f=f.replace(rootdir, outdir, 1)
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