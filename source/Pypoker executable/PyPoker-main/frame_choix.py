from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk

app = Tk()
app.title("Pypoker")
app.geometry("980x620")
app.resizable(width=False, height=False)

canva = Canvas(frame_choix, width=980, height=620)
canva.create_image(0, 0, anchor=NW, image=bgChoix)
canva.pack()
frame_choix.pack()

app.mainloop()