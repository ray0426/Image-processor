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
        self.window.geometry('1024x576')
        self.menu_bar = tk.Frame(self.window, bg='white')
        self.menu_bar.pack(side=tk.TOP, fill='x', padx=2, pady=2, )
        self.content = tk.Frame(self.window, bg='white')
        self.content.pack(side=tk.BOTTOM, fill='x', padx=2, pady=2)
        self.left_frame = tk.Frame(self.content, bg='yellow')
        self.left_frame.pack(side=tk.LEFT, fill='y')
        self.right_frame = tk.Frame(self.content, bg='green')
        self.right_frame.pack(side=tk.RIGHT, fill='y')
        #self.left_button = tk.Button(self.bottom_frame, text='pre', fg='red', command=self.img_pre)
        #self.left_button.pack(side=tk.LEFT)

        #self.right_button = tk.Button(self.bottom_frame, text='next', fg='blue', command=self.img_next)
        #self.right_button.pack(side=tk.LEFT)


    