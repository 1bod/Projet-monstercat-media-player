"""Module principal du Projet jukebox"""

#   Le module pygame est utilisé pour la lecture des musiques en format mp3
#   En effet, l'api monstercat ne founit pas les fichiers audio au format mp3
#   winsound.PlaySound ne fonctionne pas avec les fichiers mp3
#   Pour installer pygame, la commande à executer dans un terminal est: pip3 install pygame
#
#   Amélioration apportées:
#   - Les 9 musiques sont tirées des dernières sorties de l'api monstercat
#   - Possibilité de télécharger les musiques directement depuis l'api monstercat
#   - Refonte complète du code de base
#

import tkinter as tk
import tkinter.ttk as ttk
from pygame import mixer

from PIL import ImageTk, Image

import monstercat_api
import interface

class Musique():
    """Objet contenant les fonctions relatives à la musique"""
    def __init__(self):
        mixer.init()
    @classmethod
    def jouer(cls, audio_path):
        """Joue le fichier audio_path"""
        mixer.music.load(audio_path)
        mixer.music.play()
    @classmethod
    def play_pause(cls):
        """Joue ou met en pause la musique"""
        if mixer.music.get_busy():
            mixer.music.pause()
        else:
            mixer.music.unpause()
    @classmethod
    def stop(cls):
        """Arrête la musique"""
        mixer.music.stop()
    @classmethod
    def get_progress(cls) -> int:
        """Retourne la progression de la musique en secondes"""
        return mixer.music.get_pos() // 1000
    @classmethod
    def set_progress(cls, progress:int):
        """Met à jour la progression de la musique en secondes"""
        mixer.music.set_pos(progress)

def main_root(master):
    master.title("Jukebox")
    master.geometry("1000x1000")
    master.resizable(False, False)
    b=tk.Button(master, text="Quitter", command=master.destroy)
    b.pack(side='top')

def main_gui(root, fenetre, jukebox, sorties):
    """Fonction de l'interface graphique"""
    b2=tk.Button(fenetre, text="Quitter", command=root.destroy, bg="red")
    b2.grid(row=0, column=0, sticky="w")
    fenetre.columnconfigure(0, weight=1)
    fenetre.rowconfigure(0, weight=1)
    #master.iconbitmap("jukebox.ico")
    
    fenetre.pack(side="top", fill="both", expand=True)
    i=0
    for sortie in sorties:
        image=ImageTk.PhotoImage(Image.open(sortie[2]).resize((200,200)))
        button_sortie=tk.Button(fenetre, borderwidth=0, image=image, height=200, width=200, command=lambda sortie=sortie:jukebox.jouer(sortie[1]))
        button_sortie.grid(row=i//3, column=i%3, sticky="wn")
        i+=1
    root.update()
    
def startup(objet_fenetre:interface.Chargement):
    """Fonction de démarrage du programme"""
    releases=monstercat_api.get_releases()
    # création de la liste des sorties à afficher
    sorties=[] #sorties[] = (CatalogId, AudioPath, CoverPath)
    for sortie in releases["Releases"]["Data"]:
        if sortie["Streamable"] is True and len(sorties)<9:
            audio_path, image_path = monstercat_api.get_track(sortie["CatalogId"],"chansons","images")
            sorties.append((sortie["CatalogId"],audio_path, image_path))
            try:
                objet_fenetre.add_progress(10)
                objet_fenetre.update_idletasks()
            except: # pylint: disable=bare-except
                pass
    objet_fenetre.destroy()
    
    root=tk.Tk()
    main_root(root)
    jukebox = Musique()
    fenetre=tk.Frame(root, bg="black")
    main_gui(root,fenetre, jukebox, sorties)
    #fenetre.load_bibliotheque(sorties,jukebox)
    root.mainloop()

if __name__ == "__main__":
    chargement=interface.Chargement("Téléchargement des derniers titres...", callback=startup)
    chargement.start()
    
    