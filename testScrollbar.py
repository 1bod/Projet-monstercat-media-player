import tkinter as tk
from tkinter import Toplevel, ttk
from PIL import ImageTk, Image
window = tk.Tk()
window.geometry("500x500")



div = ttk.Frame(window)
container=tk.Toplevel(div)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame= ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e:canvas.configure(
        scrollregion=canvas.bbox("all")
        )
    )
scrollbar.bind("<MouseWheel>")

canvas.create_window((0,0),window=scrollable_frame,anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


#image1 = tk.PhotoImage(file = "image1.png")
#image2 = tk.PhotoImage(file = "image2.png")

image1 = ImageTk.PhotoImage(Image.open("images/COTW390.jpeg").resize((150,150), Image.ANTIALIAS))
image2 = ImageTk.PhotoImage(Image.open("images/MC029.jpeg").resize((150,150), Image.ANTIALIAS))

x = 0
y = 0
for i in range(50):
    #ttk.Label(scrollable_frame, text="Sample scrolling label").pack()
    
    ttk.Button(scrollable_frame, image=image1).grid(row=x,column=y)
    y+=1
    ttk.Button(scrollable_frame, image=image2).grid(row=x,column=y)
    y+=1
    ttk.Button(scrollable_frame, image=image1).grid(row=x,column=y)
    y=0
    x+=1
depart = 0
arrive = 10
barre = tk.Scale(window, orient='horizontal', from_=depart, to=arrive,
      resolution=0.1, tickinterval=2, length=350,)




#container.pack(fill="both", expand=True)
canvas.pack(side="left",fill="both",expand=True)
scrollbar.pack(side="right", fill="y")
barre.pack(fill="x")

#image1 = tk.PhotoImage(file = "image1.png")
#button_1 = tk.Button(window, image = image1)





window.mainloop()