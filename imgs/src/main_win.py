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
        self.window.minsize(1200, 660)
        #self.window.maxsize(1200, 660)
        self.window.rowconfigure(0, minsize=660, weight=1) # height (row height)
        self.window.columnconfigure(0, minsize=200, weight=1)  # width (column width)
        self.window.columnconfigure(1, minsize=900, weight=1)  # width (column width)
        self.window.columnconfigure(2, minsize=2, weight=1)  # width (column width)
        self.create_menu()
        self.fr_info = tk.Frame(self.window, bg='yellow')
        self.btn_open = tk.Button(self.fr_info, text="Open")
        self.btn_save = tk.Button(self.fr_info, text="Save As...")
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5)
        self.fr_info.grid(row=0, column=0, sticky="nesw")

        self.canvas = tk.Canvas(self.window, bg='#FFFFFF',scrollregion=(0,0,00,600))
        self.vbar = tk.Scrollbar(self.window, orient='vertical')
        self.vbar.grid(row=0, column=2, sticky="nesw")
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300,height=300)
        self.canvas.config(yscrollcommand=self.vbar.set) #xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=1, sticky="nesw")
        

        self.fr_exhibit = tk.Frame(self.canvas, bg='blue', height=2000)
        self.canvas.create_window((0, 0), anchor='nw', window=self.fr_exhibit)
        #self.fr_exhibit.pack(side='left', expand=True, fill='both')
        #self.refresh_exhibit()
        self.create_exhibit()
        self.refresh_img()
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.bind_display()

        

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
        for i in range(100):
            self.fr_exhibit.rowconfigure(i, minsize=220)
            for j in range(5):
                self.fr_exhibit.columnconfigure(j, minsize=180)
                frame = tk.Frame(
                    master=self.fr_exhibit,
                    relief=tk.RAISED,
                    borderwidth=1,
                    bg='yellow'
                )
                frame.grid(row=i, column=j, ipadx=5, ipady=5, padx=5, pady=5, sticky="nw")
                frame.grid_remove()
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
            self.img_frames[index].grid()
            index = index + 1

        for i in range(index, 16):
            self.img_frames[index].grid_remove()
            
    # function to resize the image with correct width height rate
    def img_resize(self, size):
        if size[0] > size[1]:
            return [156, int(156 * size[1] / size[0])]
        else:
            return [int(156 * size[0] / size[1]), 156]

    def bind_display(self):
        for i in range(len(self.img_frames)):
            self.img_frames[i].bind('<Enter>', lambda event, index=i: self.enter(index))
            self.img_frames[i].bind('<Leave>', lambda event, index=i: self.leave(index))
            for widget in [self.img_frames[i], self.imgs[i], self.img_names[i]]:
                widget.bind('<Button-1>', lambda event, index=i: self.click(index))
                widget.bind('<ButtonRelease-1>', lambda event, index=i: self.release(index))
                widget.bind('<Double-Button-1>', lambda event, index=i: self.click_double(index))
                
                #self.img_frames[i].bind('<Button-1>', lambda event, index=i: self.click(index))
                #self.img_frames[i].bind('<ButtonRelease-1>', lambda event, index=i: self.release(index))
                #self.imgs[i].bind('<Button-1>', lambda event, index=i: self.click(index))
                #self.imgs[i].bind('<ButtonRelease-1>', lambda event, index=i: self.release(index))
                #self.img_names[i].bind('<Button-1>', lambda event, index=i: self.click(index))
                #self.img_names[i].bind('<ButtonRelease-1>', lambda event, index=i: self.release(index))
                


    def enter(self, index):
        print("Enter: " + str(index))
        self.img_frames[index].configure(bg='green')

    def leave(self, index):
        print("Leave: " + str(index) + "\n")
        self.img_frames[index].configure(bg='yellow')

    def click(self, index):
        print("Click: " + str(index))
        self.img_frames[index].configure(bg='red', relief=tk.FLAT,)

    def release(self, index):
        print("Release: " + str(index))
        self.img_frames[index].configure(bg='green', relief=tk.RAISED,)

    def click_double(self, index):
        print("Double click: " + str(index))

    def test(self):
        print(self.img_frames)
        #print(self.imgs)
        for img in self.imgs:
            print(img)

if __name__ == '__main__':
    main_window = main_Window()