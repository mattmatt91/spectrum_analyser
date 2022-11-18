import numpy as np
from PIL import Image

men = ['onair\\on_air.png']
men_arr = []
miny = 16
minx = 16
for man in men:
    pix_arr_r = []
    pix_arr_c = []
    image = Image.open(man)
    pixels = list(image.getdata())
    width, height = image.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    for row, irow in zip(pixels, range(len(pixels))):
        for col, icol in zip(row, range(len(row))):
            if sum(col[0:3]) > 0:
                if irow  < minx:
                    minx = irow
                pix_arr_r.append(icol)
                if icol  < minx:
                    miny = icol
                pix_arr_c.append(irow)
    normalised = []
    # for pix in pix_arr:


    pix_arr = [[pix_arr_r[i], pix_arr_c[i]] for i in range(len(pix_arr_c))]
    
    men_arr.append(pix_arr)


i = 0
for man in men_arr:
    np.savetxt(f'on_air{i}', man, fmt='%i')
    i += 1


