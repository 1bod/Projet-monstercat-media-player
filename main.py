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
#   - Refonte graphique
#   - Lecture aléatoire
#   - Lecture en boucle
#   - Réglage du volume
#

import monstercat_api
import interface
import fenetre

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

    fenetre.demarrage()

if __name__ == "__main__":
    chargement=interface.Chargement("Téléchargement des derniers titres...", callback=startup)
    chargement.start()
    
    