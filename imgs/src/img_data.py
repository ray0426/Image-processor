import os
import fnmatch
import json
import collections
import time

class Img_Data ():
    def __init__(self):
        self.load_data()
        self.imgPath = ".\pics"
        self.exts = ['*.jpg','*.jpeg','*.png']
        

    def load_data(self):
        print("load image data")
        with open('data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data

    def write_data(self):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        print("write data success!")

    def scan_imgs(self):
        matches = []
        for root, dirs, files in os.walk(self.imgPath):
            for ext in self.exts:
                for file in fnmatch.filter(files, ext):
                    match = {'ID' : '', 'page' : '', 'format' : '', 'tags' : [], 'load_time' : ''}
                    match['src'] = os.path.join(root, file)
                    ID_page = file.split("_")
                    format = file.split(".")[1]
                    match['ID'] = ID_page[0]
                    match['page'] = ID_page[1]
                    match['format'] = format
                    match['load_time'] = time_now()
                    matches.append(match)
        return matches
    
    def reset(self):
        self.data = self.scan_imgs()

    def reload(self):
        new_data_all = self.scan_imgs()
        for new_data in new_data_all:
            print(new_data['ID'])
            if [data for data in self.data if data['ID'] == new_data['ID'] and data['page'] == new_data['page']] == []:
                print("new data" + str(new_data['ID']))
                self.data.append(new_data)
        print("reload success!")

    def Search(self, ID, page):
        return [data for data in self.data if data['ID'] == ID and data['page'] == page][0]

def time_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())