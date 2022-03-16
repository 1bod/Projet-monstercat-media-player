"""Module contenant les fonctions de l'interface graphique du projet jukebox"""

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image

class App(tk.Frame):
    """Classe principale de l'interface graphique"""
    def __init__(self, master:tk.Tk, sorties, jukebox):
        super().__init__(master)

        self.configure(background="red")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        #self.iconbitmap("jukebox.ico")
        b=tk.Button(self.master, text="Quitter", command=self.destroy_window_object)
        b.grid(row=0, column=0, sticky="nsew")
        i=0
        for sortie in sorties:
            image=ImageTk.PhotoImage(Image.open(sortie[2]).resize((300,300)))
            button_sortie=tk.Button(self.master, borderwidth=0, image=image, height=300, width=300, command=lambda sortie=sortie:jukebox.jouer(sortie[1]))
            button_sortie.grid(row=i//3, column=i%3, sticky="wn")
            i+=1
        self.grid(row=0, column=0, sticky="nsew")
        
    def destroy_window_object(self):
        """Destruction de l'interface graphique"""
        self.destroy()
        super().destroy()
    


class Chargement(tk.Tk):
    """Fenêtre de chargement au démarrage"""
    def __init__(self, message:str, geometry="300x80", title="Chargement",callback=None):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.label = tk.Label(self, text=message)
        self.label.pack(side="top", pady=10)
        self.progressbar=ttk.Progressbar(self, orient="horizontal", length=260, mode="determinate")
        self.progressbar.pack(side="top", padx=20)
        self.after(100, lambda: callback(self))
    
    def add_progress(self, value:int):
        """Ajoute une valeur à la progressbar"""
        self.progressbar.step(value)
    
    def set_progress(self, value:int):
        """Met à jour la progressbar"""
        self.progressbar.config(value=value)
        
    def start_progress(self, interval:int):
        """Démarre la progressbar"""
        self.progressbar.start(interval)
        
    def start(self):
        """Démarre la fenêtre de chargement"""
        self.mainloop()

    def destroy_window_object(self):
        """Destruction de la fenêtre de chargement"""
        self.destroy()
        super().destroy()
