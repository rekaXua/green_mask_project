#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import glob
from PIL import Image

#You can change those folder paths
rootdir = "../decensor_input_original"
outdir = "../decensor_input"
os.makedirs(rootdir, exist_ok=True)
os.makedirs(outdir, exist_ok=True)

files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files=[]
		
#Transparency remove option
transp_rem = input("Would you like to run transparency mask removal script? (It can be useful in some situations, but use it only if you know what you're doing. It's input is ../decensor_output and it will output into ../decensor_remasked) [y/N] ") or "n"

#Default options
GBlur = 3
CannyTr1 = 1
CannyTr2 = 35
LowRange = 5
HighRange = 20
DetectionTr = 0.3

convert = input('Would you like to convert input images? (Be advise, in few specific cases it can decrese the quality of images in input folder, but if an error occures - it need to be "y", but only for the first time) [y/N] ') or "n"
Prews = int(input("How many previews would you like to see (Every closed preview will already save detected file): [0] ") or "0")

def convertion (f):
	global convert
	if (convert == "y") or (convert == "Y"):
		#Dirty hack for non-typical images and non-unicode names (I blame CV2 for this)
		img_C = Image.open(f).convert("RGBA")
		x, y = img_C.size
		card = Image.new("RGBA", (x, y), (255, 255, 255, 0))
		card.paste(img_C, (0, 0, x, y), img_C)
		card.save('temp.png', format="png")
		return (cv2.imread('temp.png'))
	else:
		pilI = Image.open(f).convert('RGB') 
		cvI = np.array(pilI) 
		cvI = cvI[:, :, ::-1].copy() 
		return (cvI)
	
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

		img.save("patterns/pattern"+str(masksize)+"x"+str(masksize)+".png")

change_set("Would you like to change default settings? [y/N] ")
patterns()

#Working with files
for f in files:
	try:
		while True:
			print("Working on " + f)

			img_rgb = convertion(f)

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
					cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,0), -1)     #You can change here the color of mask
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
				
			if (convert == "y") or (convert == "Y"):     #replaces originals with converted
				os.replace('temp.png', f)

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
	
#Transparency remover itself
if (transp_rem == "y") or (transp_rem == "Y"):	
	input('Now run DCP and then press Enter to run Transparency Remove Script')
	import transparency_remove
	
#Error list	
if err_files:
	print("\n" + "Could not mask those files: ") 
	for f in err_files:
		print(f)