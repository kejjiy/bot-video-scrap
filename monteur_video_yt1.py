from moviepy.editor import VideoFileClip, clips_array
import os

def read_and_remove_first_line(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Lire la première ligne
            nom_video = file.readline().strip()

            # Réécrire le fichier sans la première ligne
            remaining_lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(remaining_lines)

        # Retourner le nom de la vidéo
        return nom_video

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None

# Assume que nom_video est une variable contenant le nom de la vidéo
nom_video = read_and_remove_first_line('lien_video.txt')

gta_videos = ["/gta_1.mp4",
              "/gta_2.mp4",
              "/gta_3.mp4",
              "/gta_4.mp4",
              "/gta_5.mp4",
              "/gta_6.mp4",
              "/gta_7.mp4",
              "/gta_8.mp4",
              "/gta_9.mp4",
              "/gta_10.mp4"]

i = 1  # Initialiser le compteur pour le nom de fichier
j = 0  # Index pour parcourir les vidéos GTA
while True:  
    # Essayer de charger la vidéo c1 (segment différent à chaque itération)
    video_c1_path = f"/video_test_from_file/segment_{i}.mp4"
    if not os.path.exists(video_c1_path):
        break  # Arrêter la boucle s'il n'y a plus de segments à traiter

    try:
        # Charger la vidéo c1
        video_c1 = VideoFileClip(video_c1_path)
        
        # Redimensionner la vidéo c1 pour qu'elle fasse 607x1080
        video_c1 = video_c1.resize(width=1200)

        # Charger la vidéo GTA correspondante avec la durée spécifiée
        video_c2_path = gta_videos[j]
        video_c2 = VideoFileClip(video_c2_path).subclip(0, video_c1.duration)
        
    except Exception as e:
        print(f"Erreur lors du chargement de la vidéo c1 : {e}")
        break  # Arrêter la boucle s'il y a une erreur lors du chargement des vidéos

    # Créer une disposition l'un au-dessus de l'autre
    combine = clips_array([[video_c1], [video_c2]])

    # Créer un dossier avec le nom de la vidéo s'il n'existe pas déjà
    output_folder = f"/{nom_video}"
    os.makedirs(output_folder, exist_ok=True)

    # Écrire la vidéo dans un fichier différent pour chaque itération dans le dossier nom_video
    output_file_path = os.path.join(output_folder, f"partie_{i}.mp4")
    combine.write_videofile(output_file_path, codec="libx264", audio_codec="aac")

    # Fermer les vidéos
    video_c1.close()
    video_c2.close()

    # Supprimer la vidéo c1 après téléchargement
    try:
        os.remove(video_c1_path)
        print(f"La vidéo c1 '{video_c1_path}' a été supprimée.")
    except OSError as e:
        print(f"Erreur lors de la suppression de la vidéo c1 : {e}")

    # Incrémenter le compteur
    i += 1
    j = (j + 1) % len(gta_videos)  # Passer à la vidéo GTA suivante (modulo pour la répétition)
