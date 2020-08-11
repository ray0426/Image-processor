from tkinter import *
root=Tk()
root.maxsize(300, 300)
frame=Frame(root,width=300,height=300)
frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300)#,scrollregion=(0,0,300,600))
#hbar=Scrollbar(frame,orient=HORIZONTAL)
#hbar.pack(side=BOTTOM,fill=X)
#hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
canvas.config(yscrollcommand=vbar.set) #xscrollcommand=hbar.set, yscrollcommand=vbar.set)

frame_in = Frame(canvas, bg='blue', width=300, height=1000)
canvas.create_window(0, 0, window=frame_in)
frame_in.pack(side='left', expand=True, fill='both')

canvas.configure(scrollregion=canvas.bbox("all"))
canvas.pack(side=LEFT,expand=True,fill=BOTH)

root.mainloop()
