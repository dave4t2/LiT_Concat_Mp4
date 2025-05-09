# Objectif du projet :
Concatener 1 video fixe de début + 1 videos personnalisée + 1 video fixe de fin


# src/LiT_Concat_Video_Perso_Planque.py
Ce programme fait l'ensemble des étapes

# input/video1/ : repertoire pour mettre la video fixe de début video1.mp4
# input/video2/ : repertoire pour mettre les videos personnalisées 33612345678.mp4
# input/video3/ : repertoire pour mettre la video fixe de fin video3.mp4

La video finale se nomme bodycam_<nom_de_la_video_personnalisée>.mp4
33612345678.mp4 ==> bodycam_33612345678.mp4

# Paramètres pour concatener
Le programme utilise ffmpeg pour la concatenation
Il faut que les 3 videos aient le même encodage pour que ça marche bien

**************************************************
*                                                *
*  PLUS DE DETAILS ? ==> LIRE LE Readme_Aide.md  *
*                                                *
**************************************************