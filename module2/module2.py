#TO-DO:
#1- NLP (Natural Language Processing) nasıl yapılır? Bunun araştırması yapılacak.
#2- NER (Named Entity Recognition) - Labeling nasıl yapaılır? Araştırılacak. 
#3- Hangi Python kütüphanesi NER - Labeling için kullanılacak? -> Doccano

import spacy_stanza

# Load spaCy with the Turkish model from spacy-stanza
nlp = spacy_stanza.load_pipeline("tr")

def extract_anamnesis_info(text_file):
    # Read the text file
    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Process the text using the loaded spaCy pipeline
    doc = nlp(text)

    # Define anamnesis categories (modify as needed)
    categories = ["Belirtiler", "Tıbbi Geçmiş", "İlaçlar"]

    # Dictionary to store extracted information
    anamnesis_info = {category: [] for category in categories}

    # Extract entities based on predefined categories
    for ent in doc.ents:
        if ent.label_ in categories:
            anamnesis_info[ent.label_].append(ent.text)

    return anamnesis_info

# Example usage:
text_file = "../dataset/dataset_module2/anamnez_batuhan.txt"
anamnesis_data = extract_anamnesis_info(text_file)
print("Anamnesis Bilgileri:")
for category, values in anamnesis_data.items():
    print(category + ":")
    for value in values:
        print("- " + value)
