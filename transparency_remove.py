﻿import cv2
import os
import glob
from PIL import Image
import numpy

rootdir = "./decensor_output"
files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files = []

for f in files:
	try:
		pilI = Image.open(f).convert('RGB') 
		src = numpy.array(pilI) 
		src = src[:, :, ::-1].copy() 
		
		#src = cv2.imread(f, 1)
		
		tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
		_,alpha = cv2.threshold(tmp,255,255,cv2.THRESH_BINARY_INV)
		b, g, r = cv2.split(src)
		rgba = [b,g,r, alpha]
		dst = cv2.merge(rgba,4)
		f=f.replace("decensor_output", "decensor_remasked", 1)
		os.makedirs(os.path.dirname(f), exist_ok=True)
		cv2.imwrite('temp_tr.png', dst)
		os.replace('temp_tr.png', f)
	except Exception as Exception:
		err_files.append(os.path.basename(f) + ": " + str(Exception))
		pass
		
if err_files:
	print("\n" + "Could not mask those files: ") 
	for f in err_files:
		print(f)