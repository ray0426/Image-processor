import json
import os

from show_img import *
from img_data import *

img_data = Img_Data()
#img_data.reset()
print(img_data.data)
img_data.reload()
print(img_data.data)
img_data.write_data()
img1 = img_data.Search("59060131", "p0")
window = Window(img_data.data)