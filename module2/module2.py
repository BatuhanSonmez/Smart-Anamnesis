import spacy_stanza
import pandas as pd
from openpyxl.utils import get_column_letter
import jsonlines

nlp = spacy_stanza.load_pipeline("tr")

def extract_anamnesis_info(text, labels):
    doc = nlp(text)

    categories = {
        "Hasta Bilgisi": ["Hasta No", "Hasta Adı", "Yaşı", "Eğitim Durumu", "İşi", "Aile Öyküsü", "Kilosu", "Boyu", "Cinsiyeti"],
        "Komorbid Durumlar": ["Eşlik Eden Bulgular"],
        "Baş Ağrısı Bilgileri": ["Ağrılı Gün sayısı", "Ağrı Şiddeti", "İlaç Kullanıldığında Ağrı Süresi", "İlaç Kullanılmadığında Ağrı Süresi", "Şiddetli Olanların Şiddeti",
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

    category_data = {category: {col: None for col in cols} for category, cols in categories.items()}

    for start, end, label in labels:
        label_text = text[start:end]
        for category, cols in categories.items():
            if label in cols:
                category_data[category][label] = label_text

    return category_data

def process_patient(patient):
    patient_id = patient['id']
    patient_text = patient['text']
    patient_labels = patient['label']

    anamnesis_data = extract_anamnesis_info(patient_text, patient_labels)

    output_excel_file = f"patient_{patient_id}_anamnesis_data.xlsx"

    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        for category, data in anamnesis_data.items():
            df = pd.DataFrame([data])
            df.to_excel(writer, sheet_name=category, index=False)
            
            for col in df.columns:
                column = df[col]
                max_length = max(column.astype(str).map(len).max(), len(col))
                adjusted_width = (max_length + 2) * 1.2
                writer.sheets[category].column_dimensions[get_column_letter(column.index[0] + 1)].width = adjusted_width

    print(f"Anamnesis information for patient {patient_id} saved to {output_excel_file}")

# Path to the JSONL file
jsonl_file = "all.jsonl"

# Process each patient in the JSONL file
with jsonlines.open(jsonl_file) as reader:
    for patient in reader:
        process_patient(patient)
