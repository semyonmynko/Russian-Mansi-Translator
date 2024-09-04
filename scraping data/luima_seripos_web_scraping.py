from bs4 import BeautifulSoup
import requests
import re
import nltk
import pandas as pd
#nltk.download('punkt')  # Download the necessary tokenizer models

class LuimaParser():
    def __init__(text):
        pass

    def exec(self, base_url: str , site_page=''):
        sn = 0
        url = base_url + site_page
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # Get all references to paper ussues
        h4_tags = soup.find_all('h4')
        hrefs = list(set([h4.find('a')['href'] for h4 in h4_tags if h4.find('a')])) # Extract all hrefs to issues
        mansi_monolingual = []

        for issue in hrefs:
            issue_page = requests.get(base_url + issue)
            issue_soup = BeautifulSoup(issue_page.content, "html.parser")
            h3_tags = issue_soup.find_all('h3')
            article_hrefs = list(set([h3.find('a')['href'] for h3 in h3_tags if h3.find('a')]))

            for article in article_hrefs:
                article_page = requests.get(base_url + article)
                article_soup = BeautifulSoup(article_page.content, "html.parser")
                # Get russian and mansi articles
                mansi = article_soup.find('div', class_='field-body')
                if mansi:
                    mansi_text = mansi.get_text(separator='\n', strip=True)
                    mansi_text = self.replace_mansi_symbols(mansi_text)
                # russian = article_soup.find('div', class_='field field-name-field-body-russian field-type-text-with-summary field-label-hidden')
                # russian = russian.find('div', class_="field-item even")
                # if russian:
                #     russian_text = russian.get_text(separator='\n', strip=True)
                mansi_monolingual.extend(self.get_sentences(mansi_text))
        pd.Series(mansi_monolingual).to_csv('data/luima_seripos.csv')

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
        #sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+', text)
        return sentences


base_url = 'https://khanty-yasang.ru'
page = '/luima-seripos'
parser = LuimaParser()
parser.exec(base_url, page)