import pandas as pd

def generate_smart_summary(data_path):
    # Load data from Excel file
    xls = pd.ExcelFile(data_path)
    
    # Initialize an empty summary string
    summary = ""
    
    # Iterate over all sheets
    for sheet_name in xls.sheet_names:
        # Read data from the current sheet
        df = pd.read_excel(xls, sheet_name)
        
        # Check if there is data in the DataFrame
        if not df.empty:
            # Extract relevant information
            sheet_info = df.iloc[0].to_dict()
            
            # Generate summary for the current sheet
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
            # Append the summary for the current sheet to the overall summary
            summary += sheet_summary + " "
    
    return summary.strip()  # Remove leading/trailing whitespace

# Example usage
data_path = "../module2/patient_1_anamnesis_data.xlsx"

smart_summary = generate_smart_summary(data_path)
print(smart_summary)
