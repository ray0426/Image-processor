import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import tag_data

class main_Window ():
    def __init__(self, img_data):
        self.img_index = 0
        self.img_frames = ()
        self.img_info = img_data
        self.img_tag = tag_data.Img_Tag()
        self.img_tag.load_tags()
        self.create_window()
        self.window.mainloop()

    def create_window(self):
        self.window = tk.Tk()
        self.window.overrideredirect(1)
        self.window.title('Img Player')
        self.window.geometry('1024x600')
        self.window.minsize(1200, 660)
        #self.window.maxsize(1200, 660)
        self.window.rowconfigure(0, minsize=330, weight=1) # height (row height)
        self.window.rowconfigure(1, minsize=330, weight=1) # height (row height)
        self.window.columnconfigure(0, minsize=250)  # width (column width)
        self.window.columnconfigure(1, minsize=930, weight=0)  # width (column width)
        #self.window.columnconfigure(2, minsize=2, weight=1)  # width (column width)
        #self.create_menu()
        
        self.create_filter()
        self.create_info()
        self.create_exhibit()

    def create_filter(self):
        self.filter = tk.Frame(self.window, bg='yellow')
        self.filter.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")

    def create_info(self):
        self.fr_info = tk.Frame(self.window, bg='pink')
        self.fr_info.grid(row=1, column=0, padx=3, pady=3, sticky="nesw")
        #self.fr_info.columnconfigure(0, minsize=20, weight=1)
        #self.fr_info.columnconfigure(1, minsize=10, weight=1)
        #self.fr_info.columnconfigure(2, minsize=2, weight=1)
        self.display_info = {}
        self.display_info['title'] = tk.Label(master=self.fr_info, font=("TkDefaultFont", 14), text="title: ")
        self.display_info['title'].grid(row=0, column=0, columnspan=3, ipadx=1, ipady=1, padx=4, pady=(4, 2), sticky="ew")
        self.display_info['painter'] = tk.Label(master=self.fr_info, font=("TkDefaultFont", 14), text="painter: ")
        self.display_info['painter'].grid(row=1, column=0, columnspan=3, ipadx=1, ipady=1, padx=4, pady=2, sticky="ew")
        self.display_info['paint_time'] = tk.Label(master=self.fr_info, font=("TkDefaultFont", 14), text="paint time: ")
        self.display_info['paint_time'].grid(row=2, column=0, columnspan=3, ipadx=1, ipady=1, padx=4, pady=2, sticky="ew")
        self.display_info['dl_time'] = tk.Label(master=self.fr_info, font=("TkDefaultFont", 14), text="dl time: ")
        self.display_info['dl_time'].grid(row=3, column=0, columnspan=3, ipadx=1, ipady=1, padx=4, pady=2, sticky="ew")
        self.display_info['id_page'] = tk.Label(master=self.fr_info, font=("TkDefaultFont", 14), text="id/page: ")
        self.display_info['id_page'].grid(row=4, column=0, columnspan=3, ipadx=1, ipady=1, padx=4, pady=2, sticky="ew")
        self.display_info['tags'] = tk.Label(master=self.fr_info, font=("TkDefaultFont", 14), text="tags: ")
        self.display_info['tags'].grid(row=5, column=0, ipadx=1, ipady=1, padx=4, pady=2, sticky="new")

        self.tags_canvas = tk.Canvas(self.fr_info, bg='#FFFFFF',scrollregion=(0,0,500,0))
        self.tags_vbar = ttk.Scrollbar(self.fr_info, orient='vertical')
        self.tags_vbar.grid(row=5, column=2, sticky="nesw")
        self.tags_vbar.config(command=self.tags_canvas.yview)
        self.tags_canvas.config(width=165,height=150)
        self.tags_canvas.config(yscrollcommand=self.tags_vbar.set) #xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.tags_canvas.grid(row=5, column=1, sticky="w")
        

        self.tags_list = tk.Frame(self.tags_canvas, bg='green')
        self.tags_list.configure(width=165, height=500)
        self.tags_canvas.create_window((0, 0), anchor='nw', window=self.tags_list)
        self.tags_list.bind(
            "<Configure>",
            lambda e: self.tags_canvas.configure(
                scrollregion=self.tags_canvas.bbox("all")
            )
        )

    def create_menu(self):
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.new_item = tk.Menu(self.menu, tearoff=0)
        self.new_item.add_command(label='New', command=self.test)
        self.menu.add_cascade(label='File', menu=self.new_item)

    def create_exhibit(self): #tkinter.Frame
        self.canvas = tk.Canvas(self.window, bg='blue', highlightthickness=0)
        self.vbar = tk.Scrollbar(self.window, orient='vertical')
        self.vbar.grid(row=0, column=2, rowspan=2, sticky="nesw")
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(width=930,height=660)
        self.canvas.config(yscrollcommand=self.vbar.set) #xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=1, rowspan=2, padx=(3, 0), pady=3, sticky="nesw")
        

        self.fr_exhibit = tk.Frame(self.canvas, bg='blue')
        self.canvas.create_window((3, 3), anchor='nw', window=self.fr_exhibit)
        self.fr_exhibit.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        #self.fr_exhibit.pack(side='left', expand=True, fill='both')
        #self.refresh_exhibit()
        self.img_frames = np.empty((0), dtype=tk.Frame)
        self.imgs = np.empty((0), dtype=tk.Label)
        self.img_names = np.empty((0), dtype=tk.Label)
        for i in range(10):
            self.fr_exhibit.rowconfigure(i, minsize=220)
            for j in range(5):
                self.fr_exhibit.columnconfigure(j, minsize=180)
                frame = tk.Frame(
                    master=self.fr_exhibit,
                    relief=tk.RAISED,
                    borderwidth=1,
                    bg='yellow'
                )
                frame.grid(row=i, column=j, ipadx=5, ipady=5, padx=(8, 0))
                frame.grid_remove()
                self.img_frames = np.append(self.img_frames, frame)

                label_img = tk.Label(frame)
                label_img.pack(pady=5)
                self.imgs = np.append(self.imgs, label_img)

                label_name = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
                label_name.pack()
                self.img_names = np.append(self.img_names, label_name)

        if len(self.img_info) != 0:
            self.focus = self.img_frames[0]
            self.img_frames[0].configure(bg='red', relief=tk.FLAT)
            self.display_info['title'].configure(text="title: " + str(self.img_info[0]['title']))
            self.display_info['painter'].configure(text="painter: " + str(self.img_info[0]['painter']))
            self.display_info['paint_time'].configure(text="paint time: " + str(self.img_info[0]['paint_time']).split(' ')[0])
            self.display_info['dl_time'].configure(text="dl time: " + str(self.img_info[0]['download_time']).split(' ')[0])
            self.display_info['id_page'].configure(text="id/page: " + str(self.img_info[0]['img_ID']) + 
                                               "-" + str(self.img_info[0]['page']))
        self.refresh_img()
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.bind_display()

    def refresh_img(self):
        index = 0
        for img_info_single in self.img_info:
            img = Image.open(img_info_single['src'])
            img = img.resize(self.img_resize(img.size), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgs[index].configure(image=photo, height=150, width=160)
            self.imgs[index].image = photo
            self.img_frames[index].grid()
            self.img_names[index].configure(text=img_info_single['title'])
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
        #print("Enter: " + str(index))
        if self.focus != self.img_frames[index]:
            self.img_frames[index].configure(bg='green')

    def leave(self, index):
        #print("Leave: " + str(index) + "\n")
        if not self.focus == self.img_frames[index]:
            self.img_frames[index].configure(bg='yellow')

    def click(self, index):
        #print("Click: " + str(index))
        self.focus.configure(bg='yellow', relief=tk.FLAT)
        self.focus = self.img_frames[index]
        self.img_frames[index].configure(bg='red', relief=tk.FLAT)
        self.display_info['title'].configure(text="title: " + str(self.img_info[index]['title']))
        self.display_info['painter'].configure(text="painter: " + str(self.img_info[index]['painter']))
        self.display_info['paint_time'].configure(text="paint time: " + str(self.img_info[index]['paint_time']).split(' ')[0])
        self.display_info['dl_time'].configure(text="dl time: " + str(self.img_info[index]['download_time']).split(' ')[0])
        self.display_info['id_page'].configure(text="id/page: " + str(self.img_info[index]['img_ID']) + 
                                               "-" + str(self.img_info[index]['page']))


    def release(self, index):
        #print("Release: " + str(index))
        #self.img_frames[index].configure(bg='green', relief=tk.RAISED,)
        return

    def click_double(self, index):
        #print("Double click: " + str(index))
        return

    def test(self):
        #print(self.img_frames)
        #print(self.imgs)
        for img in self.imgs:
            print(img)

if __name__ == '__main__':
    main_window = main_Window()