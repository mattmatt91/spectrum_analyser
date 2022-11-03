import numpy as np
from PIL import Image


men = ['m1.png', 'm2.png', 'm3.png']
men_arr = []
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
                pix_arr_r.append(icol)
                pix_arr_c.append(irow)
    normalised = []
    # for pix in pix_arr:
    pix_arr_c = [i - min(pix_arr_c) for i in pix_arr_c]
    pix_arr_r = [i - min(pix_arr_r) for i in pix_arr_r]

    pix_arr = [[pix_arr_r[i], pix_arr_c[i]] for i in range(len(pix_arr_c))]

    men_arr.append(pix_arr)
print(men_arr)

    


