import os
import pandas as pd
import spacy_stanza
from openpyxl.utils import get_column_letter

nlp = spacy_stanza.load_pipeline("tr")

def extract_anamnesis_info(text_file):
    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    doc = nlp(text)

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

    category_data = {category: {col: None for col in cols} for category, cols in categories.items()}

    for ent in doc.ents:
        for category, cols in categories.items():
            for col in cols:
                if ent.label_ == col:
                    category_data[category][col] = ent.text

    return category_data
