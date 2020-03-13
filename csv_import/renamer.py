#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
import glob
from PIL import Image
import numpy as np

rootdir = "./decensor_input_original"
outdir = "./decensor_input"
files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files=[]

for f in files:
		try:
			with open(f,"rb") as file:
				byte = file.read()
			h = hashlib.md5(byte)
			output = h.hexdigest()
			os.rename(f, rootdir + "\\" + output + ".png")


			f=f.replace(rootdir, outdir, 1)
			os.rename(f, outdir + "\\" + output + ".png")
			
		except Exception as Exception:
			err_files.append(os.path.basename(f) + ": " + str(Exception))
			pass

if err_files:
	print("\n" + "Could not rename those files: ") 
	for f in err_files:
		print(f)