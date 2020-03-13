import os
import glob
from PIL import Image

rootdir = "./decensor_input"
files = glob.glob(rootdir + '/**/*.png', recursive=True)
err_files = []

for f in files:
	try:
		img = Image.open(f)
		img = img.convert("RGBA")
		pixdata = img.load()
		for y in range(img.size[1]):
			for x in range(img.size[0]):
				if pixdata[x, y][0] == 0 and pixdata[x, y][1] == 255 and pixdata[x, y][2] == 0:
					pixdata[x, y] = (0, 0, 0, 255)

		f=f.replace("decensor_input", "decensor_input_original", 1)
		os.makedirs(os.path.dirname(f), exist_ok=True)
		img.save(f)
	except Exception as Exception:
		err_files.append(os.path.basename(f) + ": " + str(Exception))
		pass
	
if err_files:
	print("\n" + "Could not mask those files: ") 
	for f in err_files:
		print(f)
pass