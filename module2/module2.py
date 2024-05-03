#TO-DO:
# Doccano ile labeling
# nlp = spacy.load("tr_core_news_md") kodunda hata
# temel sıkıntı pandas ve C++ 14.0 ve üzeri olmaması. Kurulumu yap.

import spacy
import pandas as pd
import spacy_stanza
from openpyxl.utils import get_column_letter

nlp = spacy.load("tr_core_news_md")

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
    category_data = {category: {col: None for col in cols} for category, cols in categories.items()}

    # Extract entities based on predefined categories
    for ent in doc.ents:
        for category, cols in categories.items():
            for col in cols:
                if ent.label_ == col:
                    category_data[category][col] = ent.text

    return category_data

# Example usage:
text_file = "../dataset/dataset_module2/input_text3.txt"
anamnesis_data = extract_anamnesis_info(text_file)

# Save each category's data into separate sheets in an Excel file
output_excel_file = "anamnesis_data.xlsx"

with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for category, data in anamnesis_data.items():
        df = pd.DataFrame([data])  # Convert category data to DataFrame
        df.to_excel(writer, sheet_name=category, index=False)
        
        # Adjust column width based on text length
        for col in df.columns:
            column = df[col]
            max_length = max(column.astype(str).map(len).max(), len(col))
            adjusted_width = (max_length + 2) * 1.2
            writer.sheets[category].column_dimensions[get_column_letter(column.index[0] + 1)].width = adjusted_width

print(f"Anamnesis information saved to {output_excel_file}")
