#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import csv
import numpy as np
import os
import glob
from PIL import Image

#You can change those folder paths
rootdir = "./decensor_input"
outdir = "./decensor_masks"
os.makedirs(rootdir, exist_ok=True)
os.makedirs(outdir, exist_ok=True)

rgbvals = 255, 255, 255

files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files=[]

#Working with files
with open('example.csv', 'w', newline='', encoding='utf-8') as f_output:     #CSV
	csv_output = csv.writer(f_output, quoting=csv.QUOTE_NONE, quotechar="", delimiter=",", escapechar='~')     #CSV
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
				
				mask = np.array([0,255,0], dtype = "uint16")
				card = cv2.inRange(img_rgb, mask, mask)

				conturs, _ = cv2.findContours(card,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
				outputBoxes = []
				for j in range(0,len(conturs)):
					cv2.rectangle(img_rgb, cv2.boundingRect(conturs[j]), (0,0,0), 1)
					outputBoxes.append(cv2.boundingRect(conturs[j]))
				#print(outputBoxes)     #DEBUG
				
				for idx,(x1,y1,x2,y2) in enumerate(outputBoxes):
					#cv2.rectangle(img_rgb,(x1,y1),(x2,y2),(255,255,255),-1)
					#rectNum=list(zip(*loc[::-1]))     #CSV
					csv_output.writerow([os.path.basename(f), os.stat(f).st_size, '"{}"', len(outputBoxes), idx, '"{""name"":""rect""','""x"":' + str(x1), '""y"":' + str(y1), '""width"":' + str(x2), '""height"":' + str(y2) + '}"', '"{}"'])     #CSV
					#print(outputBoxes)

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