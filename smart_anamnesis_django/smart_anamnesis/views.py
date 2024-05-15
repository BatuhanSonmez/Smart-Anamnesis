from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import speech_recognition as sr
import spacy_stanza
import pandas as pd
from openpyxl.utils import get_column_letter
import jsonlines

# View for Module 1 - Continuous Speech Recognition
def module1_view(request):
    return render(request, 'module1.html')

def start_listening(request):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    transcription = ""

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=60)
        try:
            transcription = recognizer.recognize_google(audio, language="tr-TR")
        except sr.UnknownValueError:
            transcription = "Sorry, I did not understand that."
        except sr.RequestError:
            transcription = "Sorry, the service is down."
    
    return JsonResponse({'transcription': transcription})

# View for Module 2 - Text Processing and Saving to Excel
def module2_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        labels = request.POST.get('labels')

        # For demonstration purposes, here’s a simplified version of the processing logic:
        nlp = spacy_stanza.load_pipeline("tr", verbose=False)
        doc = nlp(text)

        data = []
        for ent in doc.ents:
            data.append([ent.text, ent.start_char, ent.end_char, ent.label_])

        # Create a DataFrame and save to Excel
        df = pd.DataFrame(data, columns=["Text", "Start", "End", "Label"])
        excel_path = "output.xlsx"
        df.to_excel(excel_path, index=False)

        return HttpResponse(f"Processed successfully! Data saved to {excel_path}")

    return render(request, 'module2.html')

# View for Module 3 - Generate Smart Summary from Excel
def module3_view(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        
        def generate_smart_summary(data_path):
            xls = pd.ExcelFile(data_path)
            summary = ""
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name)
                if not df.empty:
                    sheet_info = df.iloc[0].to_dict()
            sheet_summary = ""
            if sheet_name == "Hasta Bilgisi":
                sheet_summary = (
                    f"Hasta No: {sheet_info['Hasta No']}\n"
                    f"Hasta Adı: {sheet_info['Hasta Adı']}\n"
                    f"Hasta, {sheet_info['Yaşı']} yaşında bir "
                    f"{sheet_info['Cinsiyeti']}. "
                    f"Eğitim durumu, {sheet_info['Eğitim Durumu']} olup, "
                    f"mesleği {sheet_info['İşi']}. "
                    f"{sheet_info['Aile Öyküsü']}. "
                    f"{sheet_info['Kilosu']} "
                    f"ve boyu {sheet_info['Boyu']}'dir."
                )
            elif sheet_name == "Komorbid Durumlar":
                sheet_summary = (
                    f"Eşlik eden bulguları, {sheet_info['Eşlik Eden Bulgular']}."
                )
            elif sheet_name == "Baş Ağrısı Bilgileri":
                sheet_summary = (
                    f"Hastanın ayda ağrılı geçirdiği gün sayısı {sheet_info['Ağrılı Gün sayısı']} "
                    f"ve bu ağrıların {sheet_info['Ağrıların Kaçı Şiddetli']} şiddetli. "
                    f"Şiddetli olanların şiddeti {sheet_info['Şiddetli Olanların Şiddeti']}. "
                    f"İlaç kullanıldığında {sheet_info['İlaç Kullanıldığında Ağrı Süresi']} sürmektedir. "
                    f"İlaç kullanılmadığında ise {sheet_info['İlaç Kullanılmadığında Ağrı Süresi']} sürmektedir. "
                    f"Ağrı genellikle {sheet_info['En Sık Karakteri']} karakterdedir "
                    f"ve {sheet_info['Kaç Yıldır Baş Ağrısı Var']} yıldır migreni vardır."
                )
            elif sheet_name == "Eşlik Eden Bulgular":
                sheet_summary = (
                    f"Hastanın ağrı esnasında fotofobi seviyesi {sheet_info['Fotofobi (Ağrı Esnasında)']}, "
                    f"fonofobi seviyesi {sheet_info['Fonofobi (Ağrı Esnasında)']}, "
                    f"osmofobi seviyesi {sheet_info['Osmofobi (Ağrı Esnasında)']}. "
                    f"Ağrı dışında fotofobi seviyesi {sheet_info['Fotofobi (Ağrı Dışında)']}, "
                    f"fonofobi seviyesi {sheet_info['Fonofobi (Ağrı Dışında)']}, "
                    f"osmofobi seviyesi {sheet_info['Osmofobi (Ağrı Dışında)']}. "
                    f"Hastanın bulantı seviyesi {sheet_info['Bulantı']}, "
                    f"kusma seviyesi {sheet_info['Kusma']}. "
                    f"Hastanın menstrüel ilişki durumu {sheet_info['Menstrüel İlişki']}. "
                    f"Migrene özgü analjezik kullanımı {sheet_info['Analjezik Kullanımı (Migrene Özgü)']}. "
                    f"Migrene özgü olmayan analjezik kullanımı {sheet_info['Analjezik Kullanımı (Migrene Özgü Değil)']}. "
                    f"Aylık analjezik tüketimi {sheet_info['Aylık Analjezik Tüketimi']}. "
                    f"Daha önce {sheet_info['Daha Önce Alınan Tedaviler']} tedavisi almış. "
                    f"Düzenli olarak {sheet_info['Düzenli Kullanılan İlaç']} ilacı kullanıyor. "
                    f"Ağrıyı tetikleyen faktörler {sheet_info['Ağrıyı Tetikleyici Faktörler']}."
                )
            elif sheet_name == "Tedavi ile İlgili Beklenti":
                sheet_summary = (
                    f"{sheet_info['Tedavim Tamamıyla Etkili Olacak']}."
                )
            elif sheet_name == "Aura Bilgisi":
                sheet_summary = (
                    f"Hastanın aurası {sheet_info['Aura']}, "
                    f"aura süresi {sheet_info['Aura Süresi']} "
                    f"ve aura aylık atak sayısı {sheet_info['Aura Aylık Atak Sayısı']}."
                )
            elif sheet_name == "Ölçekler":
                sheet_summary = (
                    f"Değerlendirme skorları arasında MIDAS {sheet_info['MIDAS']}, "
                    f"HIT {sheet_info['HIT']}, "
                    f"Beck Depresyon {sheet_info['Beck Depresyon']}, "
                    f"Beck Anksiyete {sheet_info['Beck Anksiyete']}, "
                    f"Allodini {sheet_info['Allodini']}, "
                    f"VKİ {sheet_info['Vücut Kitle İndeksi (VKİ)']} "
                    f"ve UPSIT-12 {sheet_info['UPSIS-12']}."
                )
            elif sheet_name == "Diğer":
                sheet_summary = (
                    f"Ayrıca, hastada {sheet_info['Diğer']} bulunmaktadır."
                )
            summary += sheet_summary + " "
            return summary.strip()

        summary = generate_smart_summary(file_path)
        return HttpResponse(summary)
    
    return render(request, 'module3.html')
