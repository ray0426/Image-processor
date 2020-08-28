import os
import fnmatch
import json
import collections
import time

class Img_Data ():
    def __init__(self, datapath = "data.json"):
        self.imgPath = ".\pics"
        self.dataPath = datapath
        self.load_data()
#        self.exts = ['*.jpg','*.jpeg','*.png']
        

    def load_data(self):
        print("load image data")
        if os.path.isfile(self.dataPath):
            with open(self.dataPath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print("load image data success!")
        else:
            print("load file fail!!")
            print("creating file: " + str(self.dataPath))
            with open(self.dataPath, 'w', encoding='utf-8') as f:
                f.write("[\n\n]")
            print("create file success!")
            self.data = []
        return self.data

    def write_data(self):
        print("write data")
        with open(self.dataPath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        print("write data success!")

    def data_add(self, info):
        if type(info) == dict:
            self.data.append(info)

#    def scan_imgs(self):
#        matches = []
#        for root, dirs, files in os.walk(self.imgPath):
#            for ext in self.exts:
#                for file in fnmatch.filter(files, ext):
#                    match = {'ID' : '', 'page' : '', 'format' : '', 'tags' : [], 'load_time' : ''}
#                    match['src'] = os.path.join(root, file)
#                    ID_page = file.split("_")
#                    format = file.split(".")[1]
#                    match['ID'] = ID_page[0]
#                    match['page'] = ID_page[1]
#                    match['format'] = format
#                    match['load_time'] = time_now()
#                    matches.append(match)
#        return matches
    
#    def reset(self):
#        self.data = self.scan_imgs()

#    def reload(self):
#        new_data_all = self.scan_imgs()
#        for new_data in new_data_all:
#            print(new_data['ID'])
#            if [data for data in self.data if data['ID'] == new_data['ID'] and data['page'] == new_data['page']] == []:
#                print("new data" + str(new_data['ID']))
#                self.data.append(new_data)
#        print("reload success!")

    def Search(self, ID, page):
        try:
            return [data for data in self.data if data['img_ID'] == ID and data['page'] == page][0]
        except:
            return None

def time_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())