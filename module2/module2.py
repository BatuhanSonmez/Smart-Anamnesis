#TO-DO:
#1- NLP (Natural Language Processing) nasıl yapılır? Bunun araştırması yapılacak.
#2- NER (Named Entity Recognition) - Labeling nasıl yapaılır? Araştırılacak. 
#3- Hangi Python kütüphanesi NER - Labeling için kullanılacak? -> Doccano

import spacy
import pandas as pd
import spacy_stanza

# Load spaCy with the Turkish model from spacy-stanza
nlp = spacy_stanza.load_pipeline("tr")

def extract_anamnesis_info(text_file):
    # Read the text file
    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Process the text using the loaded spaCy pipeline
    doc = nlp(text)

    # Define medical anamnesis categories and their corresponding table columns
    categories = {
        "Hasta Bilgisi": ["Hasta No", "Hasta Adı", "Yaşı", "Eğitim Durumu", "İşi", "Aile Öyküsü", "Kilosu", "Boyu", "Cinsiyeti"],
        "Komorbid Durumlar": ["Eşlik Eden Bulgular"],
        "Baş Ağrısı Bilgileri": ["Ağrılı Gün sayısı", "Ağrı Şiddeti", "Ağrı Süresi", "Şiddetli Olanların Şiddeti",
                                 "En Sık Karakteri", "Kaç Yıldır Baş Ağrısı Var"],
        "Eşlik Eden Bulgular": ["Fotofobi (Ağrı Esnasında)", "Fotofobi (Ağrı Dışında)", "Fonofobi (Ağrı Esnasında)",
                                "Fonofobi (Ağrı Dışında)", "Osmofobi (Ağrı Esnasında)", "Osmofobi (Ağrı Dışında)",
                                "Bulantı", "Kusma", "Menstrüel İlişki", "Analjezik Kullanımı",
                                "Aylık Analjezik Tüketimi", "Daha Önce Alınan Tedaviler", "Düzenli Kullanılan İlaç",
                                "Ağrıyı Tetikleyici Faktörler"],
        "Tedavi ile İlgili Beklenti": ["Tedavim Tamamıyla Etkili Olacak"],
        "Aura Bilgisi": ["Aura", "Aura Süresi", "Aura Aylık Atak Sayısı"],
        "Ölçekler": ["MIDAS", "HIT", "Beck Depresyon", "Beck Anksiyete", "Allodini", "Vücut Kitle İndeksi (VKİ)", "UPSIS-12"]
    }

    # Dictionary to store extracted information for each category
    category_data = {}

    # Extract entities based on predefined categories
    for category, cols in categories.items():
        category_data[category] = {col: None for col in cols}

    for ent in doc.ents:
        for category, cols in categories.items():
            if ent.label_ in cols:
                category_data[category][ent.label_] = ent.text

    return category_data

# Example usage:
text_file = "../dataset/dataset_module2/input_text3.txt"
anamnesis_data = extract_anamnesis_info(text_file)

# Save each category's data into separate sheets in an Excel file
output_excel_file = "anamnesis_data.xlsx"

with pd.ExcelWriter(output_excel_file) as writer:
    for category, data in anamnesis_data.items():
        df = pd.DataFrame(data, index=[0])  # Convert category data to DataFrame
        df.to_excel(writer, sheet_name=category, index=False)

print(f"Anamnesis information saved to {output_excel_file}")
