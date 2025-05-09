# 📘 Documentation : `LiT_Concat_Video_Perso_Planque.py`

## 1. Introduction

### 🎯 **Objectif**

Ce script automatise la **concaténation de trois segments vidéo MP4** en un seul fichier :

* `video1.mp4` – une introduction de 5 minutes, toujours identique.
* Une **vidéo personnalisée** `video2.mp4` (~20 secondes), unique pour chaque fichier.
* `video3.mp4` – une courte conclusion de 20 secondes, basée sur le même clip de base avec de petites modifications visuelles par personne.

Il est conçu pour **traiter efficacement des milliers de trios** avec :

* Pas de ré-encodage (préservation de la qualité originale).
* Performance rapide grâce à FFmpeg et au format `.ts`.
* Journalisation pour la traçabilité.

---

### ⚙️ **Comment ça fonctionne (Vue d'ensemble)**

1. Vérifie la présence des répertoires et des composants vidéo attendus.
2. Chaque fichier MP4 est **converti au format MPEG-TS**, qui est adapté au streaming et sûr pour la concaténation.
3. Les fichiers `.ts` résultants sont listés dans un fichier temporaire et **concaténés à l'aide de FFmpeg**.
4. Le fichier final `.mp4` est enregistré dans le répertoire de sortie.
5. Les fichiers temporaires sont supprimés.

---

## 2. Exigences pour les fichiers d'entrée

Pour que le script fonctionne de manière fiable sans ré-encodage, **les vidéos d'entrée doivent respecter des contraintes d'encodage strictes**.

### ✅ **Contraintes d'encodage obligatoires**

Les 3 vidéos d'entrée doivent :

* Être encodées avec :

  * **Codec vidéo** : `H.264 / AVC` (souvent affiché comme `avc1`)
  * **Codec audio** : `AAC`
* Avoir la **même résolution** : `720x1260` (portrait).
* Avoir le **même taux de trame** : `24 fps`.
* Avoir des **structures GOP compatibles**, idéalement :

  * Commencer et se terminer par des **I-frames** pour une concaténation sûre.
  * Éviter les **B-frames à la fin** des clips.

---

### 🔍 **Comment vérifier l'encodage (avec `ffprobe`)**

Pour inspecter l'encodage d'un fichier vidéo, exécutez :

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,codec_type,width,height,avg_frame_rate -of default=noprint_wrappers=1 input.mp4
```

Pour vérifier le codec audio :

```bash
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,codec_type -of default=noprint_wrappers=1 input.mp4
```

**Exemple de sortie attendue :**

```
codec_name=h264
codec_type=video
width=720
height=1260
avg_frame_rate=24/1
---
codec_name=aac
codec_type=audio
```

Vous pouvez également obtenir un aperçu complet en utilisant :

```bash
ffprobe -hide_banner -i input.mp4
```

Recherchez :

* `Stream #0:0` → vidéo : h264 (Main)
* `Stream #0:1` → audio : aac

---

### ❌ Que se passe-t-il si les contraintes ne sont pas respectées ?

Si les codecs, la résolution ou le taux de trame ne correspondent pas :

* FFmpeg peut **échouer silencieusement** ou **produire une sortie corrompue**.
* Les fichiers concaténés peuvent présenter des **artefacts**, des **images sautées** ou un **décalage audio**.

Pour corriger cela :

* Utilisez FFmpeg pour ré-encoder avec des paramètres alignés (nous pouvons fournir une commande si nécessaire).

---

## 3. Workflow étape par étape

### 🧩 Étape 1 : **Configuration et initialisation**

#### 🛠 Imports et journalisation

```python
import os, subprocess, logging
from datetime import datetime
```

* Les bibliothèques standard sont utilisées (aucune dépendance tierce).
* Un fichier journal horodaté est créé dans le répertoire `./logs/`.

```python
log_filename = f"./logs/concat_Launch_v2_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_Log.txt"
logging.basicConfig(...)
```

📌 **Pourquoi ?**

* Pour le débogage et les audits.
* Utile lors du traitement de grands lots pour identifier les fichiers échoués ou ignorés.

---

### 📁 Étape 2 : **Définir les chemins et valider la présence des fichiers**

```python
video1_path = './input/Video1/video1.mp4'
video2_path = './input/Video2/'
video3_path = './input/Video3/video3.mp4'
ConcatVideo_path = './output'
temp_folder = './temp'
```

* `video1` et `video3` sont réutilisés pour chaque trio.
* Le répertoire `video2` contient les clips personnalisés.

```python
if not os.path.exists(...) ...
```

🧪 **Pourquoi ?**

* Empêche le script de planter en cours d'exécution à cause de chemins d'entrée ou de sortie manquants.
* Assure un échec précoce avec des journaux clairs.

---

### 🔁 Étape 3 : **Boucler sur les MP4 personnalisés**

```python
video_files = os.listdir(video2_path)
mp4_files = [file for file in video_files if file.endswith(".mp4")]
```

* Récupère tous les fichiers MP4 personnalisés.
* Pour chacun, crée un fichier concaténé en sortie.

```python
if os.path.exists(output_path):
    continue
```

📌 **Pourquoi ?**

* Évite le traitement redondant des vidéos déjà générées.

---

### 🔄 Étape 4 : **Convertir les MP4 au format TS**

```python
def convert_to_ts(input_file, output_file):
    run_ffmpeg_command([
        "ffmpeg", "-i", input_file, "-c", "copy",
        "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", output_file, "-y"
    ])
```

📦 **Objectif de cette étape** :

* Convertit chaque MP4 en fichier `.ts` (MPEG-TS) sans ré-encodage.
* Ajoute les en-têtes Annex B nécessaires (`h264_mp4toannexb`) pour rendre les flux H.264 **sûrs pour la concaténation**.

💡 **Pourquoi TS ?**

* TS permet une concaténation basée sur les flux avec moins de problèmes de lecture.
* La structure MP4 (atomes moov, index) n'est pas naturellement adaptée à la concaténation.

---

### 📝 Étape 5 : **Créer une liste d'entrée FFmpeg pour la concaténation**

```python
with open(input_list_file, "w") as f:
    f.write(f"file '{ts1_path}'\n")
    f.write(f"file '{ts2_path}'\n")
    f.write(f"file '{ts3_path}'\n")
```

📌 **Pourquoi ?**

* FFmpeg attend un fichier texte avec les chemins d'entrée lors de l'utilisation de `-f concat`.
* Les chemins absolus sont utilisés pour éviter les problèmes de résolution de chemins relatifs.

---

### 🎬 Étape 6 : **Concaténer avec FFmpeg**

```python
run_ffmpeg_command([
    "ffmpeg", "-f", "concat", "-safe", "0", "-fflags", "+genpts",
    "-i", input_list_file, "-c", "copy", "-bsf:a", "aac_adtstoasc",
    "-y", output_path
])
```

🔍 **Explication** :

* `-f concat` : Indique à FFmpeg de lire une liste de fichiers d'entrée.
* `-safe 0` : Autorise les chemins de fichiers non sécurisés (comme les chemins absolus).
* `-fflags +genpts` : Régénère les horodatages pour une lecture plus fluide.
* `-c copy` : Pas de ré-encodage ; rapide et sans perte.
* `-bsf:a aac_adtstoasc` : Corrige le flux AAC pour le conteneur MP4.

📌 **Pourquoi cette séquence exacte ?**

* Cette combinaison garantit vitesse, compatibilité et lecture propre.

---

### 🧹 Étape 7 : **Nettoyer les fichiers temporaires**

```python
os.remove(ts1_path)
os.remove(ts2_path)
os.remove(ts3_path)
os.remove(input_list_file)
```

📌 **Pourquoi ?**

* Garde le répertoire `./temp` propre.
* Évite l'encombrement et les conflits futurs de lecture/écriture.

---

## ✅ 4. Résumé des pré-requis

| Exigence                      | Pourquoi c'est important                                |
| ----------------------------- | ------------------------------------------------------ |
| FFmpeg installé               | Toutes les opérations vidéo en dépendent.             |
| Format vidéo d'entrée : H.264/AAC | Nécessaire pour la compatibilité des fichiers `.ts`. |
| Résolution et fps identiques  | Évite les décalages audio/vidéo ou les erreurs de lecture. |
| Pas de B-frames à la fin des segments | Réduit les artefacts de décodage après concaténation. |
| Python 3.x                    | Exécute le script et gère les entrées/sorties et les journaux. |
| Structure des répertoires     | Les dossiers d'entrée/sortie attendus doivent exister au préalable. |

---

Souhaitez-vous que je continue avec les sections sur les limitations connues, les conseils de débogage et les améliorations futures ?

---

## ⚠️ 5. Limitations connues et cas particuliers

### ❗ 1. **Incompatibilité des entrées**

Si une vidéo d'entrée ne respecte **pas** les contraintes d'encodage (par exemple, résolution non correspondante, mauvais codec), FFmpeg :

* Peut échouer directement avec une erreur, ou
* Produire une sortie inutilisable ou défectueuse.

📌 **Recommandation** : Validez toujours les entrées avec `ffprobe`.

---

### ❗ 2. **Problèmes de frames cachées (par exemple, B-frames aux limites des segments)**

* Si un clip se termine par une **B-frame** ou ne commence pas par une **I-frame**, des artefacts de lecture peuvent apparaître après concaténation.
* Étant donné que le script ne fait **pas de ré-encodage**, il ne peut pas corriger cela à l'exécution.

📌 **Recommandation** : Assurez des structures GOP propres lors de la préparation des vidéos.

---

### ❗ 3. **Pas de parallélisation**

* Le script traite actuellement un fichier à la fois, ce qui peut être lent pour des milliers de fichiers.

📌 **Solution de contournement** : Vous pouvez exécuter manuellement le script dans plusieurs terminaux sur différents sous-ensembles de vidéos — ou des améliorations futures peuvent introduire la multiprocessus.

---

### ❗ 4. **Gestion des erreurs centralisée**

* Une erreur arrête tout le script (par exemple, si FFmpeg plante sur une mauvaise entrée).
* Les journaux sont disponibles pour le débogage, mais le lot continue uniquement si vous le redémarrez.

📌 **Recommandation** : Ajoutez des blocs try/except par itération si vous souhaitez continuer malgré les échecs.

---

## 🧪 6. Conseils de débogage et contrôle qualité

### 🧾 Vérifiez les informations de la vidéo de sortie

Pour inspecter l'encodage du fichier de sortie :

```bash
ffprobe -i ./output/bodycam_example.mp4
```

Assurez-vous :

* `codec_name=h264` pour la vidéo
* `codec_name=aac` pour l'audio
* `avg_frame_rate=24/1`
* Pas de frames perdues ou d'avertissements

---

### 🔍 Visualisez les fichiers TS intermédiaires

Si vous suspectez qu'un segment `.ts` est mal formé :

```bash
ffplay ./temp/intermediate_2.ts
```

Cela vous permet de déboguer si l'erreur provient du clip personnalisé ou de la logique de concaténation.

---

### 🪵 Lisez le journal

Chaque exécution du script génère un journal comme :

```
./logs/concat_Launch_v2_2025_05_09_14_35_12_Log.txt
```

Recherchez :

* `[INFO] Processing completed successfully`
* `[ERROR] FFmpeg command failed` avec une sortie stderr détaillée

---

### 🛠 Correction des mauvaises entrées

Pour ré-encoder une vidéo d'entrée défectueuse et forcer une structure correcte :

```bash
ffmpeg -i bad_input.mp4 -c:v libx264 -preset fast -crf 18 -g 24 -c:a aac -b:a 128k fixed_input.mp4
```

Cela garantit :

* H.264 + AAC
* Images clés toutes les secondes (`-g 24`)
* Flux audio compatible

---

## 🚀 7. Améliorations futures

### 🧵 1. Support de la multiprocessus

Utilisez `multiprocessing.Pool` de Python pour exécuter des lots en parallèle, particulièrement utile avec un stockage SSD et plusieurs cœurs.

### 🧪 2. Validateur d'entrée

Ajoutez un script ou un drapeau qui :

* Exécute `ffprobe` sur toutes les entrées
* Confirme la résolution, le taux de trame et les codecs avant la concaténation

---

## 📎 8. Annexe : Aide-mémoire CLI

| Tâche                          | Exemple de commande                                                   |
| ------------------------------ | ---------------------------------------------------------------------- |
| Inspecter l'encodage vidéo     | `ffprobe -hide_banner -i input.mp4`                                    |
| Lire un fichier .ts intermédiaire | `ffplay ./temp/intermediate_2.ts`                                      |
| Concaténer manuellement des fichiers .ts | `ffmpeg -f concat -i input_list.txt -c copy output.mp4`                |
| Ré-encoder pour compatibilité  | `ffmpeg -i input.mp4 -c:v libx264 -g 24 -c:a aac -b:a 128k output.mp4` |

---
