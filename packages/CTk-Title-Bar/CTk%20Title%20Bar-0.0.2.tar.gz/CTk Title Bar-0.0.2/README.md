To create customize title bar for window(Tkinter)

Example :

from tkinter import *
from CTkTitle.CTkTitle import CTkTitlebar

root = Tk()
root.geometry('500x450')
CTkTitlebar().Header(master=root, title='Customized Title Bar',icon_path=r'\ctbimage.png')

root.mainloop()