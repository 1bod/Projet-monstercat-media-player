"""Module récupérant des informations à partir de l'API monstercat"""

import os
import shutil
import requests

def search(query:str, limit) -> dict:
    """Recherche d'un terme dans la bibliothèque monstercat via l'API monstercat avec une limite de résultats"""
    res= requests.get("https://www.monstercat.com/api/catalog/browse?search={}&limit={}".format(query,limit))
    return res.json()["Data"]

def save(data, path:str, force=False):
    """Enregistre des données sous un emplacement"""
    file_exists=False
    for _, _, files in os.walk('/'.join(path.split("/")[:-1])+'/'):
        if path.split("/")[-1] in files:
            file_exists=True
    #si le fichier existe déja, on ne le télécharge pas
    if (not file_exists) or force:
        #stockage du fichier
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(data.raw, out_file)
    del data
        
def get_cover(catalog_id:str, image_path:str) -> str:
    """Récupère la couverture d'un titre à partir de l'api monstercat et l'enregistre dans l'emplacement spécifié"""
    cover=requests.get("https://www.monstercat.com/release/{}/cover".format(catalog_id), stream=True)
    if not image_path.endswith("/"):
        image_path+="/"
    res=requests.get("https://www.monstercat.com/api/catalog/release/{}".format(catalog_id)).json()
    title=res["Release"]["Title"].replace("/", " ").replace("\\", " ").replace("?", " ").replace("*", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ") # nettoyage du nom du titre pour pouvoir l'enregistrer
    save(cover, image_path+title+".jpeg")
    print("Image {}.jpeg téléchargée".format(title))
    return '{}{}.jpeg'.format(image_path,title)

def get_track(
    catalog_id:str,
    audio_path:str,
    image_path:str
) -> tuple[str,str]:
    """Fonction qui télécharge un titre si il n'est pas déja présent dans le dossier passé en paramètre"""
    res= requests.get("https://www.monstercat.com/api/catalog/release/{}".format(catalog_id)).json()
    title=res["Release"]["Title"].replace("/", " ").replace("\\", " ").replace("?", " ").replace("*", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ") # nettoyage du nom du titre pour pouvoir l'enregistrer
    
    if not audio_path.endswith("/"):
        audio_path+="/"
    if not image_path.endswith("/"):
        image_path+="/"
    
    #récupération de la couverture du titre
    cover=requests.get("https://www.monstercat.com/release/{}/cover".format(catalog_id), stream=True)
    #stockage de l'image
    save(cover, image_path+title+".jpeg")
    print("Image {}.jpeg téléchargée".format(title))
    
    #même chose pour le fichier son
    #récupération du titre
    titre=requests.get("https://www.monstercat.com/api/release/{}/track-stream/{}".format(res["Release"]["Id"],res["Tracks"][0]["Id"]), stream=True)
    #stockage du fichier
    save(titre, audio_path+title+".mp3")
    print("Titre {}.mp3 téléchargé".format(title))
    return '{}{}.mp3'.format(audio_path,title), '{}{}.jpeg'.format(image_path,title)

def get_releases() -> dict:
    """Fonction qui renvoie un dictionnaire des dernières sorties disponibles sur l'api Monstercat"""
    res = requests.get("https://www.monstercat.com/api/releases")
    return res.json()