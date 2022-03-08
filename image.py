#image.py
#module pour les images
#fabrique une liste d'images
import tkinter as tk
from PIL import ImageTk, Image

def creer_item(tim):
    """créatiion d'un item"""
    #tim+".jpeg" = "inombre.jpeg" (inombre=1;2;...9;20... )
    p1 = ImageTk.PhotoImage(Image.open(tim+".jpeg"))
    return p1

def liste_image(sorties):
    """fonction qui permet de créer une liste qui comporte les photos des titres"""
    liste=[]
    for sortie in sorties:
        liste.append(ImageTk.PhotoImage(Image.open(sortie[2]).resize((300, 300))))
    
    #items= len(sorties)*[""]
    #for i in range(len(sorties)):
        #le symbole / permet d'aller chercher les images dans le dossier images
     #   tim = "images/"+sorties[i][0]
      #  items[i]=creer_item(tim)
        
    return liste

def taille_photo (photo):
    """Détermibe la taile de la photo"""
    largeur=photo.width()
    hauteur=photo.height()
    return largeur,hauteur