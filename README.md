# ESOTIM

See README_en.md for english version (TBA)

ESOTIM est un outil conçu dans le cadre du projet ArchiFiltre, une initiative d'Etalab et du programme Entrepreneur d'Intérêt Général.

Il identifie, parmi une arborescence de répertoires, les fichiers en doublons, et les liste dans un fichier .csv.

C'est un fork de l'outil DupeGuru, réalisé par hsoft https://github.com/hsoft/dupeguru. Nous avons gardé le moteur de détection des doublons, récupéré quelques éléments de structure et outils, tout cela recentré autour d'un usage simple et unique.

## Utilisation

### Haut niveau (Systèmes UNIX uniquement, plus lent)

1. Placez les répertoires à analyser dans le dossier Import.
2. En ligne de commande, exécutez run_ESOTIM.sh
3. Le programme construit et exécute une image Docker, qui exécute à son tour run.py. Les logs sont affichés dans le Terminal. La copie de fichiers peut prendre un moment.
4. Une fois que le programme a terminé, un fichier csv (son nom est indiqué dans les logs) est créé dans le dossier Doublons.

### Bas niveau (Toutes plate-formes, plus rapide)

1. Installez Python 3.5 ou plus récent
2. En ligne de commande, entrez :

python3 run.py <Répertoire à analyser> <Répertoire destination du CSV>

## Remarques
* Il est volontaire qu'ESOTIM ne propose pas pour l'instant la suppression des doublons.
