# -*- coding: utf-8 -*-
import os
from moviepy import VideoFileClip, concatenate_videoclips

dossierDeStockage = "D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/AssemblageVideoDepart/"
dossier_videosPersonnalise = dossierDeStockage+"MiddlePersonnalise/"

try:
    # Charger les deux fichiers vid�o MP4
    clip1 = VideoFileClip("D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/AssemblageVideoDepart/ProgrammePythonAutomatisation/Begin.mp4")
    clip3 = VideoFileClip("D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/AssemblageVideoDepart/ProgrammePythonAutomatisation/End.mp4")

    # V�rifier si le dossier existe
    if os.path.exists(dossier_videosPersonnalise):
        fichiers_videos = os.listdir(dossier_videosPersonnalise)
    
        # Filtrer les fichiers MP4
        fichiers_mp4 = [fichier for fichier in fichiers_videos if fichier.endswith(".mp4")]
    
        # Afficher le nombre de fichiers MP4
        print(f"Nombre de fichiers MP4 dans le dossier : {len(fichiers_mp4)}")
    else:
        print(f"Le dossier specifie nexiste pas : {dossier_videosPersonnalise}")
    
   # Liste des fichiers vid�o dans le dossier `MiddlePersonnalise`
    for fichier in os.listdir(dossier_videosPersonnalise):

        nom_sortie = f"bodycam_{fichier}"
        chemin_sortie = os.path.join("D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/", nom_sortie)
        
        # Si c'est une vid�o MP4
        if fichier.endswith(".mp4") and not os.path.exists(chemin_sortie):
            # Charger la vid�o personnalis�e (clip � changer)
            clip2 = VideoFileClip(os.path.join(dossier_videosPersonnalise, fichier))
            
            # Concat�ner clip1, clip2 et clip3
            final_clip = concatenate_videoclips([clip1, clip2, clip3])
                        
            # Sauvegarder la vid�o concat�n�e
            final_clip.write_videofile(chemin_sortie, codec="libx264", bitrate="800k", audio_codec="aac")
    
    print("Toutes les videos ont ete traitees avec succes.")
    
except Exception as e:
    print(f"Une erreur s'est produite : {e}")