import tkinter as tk
from PIL import Image, ImageTk

class Window ():
    def __init__(self, data):
        self.img_index = 0
        self.img_list = data
        self.create_window()
        self.window.mainloop()
    
    def create_window(self):
        self.window = tk.Tk()
        self.window.title('Img Player')
        self.window.geometry('1280x960')
        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack()
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(side=tk.BOTTOM)
        img = Image.open(self.img_list[self.img_index]['src'])
        #img = img.resize((250, 250), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(img)
        self.label = tk.Label(self.top_frame, image=self.photo)
        self.label.pack()
        self.left_button = tk.Button(self.top_frame, text='pre', fg='red', command=self.img_pre)
        self.left_button.pack(side=tk.LEFT)

        self.right_button = tk.Button(self.top_frame, text='next', fg='blue', command=self.img_next)
        self.right_button.pack(side=tk.LEFT)

    def img_next(self):
        self.img_index = (self.img_index + 1) % len(self.img_list)
        img = Image.open(self.img_list[self.img_index]['src'])
        self.photo = ImageTk.PhotoImage(img)
        self.label.configure(image = self.photo)
        print(self.img_index)

    def img_pre(self):
        self.img_index = (self.img_index - 1) % len(self.img_list)
        img = Image.open(self.img_list[self.img_index]['src'])
        self.photo = ImageTk.PhotoImage(img)
        self.label.configure(image = self.photo)
        print(self.img_index)

#    def refresh_img(self):
#        img = Image.open(self.path_list[self.img_index])
#        label1.configure(image = displayImage)
#        self.photo = ImageTk.PhotoImage(img)


    