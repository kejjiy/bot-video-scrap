import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

user_data_dir = 'C:\\Users\\kingd\\AppData\\Local\\Google\\Chrome\\User Data\\'

chrome_driver_path = ChromeDriverManager().install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.tiktok.com/fr/")

def inscription(driver):
    try:
        # Faire défiler la page vers le bas pour rendre le bouton de connexion visible
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Attendre que le bouton connexion soit visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app-header"]/div/div[3]/div[1]/a/div/span')))
        
        # Clic sur le bouton connexion
        driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[3]/div[1]/a/div/span').click()
        print("Clic sur le bouton Téléverser réussi.")
        
        # Attendre que l'élément d'entrée de type fichier soit visible
        file_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div/div/div/div/div[4]'))).click()
        
        # Chemin du fichier que vous souhaitez téléverser
        file_path = '/partie_1.mp4'
        
        # Envoyer le chemin du fichier à l'élément input
        file_input.send_keys(file_path)
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton Téléverser : {e}")

# Appeler la fonction inscription après le chargement de la page
inscription(driver)

# Ajouter une pause pour empêcher la fermeture immédiate de la page
time.sleep(10)  # Vous pouvez ajuster le nombre de secondes en conséquence

# Ne pas oublier de quitter le navigateur à la fin
driver.quit()


#//*[@id="root"]/div/div/div/div/div/div/div/div
