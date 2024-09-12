from bs4 import BeautifulSoup
import requests
import re
import nltk
import pandas as pd
import csv
from tqdm import tqdm
#nltk.download('punkt')  # Download the necessary tokenizer models

class LuimaParser():
    def __init__(self):
        def read_dictionary(filepath):
            data_dict = {}
            with open(filepath, mode='r', encoding='utf-8') as file:
                print(f'Reading dictionary located at {filepath}...')
                # Create a CSV reader with '|' as the delimiter (since your data uses '|')
                reader = csv.DictReader(file, delimiter='|')
            
                # Iterate over each row in the CSV file
                for row in reader:
                    # Use 'target' as the key and 'source' as the value
                    if row['target'] and row['source']:  # Ensure no empty values are added
                        data_dict[row['target']] = row['source']
                print('Reading completed!')
            return data_dict
        
        self.dict1 = read_dictionary('data/dataset_dict1.csv')
        self.dict2 = read_dictionary('data/dataset_dict2.csv')

    def exec(self, base_url: str , site_page=''):
        sn = 0
        url = base_url + site_page
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # Get all references to paper ussues
        #h4_tags = soup.find_all('h4')
        #hrefs = list(set([h4.find('a')['href'] for h4 in h4_tags if h4.find('a')])) # Extract all hrefs to issues
        years = soup.find_all('div', class_='block-toggle')
        years = [year for year in years if not any(title in str(year) for title in ['2012 год', '2013 год'])]
        hrefs = []
        for year in years:
            # Find all <a> tags within the <div> element
            links = year.find_all('a')
            # Extract the href attribute from each <a> tag
            for link in links:
                hrefs.append(link['href'])
        mansi_monolingual = []
        russian_monolingual = []

        print('Getting issues and articles...')
        for issue in tqdm(hrefs):
            issue_page = requests.get(base_url + issue)
            issue_soup = BeautifulSoup(issue_page.content, "html.parser")
            h3_tags = issue_soup.find_all('h3')
            article_hrefs = list(set([h3.find('a')['href'] for h3 in h3_tags if h3.find('a')]))

            for article in article_hrefs:
                article_page = requests.get(base_url + article)
                article_soup = BeautifulSoup(article_page.content, "html.parser")
                # Get russian and mansi articles
                mansi_text = self.get_mansi(article_soup)
                mansi_monolingual.extend(self.get_sentences(mansi_text))
                russian_text = self.get_russian(article_soup)
                russian_monolingual.extend(self.get_sentences(russian_text))
        print('Data collected!')
        print('Starting getting parallel sentences...')
        self.get_parallel_sentences(mansi_monolingual, russian_monolingual)
        pd.Series(mansi_monolingual).to_csv('luima_seripos_mansi.csv')
        pd.Series(russian_monolingual).to_csv('luima_seripos_russian.csv')

    def get_mansi(self, article_soup):
        mansi = article_soup.find('div', class_='field-body')
        if mansi:
            mansi_text = mansi.get_text(separator='\n', strip=True)
            mansi_text = self.replace_mansi_symbols(mansi_text)
            return mansi_text
        else:
            return ''
    
    def get_russian(self, article_soup):
        try:
            russian = article_soup.find('div', class_='field field-name-field-body-russian field-type-text-with-summary field-label-hidden')
            russian = russian.find('div', class_="field-item even")
            if russian:
                russian_text = russian.get_text(separator='\n', strip=True)
            return russian_text
        except AttributeError:
            return ''

    def replace_mansi_symbols(self, mansi_text: str):
        # Ӯ, ӯ, ӈ, Ӣ, ӣ already in unicode
        macron = '\u0304'
        mansi_text = mansi_text.replace('', 'э' + macron)
        mansi_text = mansi_text.replace('', 'Э' + macron)

        mansi_text = mansi_text.replace('', 'а' + macron)
        mansi_text = mansi_text.replace('', 'А' + macron)

        mansi_text = mansi_text.replace('', 'о' + macron)
        mansi_text = mansi_text.replace('', 'О' + macron)

        mansi_text = mansi_text.replace('', 'я' + macron)
        mansi_text = mansi_text.replace('', 'Я' + macron)

        mansi_text = mansi_text.replace('', 'е' + macron)
        #mansi_text = mansi_text.replace('', 'Е' + macron)

        mansi_text = mansi_text.replace('', 'ё' + macron)
        mansi_text = mansi_text.replace('', 'Ё' + macron)

        mansi_text = mansi_text.replace('', 'ю' + macron)
        mansi_text = mansi_text.replace('', 'Ю' + macron)

        mansi_text = mansi_text.replace('', 'ы' + macron)
        #mansi_text = mansi_text.replace('', 'Ы' + macron)
        return mansi_text
    
    def get_sentences(self, text: str):
        sentences = nltk.sent_tokenize(text.replace('\n', ''))
        return sentences
    
    def get_parallel_sentences(self, mansi_sentences, russian_sentences):
        """
        Based on https://arxiv.org/pdf/2103.13272
        Quote: 'To extract sentences from a document, we first translate the source sentence to English using a word dictionary,
        then we quantify the word overlap using Jaccard similarity score, which is defined as:
        Jaccard_sim(s, t) = |s ∩ t|/|s ∪ t|. We then select pairs that have Jaccard Similarity of at least 0.1.'
        """
        translated_mansi_sentences = [self.translate_mansi_to_russian(sentence) for sentence in mansi_sentences]

        def jaccard_similarity(set1, set2):
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return intersection / union if union != 0 else 0
        
        similar_pairs = []
        scores = []
        for russian_sentence, mansi_sentence in zip(russian_sentences, translated_mansi_sentences):
            russian_words_set = set(russian_sentence.split())
            mansi_words_set = set(mansi_sentence.split())
            
            jaccard_score = jaccard_similarity(russian_words_set, mansi_words_set)
            if jaccard_score >= 0.1:
             scores.append(jaccard_score)
        print(scores)
    
    def translate_mansi_to_russian(self, mansi_sentence):
        translated_words = []
        for word in mansi_sentence.split():
            if word in self.dict1:
                translated_words.append(self.dict1[word])
            elif word in self.dict2:
                translated_words.append(self.dict2[word])
            else:
                translated_words.append(word)  # Word not in dicts, keep it as is
        return ' '.join(translated_words)


base_url = 'https://khanty-yasang.ru'
page = '/luima-seripos'
parser = LuimaParser()
parser.exec(base_url, page)