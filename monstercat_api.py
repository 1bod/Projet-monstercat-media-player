"""Module récupérant des informations à partir de l'API monstercat"""

import os
import shutil
import requests

def search(query:str, limit) -> dict:
    """Recherche d'un terme dans la bibliothèque monstercat via l'API monstercat avec une limite de résultats"""
    try:
        res= requests.get(f"https://www.monstercat.com/api/catalog/browse?search={query}&limit={limit}")
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

def get_cover(catalog_id:str, image_path:str, results=None) -> str:
    """Récupère la couverture d'un titre à partir de l'api monstercat et l'enregistre dans l'emplacement spécifié"""
    if results is None:
        results=[]
    try:
        cover=requests.get(f"https://www.monstercat.com/release/{catalog_id}/cover", stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    if not image_path.endswith("/"):
        image_path+="/"
    try:
        res=requests.get(f"https://www.monstercat.com/api/catalog/release/{catalog_id}").json()
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    title=res["Release"]["Title"].replace("/", " ").replace("\\", " ").replace("?", " ").replace("*", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ") # nettoyage du nom du titre pour pouvoir l'enregistrer
    save(cover, image_path+title+".jpeg")
    print(f"Image {title}.jpeg téléchargée")
    results.append(f'{image_path}{title}.jpeg')
    return f'{image_path}{title}.jpeg'

def get_track(
    catalog_id:str,
    audio_path:str,
    image_path:str,
    results=None
) -> tuple[str,str]:
    """Fonction qui télécharge le premier titre lié à l'identifiant de sortie s'il n'est pas déja présent dans le dossier passé en paramètre"""
    if results is None:
        results=[]
    try:
        res= requests.get(f"https://www.monstercat.com/api/catalog/release/{catalog_id}").json()
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
        cover=requests.get(f"https://www.monstercat.com/release/{catalog_id}/cover", stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    #stockage de l'image
    save(cover, image_path+title+".jpeg")
    print(f"Image {title}.jpeg téléchargée")

    #même chose pour le fichier son
    #récupération du titre
    try:
        titre=requests.get(f"https://www.monstercat.com/api/release/{res['Release']['Id']}/track-stream/{res['Tracks'][0]['Id']}", stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    #stockage du fichier
    save(titre, audio_path+title+".mp3")
    print(f"Titre {title}.mp3 téléchargé")
    results.append((f'{audio_path}{title}.mp3', f'{image_path}{title}.jpeg'))
    return f'{audio_path}{title}.mp3', f'{image_path}{title}.jpeg'

def get_unique_track(catalog_id:str, release_id:str, track_id:str,image_path:str, audio_path:str, title:str) -> str:
    """Fonction qui télécharge un titre unique à partir de son identifiant de sortie et de son identifiant de titre"""
    if not audio_path.endswith("/"):
        audio_path+="/"
    if not image_path.endswith("/"):
        image_path+="/"
    try:
        cover=requests.get(f"https://www.monstercat.com/release/{catalog_id}/cover", stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    #stockage de l'image
    save(cover, image_path+title+".jpeg")
    print(f"Image {title}.jpeg téléchargée")

    try:
        titre=requests.get(f"https://player.monstercat.app/api/release/{track_id}/track-stream/{release_id}", stream=True)
    except ConnectionError:
        print("Erreur de connexion: Aucun accès internet")
        raise ConnectionError from ConnectionError
    save(titre, audio_path+title+".mp3")
    print(f"Titre {title}.mp3 téléchargé")

def get_release(catalog_id:str, results=None) -> list:
    """
    Fonction qui récupère toutes les informations liés à une sortie
    """
    if results is None:
        results=[]
    try:
        res = requests.get(f"https://www.monstercat.com/api/catalog/release/{catalog_id}").json()
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
