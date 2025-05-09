# -*- coding: utf-8 -*-
import os
from moviepy import VideoFileClip, concatenate_videoclips

dossierDeStockage = "D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/AssemblageVideoDepart/"
dossier_videosPersonnalise = dossierDeStockage+"MiddlePersonnalise/"

try:
    # Charger les deux fichiers vidéo MP4
    clip1 = VideoFileClip("D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/AssemblageVideoDepart/ProgrammePythonAutomatisation/video1.mp4")
    clip3 = VideoFileClip("D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/AssemblageVideoDepart/ProgrammePythonAutomatisation/video3.mp4")

    # Vérifier si le dossier existe
    if os.path.exists(dossier_videosPersonnalise):
        fichiers_videos = os.listdir(dossier_videosPersonnalise)
    
        # Filtrer les fichiers MP4
        fichiers_mp4 = [fichier for fichier in fichiers_videos if fichier.endswith(".mp4")]
    
        # Afficher le nombre de fichiers MP4
        print(f"Nombre de fichiers MP4 dans le dossier : {len(fichiers_mp4)}")
    else:
        print(f"Le dossier specifie nexiste pas : {dossier_videosPersonnalise}")
    
   # Liste des fichiers vidéo dans le dossier `MiddlePersonnalise`
    for fichier in os.listdir(dossier_videosPersonnalise):

        nom_sortie = f"bodycam_{fichier}"
        chemin_sortie = os.path.join("D:/Documents/IncroyableThriller/SessionMars0224/VideoDuDebut/", nom_sortie)
        
        # Si c'est une vidéo MP4
        if fichier.endswith(".mp4") and not os.path.exists(chemin_sortie):
            # Charger la vidéo personnalisée (clip à changer)
            clip2 = VideoFileClip(os.path.join(dossier_videosPersonnalise, fichier))
            
            # Concaténer clip1, clip2 et clip3
            final_clip = concatenate_videoclips([clip1, clip2, clip3])
                        
            # Sauvegarder la vidéo concaténée
            final_clip.write_videofile(chemin_sortie, codec="libx264", bitrate="800k", audio_codec="aac")
    
    print("Toutes les videos ont ete traitees avec succes.")
    
except Exception as e:
    print(f"Une erreur s'est produite : {e}")