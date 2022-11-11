

center_x = 8
center_y = 8
for ring in range(1,3):
    print('\n', ring)
    for x, y in zip([1, 1, -1, -1], [1, -1, 1, -1]):

        val_x = x*(ring) +x  # + center_x 
        val_y = y*(ring) +y#  + center_y - y
        print(val_x, val_y)
