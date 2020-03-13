'''
Implements a simple scraper for google search page results, wikipedia, and NYT.
Scraping featured snippets from Google has two different methods:
using the scrape_google_snippets_raw function and the scrape_google_snippets
function. The scrape_google_snippets function uses the SerpScrap python library.
The scrape_google_snippets_raw function uses a combination of BeautifulSoup,
regex, and the nltk English words corpus.
'''
import requests
import re
import nltk
import serpscrap
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.query = ''
        #self.snippet_re = '{text-align:center}([A-Za-z0-9.;,()\'\:\- ]+) \.\.\. ([A-Za-z0-9.;,()\'\:\- ]+) \.\.\.'
        self.snippet_re = '{text-align:center}([A-Za-z0-9.;,()|\/\'\:\- %]+)'
        self.words = set(nltk.corpus.words.words())
    '''
    Implements a scrape of a Google search page (HTML reading) from a query using BeautifulSoup, regex,
    and the nltk corpus. Needs some bug fixes (writes all matching snippets to the file inluding
    the first 4 snippets which are basic Google comments to users)
    '''
    def scrape_google_snippets_raw(self, query='', file='info.txt'):
        f = open(file, 'a')
        
        query = self.create_readable_query(query)
        
        r = requests.get(query)
        html_doc = r.text
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        to_parse = soup.get_text()
        
        for l in self.find_text(to_parse):
            f.write(l)
        f.write(to_parse)
        f.close()
    
    '''
    Scrapes Google search page (HTML reading) using SerpScrap
    '''
    def scrape_google_snippets(self, query='', file='info.txt'):
        f = open(file, 'a')
        
        keyword = [query]

        config = serpscrap.Config()
        config.set('scrape_urls', False)

        scrap = serpscrap.SerpScrap()
        scrap.init(config=config.get(), keywords=keyword)
        results = scrap.run()
        return results
        
    
    def scrape_wikipedia_pages(self, possible_pages=[], file='info.txt'):
        pass
    
    '''
    Writes basic information concerning the query using the NYT API to a given file.
    The string 'type' can be one of five types and each maps to at least one API:
    'basic' --> Article Search
    'keyword' --> Semantic, Times Tag
    'current' --> Top Stories
    'time' --> Archive API
    '''
    def scrape_NYT(self, type='event',query='',file='info.txt'):
        pass

    def erase(self, file='info.txt'):
        f = open('info.txt', 'w')
        f.write('')
        f.close()
    
    '''
    Helper function to scrape_google_snippets_raw().
    Uses regex and the nltk corpus to find possible snippets of information from given nonsense HTML text
    '''
    def find_text(self, to_parse=''):
        matches = re.findall(self.snippet_re, to_parse)
        assessed = []
        '''
        for m in matches:
            test = m.lower()
            test = test.split(' ')
            if (test[0] in self.words or test[0].isnumeric()) and len(test) > 2 and test[0] != '0': #2 is an arbitrary threshhold that can be changed
                assessed.append(m)
        '''
        return matches
    
    '''
    Creates hyperlink readable by Google search engine from user query
    '''
    def create_readable_query(self, query=''):
        query = query.replace(' ', '+')
        query = 'https://www.google.com/search?q=' + query
        return query
        
if __name__ == '__main__':
    scrapy = Scraper()
    scrapy.erase()
    scrapy.scrape_google_snippets_raw(query='coronavirus 2020')
    
