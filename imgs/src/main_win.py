import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class main_Window ():
    def __init__(self, img_data):
        self.img_index = 0
        self.img_frames = ()
        self.img_info = img_data
        self.create_window()
        self.window.mainloop()
    
    def create_window(self):
        self.window = tk.Tk()
        self.window.title('Img Player')
        self.window.geometry('1024x600')
        self.window.minsize(1024, 660) 
        self.window.rowconfigure(0, minsize=660, weight=1) # height (row height)
        self.window.columnconfigure(0, minsize=124, weight=1)  # width (column width)
        self.window.columnconfigure(1, minsize=900, weight=1)  # width (column width)
        self.create_menu()
        self.fr_info = tk.Frame(self.window, bg='yellow')
        self.fr_exhibit = tk.Frame(self.window, bg='blue')
        self.btn_open = tk.Button(self.fr_info, text="Open")
        self.btn_save = tk.Button(self.fr_info, text="Save As...")
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5)
        self.fr_info.grid(row=0, column=0, sticky="nesw")
        self.fr_exhibit.grid(row=0, column=1, sticky="nesw")
        #self.refresh_exhibit()
        self.create_exhibit()
        self.refresh_img()

    def create_menu(self):
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.new_item = tk.Menu(self.menu, tearoff=0)
        self.new_item.add_command(label='New', command=self.test)
        self.menu.add_cascade(label='File', menu=self.new_item)

    def create_exhibit(self): #tkinter.Frame
        self.img_frames = np.empty((0), dtype=tk.Frame)
        self.imgs = np.empty((0), dtype=tk.Label)
        self.img_names = np.empty((0), dtype=tk.Label)
        for i in range(3):
            self.fr_exhibit.rowconfigure(i, minsize=220)
            for j in range(5):
                self.fr_exhibit.columnconfigure(j, minsize=180)
                frame = tk.Frame(
                    master=self.fr_exhibit,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.bind('<Enter>', self.enter)
                frame.bind('<Leave>', self.leave)
                frame.grid(row=i, column=j, ipadx=5, ipady=5, padx=5, pady=5, sticky="nw")
                self.img_frames = np.append(self.img_frames, frame)

                label_img = tk.Label(frame)
                label_img.pack(pady=5)
                self.imgs = np.append(self.imgs, label_img)

                label_name = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
                label_name.pack()
                self.img_names = np.append(self.img_names, label_name)

    def refresh_img(self):
        index = 0
        for img_info_single in self.img_info:
            img = Image.open(img_info_single['src'])
            img = img.resize(self.img_resize(img.size), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgs[index].configure(image=photo, height=150, width=160)
            self.imgs[index].image = photo
            index = index + 1
            
    # function to resize the image with correct width height rate
    def img_resize(self, size):
        if size[0] > size[1]:
            return [156, int(156 * size[1] / size[0])]
        else:
            return [int(156 * size[0] / size[1]), 156]

    def enter(self, event):
        print("Enter")
        print(event)

    def leave(self, event):
        print("Leave\n")

    def test(self):
        print(self.img_frames)
        #print(self.imgs)
        for img in self.imgs:
            print(img)

if __name__ == '__main__':
    main_window = main_Window()