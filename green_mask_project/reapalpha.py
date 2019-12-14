import os
import glob
from PIL import Image

def reapalpha (rgbvals, trhold):
	rlow = rgbvals[0]-trhold
	if (rlow < 0):
		rlow = 0
	rhigh = rgbvals[0]+trhold+1
	if (rhigh >255):
		rhigh = 255

	glow = rgbvals[1]-trhold
	if (glow < 0):
		glow = 0
	ghigh = rgbvals[1]+trhold+1
	if (ghigh >255):
		ghigh = 255

	blow = rgbvals[2]-trhold
	if (blow < 0):
		blow = 0
	bhigh = rgbvals[2]+trhold+1
	if (bhigh >255):
		bhigh = 255
	
	rootdir = "../decensor_output"
	files = glob.glob(rootdir + '/**/*.png', recursive=True)
	err_files = []

	for f in files:
		try:
			img = Image.open(f)
			img = img.convert("RGBA")
			pixdata = img.load()
			for y in range(img.size[1]):
				for x in range(img.size[0]):
					if pixdata[x, y][0] in range(rlow,rhigh) and pixdata[x, y][1] in range(glow,ghigh) and pixdata[x, y][2] in range(blow,bhigh):
						pixdata[x, y] = (255, 255, 255, 0)
			
			AA = input('Would you like to apply "anti-aliasing" (it will take some time) [n]') or "n"
			if (AA == "y") or (AA == "Y"):
				for y in range(1, img.size[1]):
					for x in range(1, img.size[0]):
						try:
							if pixdata[x, y][3] != 0:
								if (pixdata[x-1, y][3] == 0) or (pixdata[x+1, y][3] == 0) or (pixdata[x, y-1][3] == 0) or (pixdata[x, y+1][3] == 0):
									pixdata[x, y] = (pixdata[x, y][0], pixdata[x, y][1], pixdata[x, y][2], 65)
						except:
							pass

				for y in range(1, img.size[1]):
					for x in range(1, img.size[0]):
						try:
							if pixdata[x, y][3] != 0 and (pixdata[x, y][3] != 65):
								if (pixdata[x-1, y][3] == 65) or (pixdata[x+1, y][3] == 65) or (pixdata[x, y-1][3] == 65) or (pixdata[x, y+1][3] == 65):
									pixdata[x, y] = (pixdata[x, y][0], pixdata[x, y][1], pixdata[x, y][2], 195)
						except:
							pass

			f=f.replace("decensor_output", "decensor_realpha", 1)
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

if __name__ == "__main__":
	realpha = input("Would you like to change default color (240, 240, 240) and threshold (5)? [y/N] ") or "n"
	trhold = 5
	rgbvals = 240, 240, 240
	if (realpha == "y") or (realpha == "Y"):
		rgbvals = eval(input('Write your BG color that will be re-masked (write with commas): [240, 240, 240] ') or '240, 240, 240')
		trhold = int(input('Write your threshold value: [5] ') or '5')
	reapalpha(rgbvals, trhold)