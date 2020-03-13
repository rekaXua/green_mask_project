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
outdir = "./decensor_input_original"
os.makedirs(rootdir, exist_ok=True)

rgbvals = 255, 255, 255

files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files=[]

#Working with files
with open('example.csv', 'w', newline='', encoding='utf-8') as f_output:     #CSV
	csv_output = csv.writer(f_output, quoting=csv.QUOTE_NONE, quotechar="", delimiter=",", escapechar=' ')     #CSV
	csv_output.writerow(['filename','file_size','file_attributes','region_count','region_id','region_shape_attributes','region_attributes'])     #CSV
	for f in files:
		try:
			print("Working on " + f)

			img_C = Image.open(f).convert("RGB")
			x, y = img_C.size
			card = np.array(Image.new("RGB", (x, y), (rgbvals)))
			img_C = np.array(img_C) 
			img_rgb = img_C[:, :, ::-1].copy() 
				
			mask = np.array([0,255,0], dtype = "uint16")
			card = cv2.inRange(img_rgb, mask, mask)
			cv2.imshow('Preview! Press any key or close to save', card)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			conturs, _ = cv2.findContours(card,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)    #cv2.CHAIN_APPROX_SIMPLE, cv2.CHAIN_APPROX_TC89_L1, cv2.CHAIN_APPROX_TC89_KCOS
			#print(conturs)
			f=f.replace(rootdir, outdir, 1)
			for idx,conturJ in enumerate(conturs):
				outputX = []
				outputY = []
				for temp in conturJ:
					outputX.append(temp[0][0])
					outputY.append(temp[0][1])
				csv_output.writerow([os.path.basename(f), os.stat(f).st_size, '"{}"', len(conturs), idx, '"{""name"":""polygon""','""all_points_x"":' + str(outputX), '""all_points_y"":' + str(outputY) + '}"', '"{}"'])     #CSV
		except Exception as Exception:
			err_files.append(os.path.basename(f) + ": " + str(Exception))
			pass

#Error list	
if err_files:
	print("\n" + "Could not mask those files: ") 
	for f in err_files:
		print(f)