#musique.py

from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from pygame import mixer
from image import *
import requests 
import shutil
import os
import monstercat_api

#   Le module pygame est utilisé pour la lecture des musiques en format mp3
#   En effet, l'api monstercat ne founit pas les fichiers audio au format mp3
#   winsound.PlaySound ne fonctionne pas avec les fichiers mp3
#   Pour installer pygame, la commande à executer dans un terminal est: pip3 install pygame
#
#   Amélioration appotées:
#   - Les 9 musiques sont tirées des dernières sorties de l'api monstercat
#   - Possibilité de télécharger les musiques directement depuis l'api monstercat
#


def debutmusique(audio):
    global musicPosFront
    mixer.music.load(audio)
    mixer.music.play()
    #PlaySound(son,1)

def stopmusique():
    global Continue
    Continue=False
    mixer.music.stop()
    #PlaySound(None,0)

def debut():
    global Continue, son
    if Continue==True and son != "":
        debutmusique(son)
        
def setVolume(volume):
    mixer.music.set_volume(volume/100)

class cdrom():
    def __init__(self, son=''):
        self.son=son
    def start(self):
        global son
        
        debut()

def change(numero, audio):
    global Continue, compt, son
    Continue = True
    son=audio[1]
    musique=cdrom()
    musique.start()
    
def openResearch():
    """Ouvre une fenêtre de recherche de musique"""
    global fenetreRecherche, nbRemplacement
    fenetreRecherche=Toplevel(fenetre)
    fenetreRecherche.title("Recherche de musique")
    fenetreRecherche.geometry("1100x700")
    fenetreRecherche.rowconfigure(0, weight=1)
    fenetreRecherche.columnconfigure(0, weight=1)
    termeRecherche = StringVar() 
    termeRecherche.set("")
    cadreRecherche=Frame(fenetreRecherche)
    cadreRecherche.pack(side=TOP, padx=5, pady=5)
    labelTermeARechercher=Label(cadreRecherche, text="Terme à rechercher : ")
    labelNombreDeResultats=Label(cadreRecherche, text="Nombre de tentatives : ")
    labelNombreRemplacement=Label(cadreRecherche, text="Numéro du titre à remplacer : ")
    labelTermeARechercher.grid(row=0, column=0)
    labelNombreDeResultats.grid(row=0, column=1)
    labelNombreRemplacement.grid(row=0, column=3)
    entree = Entry(cadreRecherche, textvariable=termeRecherche)
    entree.grid(row=1, column=0, padx=5, pady=5)
    nbResults=IntVar()
    nbResults.set(10)
    entreeNbResults = Spinbox(cadreRecherche, from_=1, to=100, textvariable=nbResults)
    entreeNbResults.grid(row=1, column=1, padx=5, pady=5)
    nbRemplacement=IntVar()
    nbRemplacement.set(9)
    entreeRemplacement=Spinbox(cadreRecherche, from_=1, to=9, textvariable=nbRemplacement)
    entreeRemplacement.grid(row=1, column=3, padx=5, pady=5)
    buttonRecherche = Button(cadreRecherche, text="Rechercher", command=lambda: recherche(termeRecherche.get(), nbResults.get(), cadreResultats))
    buttonRecherche.grid(row=1, column=2, padx=5, pady=5)
    canvas = Canvas(fenetreRecherche)
    cadreResultats = Frame(canvas)
    frameScrollbar=Frame(fenetreRecherche)
    frameScrollbar.pack(side=RIGHT, fill=Y)
    defilY = Scrollbar(frameScrollbar, orient='vertical', command=canvas.yview)
    cadreResultats.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0,0),window=cadreResultats,anchor="nw")
    #defilY.config(command=canvas.yview)
    #canvas['yscrollcommand'] = defilY.set
    canvas.configure(yscrollcommand=defilY.set)
    canvas.pack(side='top', padx=5, pady=5, fill='both', expand=True)
    defilY.pack(side='right', fill='y',)
    #defilY.grid(row=0, column=5, sticky='ns')
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    fenetreRecherche.bind_all("<MouseWheel>", on_mousewheel)



def charger(CatalogID:str, emplacementARemplacer:int):
    global fenetre
    print(CatalogID)
    audioPath, imagePath=monstercat_api.get_track(CatalogID, "chansons", "images")
    print(audioPath, imagePath)
    nouvelleIimage=ImageTk.PhotoImage(Image.open(imagePath).resize((300, 300)))

    lb2 = Button(fenetre,borderwidth=0, image=nouvelleIimage, command=lambda: change(emplacementARemplacer, [None, audioPath]), height=300, width=300)
    lb2.grid(row=((emplacementARemplacer-1)//3)*3, column=((emplacementARemplacer-1)%3)*3,columnspan=3, rowspan=3,sticky='wn')
    fenetreRecherche.destroy()
    fenetre.mainloop( )


    

def recherche(terme, nombre, fenetreResultats):
    """Recherche de musiques via l api monstercat et affichage des résultats"""
    res= requests.get("https://www.monstercat.com/api/catalog/browse?search={}&limit={}".format(terme,nombre)).json()["Data"]
    global titres
    titresCharges=[]
    titres=[]
    for resultat in res:
        CatalogID=resultat["Release"]["CatalogId"]
        if resultat["Streamable"]==True and not CatalogID in titresCharges:
            #on récupère l'image
            img_path=monstercat_api.get_cover(CatalogID, "images/")
            print("Image {}.jpeg téléchargée".format(CatalogID))
            
            img=ImageTk.PhotoImage(Image.open(img_path).resize((200,200)))
            titres.append((resultat["Release"]["Title"],img, CatalogID))
            titresCharges.append(CatalogID)
    
    
    resultats=monstercat_api.search(terme, nombre)
    for resultat in resultats:
        catalog_id=resultat["Release"]["CatalogId"]
    i=0
    for titre in titres:
        #on crée un bouton pour chaque résultat dans une grille avec 5 colonnes
        #chaque bouton est contenu dans un cadre
        frame=Frame(fenetreResultats)
        #print(i)
        bouton=Button(frame, image=titre[1], height=200, width=200,compound = TOP, command=lambda c=titre[2]: charger(c, nbRemplacement.get()))
        bouton.pack(side=TOP)
        lbl=Label(frame, text=titre[0])
        lbl.pack(side=BOTTOM)
        #print("position : x={} y={}".format(i%5, i//5))
        frame.grid(row=i//5,column=i%5)
        i+=1
    fenetreRecherche.update_idletasks()

def setProgression(nouvelleProgression:int):
    """Mets à jour la progression du titre"""
    global progression
    
    

def menu(fenetre, images, sons):
    global Continue, son
    #création des 9 boutons
    lb2 = Button(fenetre,borderwidth=0, image=images[0], command=lambda: change(0, sons[0]), height=300, width=300)
    lb2.grid(row=0, column=0,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[1], command=lambda: change(1, sons[1]), height=300, width=300)
    lb2.grid(row=0, column=3,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[2], command=lambda: change(2, sons[2]), height=300, width=300)
    lb2.grid(row=0, column=6,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[3], command=lambda: change(3, sons[3]), height=300, width=300)
    lb2.grid(row=3, column=0,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[4], command=lambda: change(4, sons[4]), height=300, width=300)
    lb2.grid(row=3, column=3,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[5], command=lambda: change(5, sons[5]), height=300, width=300)
    lb2.grid(row=3, column=6,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[6], command=lambda: change(6, sons[6]), height=300, width=300)
    lb2.grid(row=6, column=0,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[7], command=lambda: change(7, sons[7]), height=300, width=300)
    lb2.grid(row=6, column=3,columnspan=3, rowspan=3,sticky='wn')
    lb2 = Button(fenetre,borderwidth=0, image=images[8], command=lambda: change(8, sons[8]), height=300, width=300)
    lb2.grid(row=6, column=6,columnspan=3, rowspan=3,sticky='wn')
    ft="Times 12 bold"
    b2=Button(fenetre, text="Quitter", bg="red", font=ft, command=fenetre.destroy)
    b2.grid(row=0,column=9)
    b2=Button(fenetre, text="ON", bg="blue", fg="white", font=ft, command=debut)
    b2.grid(row=1,column=9)
    b2=Button(fenetre,text="OFF", bg="green", fg="white", font=ft, command=stopmusique)
    b2.grid(row=2,column=9)
    b2=Button(fenetre, text="Changer\nmusique", bg="yellow", fg="black", font=ft, command=openResearch)
    b2.grid(row=3,column=9)
    volume=IntVar()
    volume.set(100)
    scaleVolume=Scale(fenetre, from_=100, to=0, orient='vertical', variable=volume, command=lambda vol=volume.get(): setVolume(int(vol)))
    scaleVolume.grid(row=5,column=9)
    
    menuBas=Frame(fenetre)
    menuBas.grid(row=9,column=0,columnspan=10,sticky='nsew')
    #barre de progression du titre
    progressionBarre=IntVar()
    progressionBarre.set(0)
    barreProgression=Scale(menuBas,showvalue=0,length=500,sliderlength=10, from_=0, to=100,variable=progressionBarre, orient='horizontal', command=lambda prog=progressionBarre.get(): setProgression(prog))
    barreProgression.pack(side='top', fill='x')
    
    Continue = False
    
def demarrage():
    global fenetre, Continue, son, progression, musicPosFront
    # obtention des dernières sorties à partir de l'api monstercat
    
    pb.start(1)
    releases=monstercat_api.get_releases()
    # création d'une liste de sorties
    sorties=[]
    for sortie in releases["Releases"]["Data"]:
        if sortie["Streamable"] == True and len(sorties)<9:
            audioPath, imagePath = monstercat_api.get_track(sortie["CatalogId"],"chansons","images")
            sorties.append((sortie["CatalogId"],audioPath, imagePath))
            try:
                pb.step(10)
                chargement.update_idletasks()
            except:
                pass
    chargement.destroy()
    
    print (sorties)
    #sorties[n] = (CatalogId, AudioPath, CoverPath)

    mixer.init()
###################### Programme principal #############################
    fenetre=Tk()
    #photo=PhotoImage(file="images/1.png")
    #largeur,hauteur=taille_photo(photo)
    fenetre.geometry("1000x1000")
    fenetre.title("JUKE BOX")
    #fond=Label(fenetre, image=photo)
    #fond.grid(row=0, column=0, rowspan=9, columnspan=10)
    Continue=False
    son=''
    progression=IntVar()
    progression.set(0)
    musicPosFront=(0,0)
    images=liste_image(sorties)
    menu(fenetre, images, sorties)
    fenetre.mainloop()
########################################################################
if __name__ == "__main__":
    chargement=Tk()
    chargement.geometry("300x80")
    chargement.title("Chargement du Jukebox")
    lbl=Label(chargement, text="Téléchargement des derniers titres...")
    lbl.pack(side=TOP,pady=10)
    pb=ttk.Progressbar(chargement, orient=HORIZONTAL, length=260, mode='determinate')
    pb.pack(side=TOP,padx=20)
    chargement.after(100, demarrage)
    chargement.mainloop()