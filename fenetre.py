"""
importation
"""


import tkinter as tk
from tkinter import ttk
import os
import random
from PIL import ImageTk, Image
from pygame import mixer
import monstercat_api
"""
Volé chez max
"""

class Musique():
    """Objet contenant les fonctions relatives à la musique"""
    def __init__(self):
        mixer.init()
        self.audio_path=""
    def jouer(self, audio_path):
        """Joue le fichier audio_path"""
        NOM_MUSIQUE_ACTUEL.set(audio_path[9:-4])
        self.audio_path=audio_path
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
    def set_progress(cls, progress:float):
        """Met à jour la progression de la musique en secondes"""
        mixer.music.set_pos(progress)
    @classmethod
    def set_volume(cls, volume):
        """Met à jour le volume de la musique"""
        mixer.music.set_volume(float(volume))
    @classmethod
    def get_busy(cls):
        """Retourne True si la musique est en cours de lecture, False sinon"""
        return mixer.music.get_busy()
    def get_length(self):
        """Retourne la durée de la musique en secondes"""
        return mixer.Sound(self.audio_path).get_length()

def open_research(window):
    """Ouvre une fenêtre de recherche de musique"""
    global FENETRE_RECHERCHE
    FENETRE_RECHERCHE=tk.Toplevel(window)
    FENETRE_RECHERCHE.title("Recherche de musique")
    FENETRE_RECHERCHE.geometry("1100x700")
    FENETRE_RECHERCHE.rowconfigure(0, weight=1)
    FENETRE_RECHERCHE.columnconfigure(0, weight=1)
    terme_recherche = tk.StringVar()
    terme_recherche.set("")
    cadre_recherche=tk.Frame(FENETRE_RECHERCHE)
    cadre_recherche.pack(side="top", padx=5, pady=5)
    label_terme_a_rechercher=tk.Label(cadre_recherche, text="Terme à rechercher : ")
    label_nombre_de_resultats=tk.Label(cadre_recherche, text="Nombre de tentatives : ")
    label_terme_a_rechercher.grid(row=0, column=0)
    label_nombre_de_resultats.grid(row=0, column=1)
    entree = ttk.Entry(cadre_recherche, textvariable=terme_recherche)
    entree.grid(row=1, column=0, padx=5, pady=5)
    nb_results=tk.IntVar()
    nb_results.set(10)
    entree_nb_results = ttk.Spinbox(cadre_recherche, from_=1, to=100, textvariable=nb_results)
    entree_nb_results.grid(row=1, column=1, padx=5, pady=5)
    button_recherche = ttk.Button(cadre_recherche, text="Rechercher", command=lambda: recherche(terme_recherche.get(), nb_results.get(), cadre_resultats, window))
    button_recherche.grid(row=1, column=2, padx=5, pady=5)
    canvas = tk.Canvas(FENETRE_RECHERCHE)
    cadre_resultats = tk.Frame(canvas)
    frame_scrollbar=tk.Frame(FENETRE_RECHERCHE)
    frame_scrollbar.pack(side="right", fill="y")
    defil_y = ttk.Scrollbar(frame_scrollbar, orient='vertical', command=canvas.yview)
    cadre_resultats.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.create_window((0,0),window=cadre_resultats,anchor="nw")
    #defil_y.config(command=canvas.yview)
    #canvas['yscrollcommand'] = defil_y.set
    canvas.configure(yscrollcommand=defil_y.set)
    canvas.pack(side='top', padx=5, pady=5, fill='both', expand=True)
    defil_y.pack(side='right', fill='y',)
    #defil_y.grid(row=0, column=5, sticky='ns')
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    FENETRE_RECHERCHE.bind_all("<MouseWheel>", on_mousewheel)

def recherche(terme, nb_results, cadre_resultats,window):
    """Recherche les musiques correspondant au terme dans le catalogue"""
    titres=[]
    titres_charges=[]
    # pas de logique de mettre une liste en global mais ça ne marche pas sinon
    global LISTE_IMAGE_RECHERCHE
    LISTE_IMAGE_RECHERCHE = []
    res=monstercat_api.search(terme, nb_results)
    for resultat in res:
        catalog_id=resultat["Release"]["CatalogId"]
        if resultat["Streamable"] is True and not catalog_id in titres_charges:
            #on récupère l'image
            img_path=monstercat_api.get_cover(catalog_id, "images/")
            #print("Image {}.jpeg téléchargée".format(catalog_id))
            img=ImageTk.PhotoImage(Image.open(img_path).resize((200,200)))
            titres.append((resultat["Release"]["Title"],img, catalog_id))
            titres_charges.append(catalog_id)
    i=0
    for titre in titres:
        #on crée un bouton pour chaque résultat dans une grille avec 5 colonnes
        #chaque bouton est contenu dans un cadre
        frame=tk.Frame(cadre_resultats)
        #print(i)
        print(titre)
        img=ImageTk.PhotoImage(Image.open(str("images/"+titre[0]+".jpeg")).resize((200,200), Image.ANTIALIAS))
        LISTE_IMAGE_RECHERCHE.append(img)
        bouton=ttk.Button(frame, image=LISTE_IMAGE_RECHERCHE[-1],compound = "top", command=lambda c=titre[2]: charger(c, window))
        bouton.pack(side="top")
        lbl=tk.Label(frame, text=titre[0])
        lbl.pack(side='bottom')
        #print("position : x={} y={}".format(i%5, i//5))
        frame.grid(row=i//5,column=i%5)
        i+=1
    input()
    FENETRE_RECHERCHE.update()



"""
NOUVEAU CODE
"""

def charger(cid, window):
    """Charge la musique correspondant au catalog_id"""
    destroy_window(window)
    print(cid)
    monstercat_api.get_track(cid, "chansons/", "images/")
    demarrage()


def construction_bouton(frame,image,texte,audiopath, jukebox):
    """Crée un bouton avec l'image et le texte"""
    button_musique = ttk.Button(frame, image=image, text= texte, command=lambda:jukebox.jouer(audiopath))
    return button_musique

def demarrage():
    """Fonction de démarrage de l'application"""
    global JUKEBOX
    JUKEBOX = Musique()

    liste_musique = os.listdir('chansons')


    window = tk.Tk()
    window.title("JukeBox")
    window.geometry("570x570")
    window.resizable(False,False)
    window.iconbitmap('images/icone.ico')

    global NOM_MUSIQUE_ACTUEL
    NOM_MUSIQUE_ACTUEL = tk.StringVar()
    container = ttk.Frame(window)
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame= ttk.Frame(canvas)

    sound_frame = tk.Frame(container)
    volume = tk.IntVar()
    volume.set(50)
    scrollbar_sound = ttk.Scale(sound_frame, orient="vertical", command=lambda vol=volume.get():JUKEBOX.set_volume(vol), variable=volume, from_=1.0, to=0.0, length=200)


    plus_image = ImageTk.PhotoImage(Image.open("images/plus.png").resize((45,45), Image.ANTIALIAS))
    bouton_plus = ttk.Button(sound_frame, command=lambda:open_research(window), image=plus_image)
    bouton_plus.pack(fill="both", side="top")


    scrollbar_sound.pack(padx=5, side="top")
    sound_frame.pack(side = "left", fill="y")

    scrollable_frame.bind(
        "<Configure>",
        lambda e:canvas.configure(
            scrollregion=canvas.bbox("all")
            )
        )
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    window.bind_all("<MouseWheel>", on_mousewheel)

    canvas.create_window((0,0),window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)




    les_images = []
    les_chansons = []
    compteur = 0
    for elt in liste_musique:
        if compteur == 0:
            frame = tk.Frame(scrollable_frame)
        compteur+=1
        print('images/'+elt[:-4]+".jpeg")
        image = ImageTk.PhotoImage(Image.open('images/'+elt[:-4]+".jpeg").resize((150,150), Image.ANTIALIAS))
        texte = elt[:-4]
        audiopath = 'chansons/'+elt
        les_images.append(image)
        les_chansons.append(audiopath)


        construction_bouton(frame,les_images[-1],texte,les_chansons[-1], JUKEBOX).pack(side="left", fill="both", expand=True)

        if compteur%3==0:
            frame.pack(fill="both")
            frame = tk.Frame(scrollable_frame)
    frame.pack()


    # Progression
    frame_barre = tk.Frame(window)
    under_barre = tk.Frame(frame_barre)
    upper_barre = tk.Frame(frame_barre)
    """
    depart = 0
    arrive = 1000
    timer_musique_affichage = tk.StringVar()
    longueur_musique_affichage = tk.StringVar()
    label_gauche = tk.Label(under_barre, textvariable=timer_musique_affichage)
    label_droite = tk.Label(under_barre, textvariable=longueur_musique_affichage)
    global variable_barre
    variable_barre=tk.IntVar()
    variable_barre.set(depart)
    barre = ttk.Scale(under_barre, orient='horizontal', from_=depart, to=arrive, length=350, variable=variable_barre, command=update_progress_from_user)"""
    again_image = ImageTk.PhotoImage(Image.open("images/again.png").resize((80,30), Image.ANTIALIAS))
    play_pause_image = ImageTk.PhotoImage(Image.open("images/play_pause.png").resize((80,30), Image.ANTIALIAS))
    aleatoire_image = ImageTk.PhotoImage(Image.open("images/aleatoire.png").resize((80,30), Image.ANTIALIAS))
    bouton_alea = ttk.Button(upper_barre,command=lambda:JUKEBOX.jouer(random.choice(les_chansons)), image= aleatoire_image)
    bouton_play_pause = ttk.Button(upper_barre, command=JUKEBOX.play_pause, image= play_pause_image)
    bouton_again = ttk.Button(upper_barre, command=lambda:JUKEBOX.set_progress(0), image=again_image)


    container.pack(fill="both", expand=True)
    canvas.pack(side="left",fill="both",expand=True)
    scrollbar.pack(side="right", fill="y")
    bouton_alea.pack(side="left", fill="both", expand=True)
    bouton_play_pause.pack(side="left", fill="both", expand=True)
    bouton_again.pack(side="left", fill="both", expand=True)
    """
    label_gauche.pack(side="left")
    barre.pack(fill="x", side="left",  pady=5)
    label_droite.pack(side="left")"""

    label_nom_musique = tk.Label(frame_barre, textvariable=NOM_MUSIQUE_ACTUEL,font=("Nunito", 20))


    upper_barre.pack(pady=15)
    label_nom_musique.pack()
    under_barre.pack()
    frame_barre.pack(fill="x")

    #image1 = tk.PhotoImage(file = "image1.png")
    #button_1 = tk.Button(window, image = image1)
    JUKEBOX.set_volume(0.25)
    volume.set(0.25)
    #window.after(100, progress_update)
    window.mainloop()
    """
    PROGRESSBAR NON FONCTIONNELLE
def update_progress_from_user(new_progress:float):
    global JUKEBOX, variable_barre
    #print(type(new_progress),new_progress, type(JUKEBOX.get_length()), JUKEBOX.get_length())
    new_progress=(float(new_progress)/1000)*JUKEBOX.get_length()
    JUKEBOX.set_progress(new_progress)
    variable_barre.set(new_progress)

def progress_update():
    global variable_barre
    if JUKEBOX.get_busy(): #si un titre est en cours de lecture
        variable_barre.set((JUKEBOX.get_progress()/JUKEBOX.get_length())*1000)
    t1=threading.Timer(1, progress_update)
    t1.start()"""

def destroy_window(window):
    """Destruction de la fenetre"""
    window.destroy()
