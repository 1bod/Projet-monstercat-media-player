"""Module principal du Projet monstercat media player"""

#   Le module pygame est utilisé pour la lecture des musiques en format mp3
#   En effet, l'api monstercat ne founit pas les fichiers audio au format mp3
#   winsound.PlaySound ne fonctionne pas avec les fichiers mp3
#   Pour installer pygame, la commande à executer dans un terminal est: pip3 install pygame
#
#   Amélioration apportées:
#   - Les 9 musiques sont tirées des dernières sorties de l'api monstercat
#   - Possibilité de télécharger les musiques directement depuis l'api monstercat
#   - Refonte complète du code de base
#   - Refonte graphique
#   - Lecture aléatoire
#   - Lecture en boucle
#   - Réglage du volume
#   - Multithreading lors du chargment des musiques
#

from threading import Thread
import monstercat_api
import interface
import fenetre



def startup(objet_fenetre:interface.Chargement):
    """Fonction de démarrage du programme"""
    threads = []
    results= []
    releases=monstercat_api.get_releases()
    # création de la liste des sorties à afficher
    sorties=[] #sorties[] = (CatalogId, AudioPath, CoverPath)
    nombre_telecharge=0
    for sortie in releases["Releases"]["Data"]:
        if sortie["Streamable"] is True and nombre_telecharge<12:
            nombre_telecharge+=1
            thread = Thread(target=monstercat_api.get_track, args=(sortie["CatalogId"],"chansons","images", results))
            threads.append(thread)
            try:
                objet_fenetre.add_progress(10)
                objet_fenetre.update_idletasks()
            except: # pylint: disable=bare-except
                pass
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    for result in results:
        sorties.append((sortie["CatalogId"],result[0],result[1]))
    
    # audio_path, image_path = monstercat_api.get_track(sortie["CatalogId"],"chansons","images")
    #sorties.append((sortie["CatalogId"],audio_path, image_path))
    objet_fenetre.destroy()
    fenetre.demarrage()

if __name__ == "__main__":
    chargement=interface.Chargement("Téléchargement des derniers titres...", callback=startup)
    chargement.start()