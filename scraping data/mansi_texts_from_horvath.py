import nltk
import re
import pandas as pd


def get_sentences(text: str):
    data = []
    sentences = nltk.sent_tokenize(text.replace('\n', ''))
    #sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+', text)
    return pd.Series(sentences)

def extract_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    extracted_text = []
    
    for line in lines:
        # Ignore lines that look like a date or a name (adjust the conditions as needed)
        if not line.strip() or (line.strip().startswith('<') and line.strip().endswith('>')) or \
        len(line.strip()) < 22 or any(line.strip().startswith(prefix) for prefix in ['2013.', '2014.', \
        '2015.', '2016.', '2017.', '2018.', '2019.', '2020.', '2021.', '2022.', '2023.', '1139', '1140', '1141']):
            continue
        if line.strip().startswith('<span class="text">'):
            line = line.strip()[19:]
        extracted_text.append(line.strip())
    # Joining the lines to form the complete text
    return " ".join(extracted_text)

# Set the path to your .txt file
file_path = 'Mansi texts.txt'
text = extract_text(file_path)
sentences = get_sentences(text)
sentences.to_csv('data/mansi_from_horvath_mono.csv')

