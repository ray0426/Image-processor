import tkinter as tk
from PIL import Image, ImageTk

class main_Window ():
    def __init__(self, img_data):
        self.img_index = 0
        self.img_data = img_data
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
        self.refresh_exhibit()

    def create_menu(self):
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.new_item = tk.Menu(self.menu, tearoff=0)
        self.new_item.add_command(label='New', command=lambda: print("menu-new"))
        self.menu.add_cascade(label='File', menu=self.new_item)

    # refresh the exhibit place of image
    def refresh_exhibit(self):
        print(int(len(self.img_data)))
        for i in range(int(len(self.img_data) / 5) + 1):
            self.fr_exhibit.rowconfigure(i, weight=1, minsize=220)

            for j in range(5):
                self.fr_exhibit.columnconfigure(j, weight=1, minsize=180)
                if (i * 5 + j) < len(self.img_data):
                    print("ya")
                    frame = tk.Frame(
                        master=self.fr_exhibit,
                        relief=tk.RAISED,
                        borderwidth=1
                    )
                    frame.grid(row=i, column=j, ipadx=5, ipady=5, padx=5, pady=5, sticky="nw")

                    img = Image.open('.\\pics\\59060131_p0_master1200.jpg')
                    img = img.resize(self.img_resize(img.size), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(img)
                    self.label = tk.Label(frame, image=photo, height=150, width=160)
                    self.label.image = photo # the image should be saved because photo is a local variable
                    self.label.pack(pady=5)

                    label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
                    label.pack()

    # function to resize the image with correct width height rate
    def img_resize(self, size):
        if size[0] > size[1]:
            return [156, int(156 * size[1] / size[0])]
        else:
            return [int(156 * size[0] / size[1]), 156]

if __name__ == '__main__':
    main_window = main_Window()