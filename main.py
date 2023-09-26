from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Tweet Sheduler")
root.minsize(height=300, width=150)
frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

e1 = Entry(frm)
e2 = Entry(frm)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

root.mainloop()
