from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import re

def download_and_cut_video(video_url, new_filename, segment_duration=90, max_segments=10):
    try:
        # Télécharger la vidéo
        yt = YouTube(video_url)
        best_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if best_stream:
            print(f"Téléchargement de la vidéo '{yt.title}' en cours...")
            best_stream.download()
            print(f"La vidéo '{yt.title}' a été téléchargée avec succès !")

            # Renommer la vidéo
            file_extension = best_stream.mime_type.split("/")[-1]
            cleaned_title = re.sub(r'[\/:*\'$?"#<>.,|]', '', yt.title)
            old_file_path = os.path.abspath(cleaned_title + f".{file_extension}")
            new_file_path = os.path.abspath(os.path.join(os.path.dirname(old_file_path), f"{new_filename}.{file_extension}"))
            os.rename(old_file_path, new_file_path)
            print(f"La vidéo a été renommée en '{new_file_path}'.")
        else:
            print("Aucun flux vidéo disponible sur l'URL.")
            return

        # Découper la vidéo
        video_path = new_file_path
        output_folder = new_filename
        os.makedirs(output_folder, exist_ok=True)

        video_clip = VideoFileClip(video_path)
        num_segments = min(int(video_clip.duration // segment_duration) + 1, max_segments)
        for i in range(num_segments):
            segment_start_time = i * segment_duration
            segment_end_time = min((i + 1) * segment_duration, video_clip.duration)
            output_file = os.path.join(output_folder, f"segment_{i + 1}.mp4")
            video_clip.subclip(segment_start_time, segment_end_time).write_videofile(output_file, codec="libx264", audio_codec="aac")
        
        print(f"{num_segments} segments ont été créés et enregistrés dans le dossier '{output_folder}'.")
        video_clip.close()  # Fermer la vidéo principale

        try:
            os.remove(video_path)
            print(f"La vidéo principale '{video_path}' a été supprimée.")
        except OSError as e:
            print(f"Erreur lors de la suppression de la vidéo principale : {e}")

        return new_file_path

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None

def get_video_url_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Lire la première ligne du fichier (l'URL)
            video_url = file.readline().strip()
        return video_url
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return None

def delete_url_from_file(file_path, url):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                if line.strip() != url:
                    file.write(line)

        print(f"L'URL '{url}' a été supprimée du fichier.")
    except Exception as e:
        print(f"Erreur lors de la suppression de l'URL du fichier : {e}")

# Lire l'URL depuis le fichier
file_path = 'lien_video.txt'
video_url_from_file = get_video_url_from_file(file_path)

if video_url_from_file:
    new_filename = 'video_test_from_file'
    downloaded_video_path = download_and_cut_video(video_url_from_file, new_filename)
    
    if downloaded_video_path:
        delete_url_from_file(file_path, video_url_from_file)
else:
    print("Aucune URL n'a pu être extraite du fichier.")
