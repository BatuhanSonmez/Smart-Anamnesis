import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the categories
categories = {
    "Hasta Bilgisi": ["Hasta No", "Hasta Adı", "Yaşı", "Eğitim Durumu", "İşi", "Aile Öyküsü", "Kilosu", "Boyu", "Cinsiyeti"],
    "Komorbid Durumlar": ["Eşlik Eden Bulgular"],
    "Baş Ağrısı Bilgileri": ["Ağrılı Gün sayısı", "Ağrıların Kaçı Şiddetli", "İlaç Kullanıldığında Ağrı Süresi", "İlaç Kullanılmadığında Ağrı Süresi", "Şiddetli Olanların Şiddeti",
                             "En Sık Karakteri", "Kaç Yıldır Baş Ağrısı Var"],
    "Eşlik Eden Bulgular": ["Fotofobi (Ağrı Esnasında)", "Fotofobi (Ağrı Dışında)", "Fonofobi (Ağrı Esnasında)",
                            "Fonofobi (Ağrı Dışında)", "Osmofobi (Ağrı Esnasında)", "Osmofobi (Ağrı Dışında)",
                            "Bulantı", "Kusma", "Menstrüel İlişki", "Analjezik Kullanımı (Migrene Özgü)", "Analjezik Kullanımı (Migrene Özgü Değil)",
                            "Aylık Analjezik Tüketimi", "Daha Önce Alınan Tedaviler", "Düzenli Kullanılan İlaç",
                            "Ağrıyı Tetikleyici Faktörler"],
    "Tedavi ile İlgili Beklenti": ["Tedavim Tamamıyla Etkili Olacak"],
    "Aura Bilgisi": ["Aura", "Aura Süresi", "Aura Aylık Atak Sayısı"],
    "Ölçekler": ["MIDAS", "HIT", "Beck Depresyon", "Beck Anksiyete", "Allodini", "Vücut Kitle İndeksi (VKİ)", "UPSIS-12"],
    "Diğer": ["Diğer"]
}

def extract_anamnesis_data(anamnesis_text):
    # Setup the WebDriver
    driver = webdriver.Firefox()

    try:
        # Open ChatGPT
        driver.get("https://chat.openai.com/")

        # Wait for the text area to be present
        wait = WebDriverWait(driver, 5)  # Increased wait time for robustness
        textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))

        # Compose the message
        message = f"Extract and classify the following anamnesis into categories in Turkish: {anamnesis_text}\n\n{categories}"

        # Send the message
        textarea.send_keys(message)
        textarea.send_keys(Keys.RETURN)

        # Allow some time for the response
        time.sleep(50)  # Increased sleep time to ensure the response is loaded

        # Wait for the latest response div
        response_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".agent-turn > div:nth-child(2) > div:nth-child(1)")))

        # Extract the text from the div
        classified_data = response_div.text

    except Exception as e:
        print(f"An error occurred: {e}")
        classified_data = "{}"
    finally:
        driver.quit()

    return classified_data

def parse_classified_data(classified_data):
    # Split the classified data into lines
    lines = classified_data.split('\n')

    # Initialize a dictionary to hold the parsed data
    parsed_data = {}

    # Loop through each line and parse the category and its corresponding information
    for line in lines:
        if ':' in line:  # Check if the line contains a colon
            category, info = line.split(':', 1)  # Split at the first colon
            parsed_data[category.strip()] = info.strip()  # Remove leading/trailing whitespaces

    return parsed_data


def save_to_excel(parsed_data, filename):
    # Convert parsed data into DataFrame
    df = pd.DataFrame(parsed_data.items(), columns=['Category', 'Information'])
    
    # Save DataFrame to Excel
    df.to_excel(filename, index=False)

def main():
    # Load the anamnesis text from a file
    with open('../module1/transcription.txt', 'r', encoding='utf-8') as file:
        anamnesis_text = file.read()

    # Extract and classify the anamnesis data using ChatGPT
    classified_data = extract_anamnesis_data(anamnesis_text)
    print("Classified Data:", classified_data)  # Print the classified data to the command prompt

    # Parse the classified data into tables
    parsed_data = parse_classified_data(classified_data)

    # Save the tables to an Excel file
    save_to_excel(parsed_data, 'anamnesis_tables.xlsx')

if __name__ == '__main__':
    main()
