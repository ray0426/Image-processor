import json
import os

import show_img
import img_data
import main_win

img_data = img_data.Img_Data(datapath = "data-temp - Copy.json")
#img_data.reset()
#print(img_data.data)
#img_data.scan_imgs()
#print(img_data.data)
#img_data.write_data()
img1 = img_data.Search("59060131", "p0")
#img_window = show_img.Img_Window(img_data.data)
main_window = main_win.main_Window(img_data.data)
#main_window.refresh_exhibit(img_data.data)