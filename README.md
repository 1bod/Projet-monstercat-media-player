# Monstercat Media Player

**Les trophées NSI**
**Édition 2022**

## Documentation

Installation:
Pour exécuter cette application sont requis [Python 3.10](https://www.python.org/downloads/) et ces bibliothèques:

- Tkinter ( intégré à Python )
- [pygame]( https://pypi.org/project/pygame/ )
- [PIL]( https://pypi.org/project/PIL/ ) peut être installé via [pillow]( https://pypi.org/project/Pillow/ )
- [requests]( https://pypi.org/project/requests/ )

Utilisation:
Au lancement de l’application, les 9 dernières sorties Monstercat sont automatiquement téléchargées. Pour lancer un titre, il suffit de cliquer sur sa couverture d’album. Pour lancer un titre aléatoire, il faut cliquer sur le bouton aléatoire . Pour lire un titre en boucle, il faut cliquer sur le bouton répéter . Pour mettre un titre en pause, il suffit d’appuyer sur le bouton play/pause et de répéter l’opération pour relancer la lecture.
Pour ajouter un titre, appuyez sur le bouton ajouter : la fenêtre de recherche s’ouvre. Pour ajouter un titre via la fenêtre de recherche, entrez le terme à rechercher dans la zone de texte, entrez le nombre de résultats maximum (définit le temps de traitement de la recherche et la taille du téléchargement) et enfin appuyez sur rechercher. Vous sont donc présentés les résultats de recherche dans lesquels vous pouvez choisir le titre à télécharger ou l’album à explorer. Si l’élément sélectionné est un titre, il sera téléchargé et l’application redémarrera automatiquement pour l’intégrer. Sinon si l’élément est un album, la fenêtre d’album s’ouvre. Dans la fenêtre d’album, les titres présents dans un album se rendent disponibles au téléchargement. Ici, comme pour un titre simple, lors de la sélection d’une musique, elle sera téléchargée et l’application redémarrera automatiquement pour l’intégrer.

Les images de couverture sont stockées dans le dossier images et les fichiers audio dans le fichier chansons. L’intégralité du code est écrit en Python. Le multithreading est utilisé lors du téléchargement et de la vérification initiale de la présence des titres au lancement de l’application ainsi que lors du téléchargement de la couverture des albums lors de la recherche.

Pour un fonctionnement optimal, il est recommandé un processeur multicoeurs et une connexion internet haut débit.

## DOSSIER DE CANDIDATURE PRÉSENTATION DU PROJET

### PRÉSENTATION GÉNÉRALE

Notre projet est un projet de jukebox, ce projet nous fut proposé par notre professeur de NSI, la consigne initiale était de créer une application permettant d'écouter plusieurs musiques présentes dans les fichiers. Ce qui nous a amené à créer dans un premier temps une interface graphique capable d'accueillir notre jukebox, pour un nombre indéfini et illimité de musique. Nous avons ensuite implémenté au fur et à mesure de nouvelles fonctionnalités comme la possibilité de régler le volume, de faire pause, de choisir un titre aléatoire etc…

Notre plus gros ajout est probablement l’utilisation d’une api: celle du label de musique Monstercat, qui nous permet d’avoir accès via une interface de recherche à toutes les musiques signées avec le label.

### ORGANISATION DU TRAVAIL

Equipe:

- Louis
- Maxence

Répartition du travail:

- Louis s'est occupé de l’interface graphique, de la gestion des fichiers et de résoudre les bugs.
- Maxence s’est occupé de l'implémentation de l’API de recherche de musique ainsi que de l’aspect lecture de la musique et de l’utilisation de multi-threading dans le but d'accélérer l’ouverture de l'application.

Pour l’organisation nous avons majoritairement travaillé via github pour centraliser le projet. Nous avons ensuite utilisé discord pour communiquer. Nous avions dans le cadre de nos cours de NSI en travaux pratiques l'occasion de se voir et de parler de l’orientation de notre travail.

### LES ÉTAPES DU PROJET

Le but à la base était de simplement ajouter une rotation quotidienne de musiques basée sur les sorties du label Monstercat. Ensuite nous est venue l’idée de permettre la recherche des titres. Le projet étant devenu assez conséquent, nous avons pris la décision d’ajouter les fonctionnalités habituellement présentes dans les logiciels de streaming musical comme le réglage du niveau sonore, la lecture aléatoire, la lecture en boucle et la fonctionnalité play/pause.

### FONCTIONNEMENT ET OPÉRATIONNALITÉ

La fenêtre de recherche est aboutie: il est possible de faire sa recherche sans soucis ( en prenant en compte les limitations du moteur de recherche de monstercat). La fenêtre principale manque d’une barre de progression. Nous avons tenté d'implémenter cette fonctionnalité mais notre solution posait des problèmes de performances comme des pauses dans la lecture d’un titre.

### OUVERTURE

Finalement, il devrait être possible d’utiliser l’api de Spotify pour accéder à une plus grande bibliothèque de titres et donc toucher une plus grande audience mais il faudrait donc lacher le module Tkinter avec tout ses défauts pour probablement le remplacer par une interface web, bien plus facile à naviguer et plus usuelle de nos jours.
L’application finale semble très convenable, si c'était à refaire, nous changerions l’interface graphique pour un modèle avec une expérience utilisateur plus ergonomique; il faudrait aussi trouver un autre moyen de faire sa recherche et surtout nous aurions cherché une alternative à Tkinter qui a posé beaucoup de problèmes tels que des éléments non fonctionnels sans renvoyer d’erreur, rendant l’application difficile à débugger dans certaines situations. Il doit aussi être possible de faire afficher des images au format webp plutôt que jpeg car l’API Monstercat propose [une taille presque dix fois réduite pour les images à ce format](https://bit.ly/connect-v2-docs-CDX).
