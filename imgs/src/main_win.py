import tkinter as tk
from PIL import Image, ImageTk

class main_Window ():
    def __init__(self):
        self.img_index = 0
        self.create_window()
        self.window.mainloop()
    
    def create_window(self):
        self.window = tk.Tk()
        self.window.title('Img Player')
        self.window.geometry('1024x600')
        self.window.minsize(1024, 600) 
        self.window.rowconfigure(0, minsize=600, weight=1) # height (row height)
        self.window.columnconfigure(0, minsize=124, weight=1)  # width (column width)
        self.window.columnconfigure(1, minsize=900, weight=1)  # width (column width)
        self.create_menu()
        #self.content = tk.Frame(self.window, bg='white')
        #self.content.pack(side=tk.BOTTOM, fill='x', padx=2, pady=2)
        self.fr_info = tk.Frame(self.window, bg='yellow')
        self.fr_exhibit = tk.Frame(self.window, bg='blue')
        self.btn_open = tk.Button(self.fr_info, text="Open")
        self.btn_save = tk.Button(self.fr_info, text="Save As...")
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5)
        self.fr_info.grid(row=0, column=0, sticky="nesw")
        self.fr_exhibit.grid(row=0, column=1, sticky="nesw")
        self.create_exhibit()

    def create_menu(self):
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.new_item = tk.Menu(self.menu, tearoff=0)
        self.new_item.add_command(label='New', command=lambda: print("menu-new"))
        self.menu.add_cascade(label='File', menu=self.new_item)

    def create_exhibit(self):
        for i in range(3):
            self.fr_exhibit.rowconfigure(i, weight=1, minsize=200)

            for j in range(5):
                self.fr_exhibit.columnconfigure(j, weight=1, minsize=180)

                frame = tk.Frame(
                    master=self.fr_exhibit,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j, padx=5, pady=5)

                img = Image.open('.\\pics\\59060131_p0_master1200.jpg')
                [imageSizeWidth, imageSizeHeight] = img.size
                img = img.resize((168, 168), Image.ANTIALIAS)
                self.photo = ImageTk.PhotoImage(img)
                self.label = tk.Label(frame, image=self.photo)
                self.label.pack()


                label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
                label.pack(padx=5, pady=5)


if __name__ == '__main__':
    main_window = main_Window()