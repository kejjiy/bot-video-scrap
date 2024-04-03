import re
import time
from pytube import YouTube
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def accept_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button'))).click()
    except:
        print("Le bouton Tout accepter n'a pas été trouvé ou n'est pas cliquable.")

def clean_title(title):
    cleaned_title = re.sub(r'[^\w\s]', '', title)
    return cleaned_title.strip()  # Supprimer les espaces inutiles
def get_latest_videos(channel_url, max_results=30):
    # Utilisation de Selenium pour charger dynamiquement la page
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(channel_url)

    try:
        # Accepter les cookies
        accept_cookies(driver)
        time.sleep(5)
        print("1")

        # Attendre que les éléments vidéo soient chargés
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a#video-title')))
        print("2")
        # Extraire les liens vidéo après que la page a été chargée
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_links = [a['href'] for a in soup.select('a#video-title')[:max_results]]

        with open('lien_video.txt', 'w', encoding='utf-8') as file:
            for video_link in video_links:
                video_url = 'https://www.youtube.com' + video_link
                try:
                    video = YouTube(video_url)
                    video_id = video.video_id
                    video_title = clean_title(video.title)  # Nettoyer le titre
                    # Vérifier si l'URL de la vidéo contient le mot "shorts"
                    if 'shorts' not in video_link:
                        file.write(f"{video_url}\n{video_title}\n")
                        print(f"Ajout de la vidéo : {video_title}")
                    else:
                        print(f"Ignorer la vidéo (shorts) : {video_title}")
                except Exception as e:
                    print(f"Erreur lors du traitement de la vidéo {video_url}: {e}")
    finally:
        # Fermer le navigateur après utilisation
        driver.quit()

if __name__ == "__main__": # Exécuter le script 
    channel_url = 'https://www.youtube.com/feed/trending'
    get_latest_videos(channel_url)
