"""Module récupérant des informations à partir de l'API monstercat"""

import os
import shutil
import requests

def search(query:str, limit) -> dict:
    """Recherche d'un terme dans la bibliothèque monstercat via l'API monstercat avec une limite de résultats"""
    try:
        res= requests.get("https://www.monstercat.com/api/catalog/browse?search={}&limit={}".format(query,limit))
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
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
        
def get_cover(catalog_id:str, image_path:str, results=[]) -> str:
    """Récupère la couverture d'un titre à partir de l'api monstercat et l'enregistre dans l'emplacement spécifié"""
    try:
        cover=requests.get("https://www.monstercat.com/release/{}/cover".format(catalog_id), stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    if not image_path.endswith("/"):
        image_path+="/"
    try:
        res=requests.get("https://www.monstercat.com/api/catalog/release/{}".format(catalog_id)).json()
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    title=res["Release"]["Title"].replace("/", " ").replace("\\", " ").replace("?", " ").replace("*", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ") # nettoyage du nom du titre pour pouvoir l'enregistrer
    save(cover, image_path+title+".jpeg")
    print("Image {}.jpeg téléchargée".format(title))
    results.append('{}{}.jpeg'.format(image_path,title))
    return '{}{}.jpeg'.format(image_path,title)

def get_track(
    catalog_id:str,
    audio_path:str,
    image_path:str, 
    results=[]
) -> tuple[str,str]:
    """Fonction qui télécharge le premier titre lié à l'identifiant de sortie s'il n'est pas déja présent dans le dossier passé en paramètre"""
    try:
        res= requests.get("https://www.monstercat.com/api/catalog/release/{}".format(catalog_id)).json()
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    title=res["Release"]["Title"].replace("/", " ").replace("\\", " ").replace("?", " ").replace("*", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ") # nettoyage du nom du titre pour pouvoir l'enregistrer
    
    if not audio_path.endswith("/"):
        audio_path+="/"
    if not image_path.endswith("/"):
        image_path+="/"
    
    #récupération de la couverture du titre
    try:
        cover=requests.get("https://www.monstercat.com/release/{}/cover".format(catalog_id), stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    #stockage de l'image
    save(cover, image_path+title+".jpeg")
    print("Image {}.jpeg téléchargée".format(title))
    
    #même chose pour le fichier son
    #récupération du titre
    try:
        titre=requests.get("https://www.monstercat.com/api/release/{}/track-stream/{}".format(res["Release"]["Id"],res["Tracks"][0]["Id"]), stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    #stockage du fichier
    save(titre, audio_path+title+".mp3")
    print("Titre {}.mp3 téléchargé".format(title))
    results.append(('{}{}.mp3'.format(audio_path,title), '{}{}.jpeg'.format(image_path,title)))
    return '{}{}.mp3'.format(audio_path,title), '{}{}.jpeg'.format(image_path,title)

def get_unique_track(catalog_id:str, release_id:str, track_id:str,image_path:str, audio_path:str, title:str) -> str:
    if not audio_path.endswith("/"):
        audio_path+="/"
    if not image_path.endswith("/"):
        image_path+="/"
    try:
        cover=requests.get("https://www.monstercat.com/release/{}/cover".format(catalog_id), stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    #stockage de l'image
    save(cover, image_path+title+".jpeg")
    print("Image {}.jpeg téléchargée".format(title))
    
    try:
        titre=requests.get("https://player.monstercat.app/api/release/{}/track-stream/{}".format(track_id,release_id), stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    save(titre, audio_path+title+".mp3")
    print("Titre {}.mp3 téléchargé".format(title))
    

def get_release(catalog_id:str, results=[]) -> list:
    """
    Fonction qui récupère toutes les informations liés à une sortie
    """
    try:
        res = requests.get("https://www.monstercat.com/api/catalog/release/{}".format(catalog_id)).json()
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    results.append(res)
    return res
    

def get_releases() -> dict:
    """Fonction qui renvoie un dictionnaire des dernières sorties disponibles sur l'api Monstercat"""
    try:
        res = requests.get("https://www.monstercat.com/api/releases")
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    return res.json()