import tkinter as tk
from PIL import Image, ImageTk

def show_img (path):
    root = tk.Tk()
    img = Image.open(path)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.pack()
    root.mainloop()