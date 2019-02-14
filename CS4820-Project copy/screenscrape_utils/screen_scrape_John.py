import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class ScreenScraper:
    key_sd = ""

    def __init__(self):
        self.key_sd = open("ScienceDirectAPI.txt").read()

    @staticmethod
    def doi_to_url(doi):
        url = "http://dx.doi.org/" + doi
        r = requests.get(url, allow_redirects=False)
        return r.headers['Location']

    def science_direct(self, doi):
        parameters = {"APIKey": self.key_sd}
        r = requests.get("https://api.elsevier.com/content/article/doi/" + doi, params=parameters)

        if r.text == "":
            return "Server Down"

        root = ET.fromstring(r.text)
        for item in root.iter():
            if item.text == "FULL-TEXT":
                return True
            if item.text == "RESOURCE_NOT_FOUND":
                return "Article not found"
        return False

    @staticmethod
    def springer(doi):
        url = 'https://link.springer.com/article/' + doi

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        free = soup.find('div', {"id": "open-choice-icon"})
        no_access = soup.find('div', {"id": "article_no_access_banner"})
        school_access = soup.find('div', {"class": "note test-pdf-link"}, {"id": "cobranding-and-download-"
                                                                                 "availability-text"})
        if no_access:
            return False
        if school_access:
            return True
        if free.text == "Open Access":
            return "Open access"


    @staticmethod
    def oxford(doi):
        url = ScreenScraper.doi_to_url(doi)

        # Lie about who we are to get access
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        for title in soup.find_all('title'):
            if 'OUP | Not Found' in title.text:
                return "Article not found"
        if soup.find('div', {"class": "article-top-info-user-restricted-options"}):
            return False
        return True

    @staticmethod
    def acs(doi):
        # Looks at the headers for things that look like an article
        # Needs a lot of testing if the current method is used
        # So returns an array instead of a simple true or false
        url = 'https://pubs.acs.org/doi/' + doi

        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')

        results = [True, "_", "_", "_", "_", "_"]

        for div in soup.find_all("h2"):
            if div.text == "Introduction":
                results[1] = 'I'
            elif "Result" in div.text:
                results[2] = 'R'
            if div.text == "Conclusion":
                results[3] = 'C'
            if div.text == "Acknowledgments":
                results[4] = 'A'
            if div.text == "References":
                results[5] = 'R'

        # Abstract appears in the third line if no access
        header = r.text.split('\n')[2]
        if 'Abstract' in header:
            results[0] = False

        return results


article_list = [['ACS', '10.1021/acs.inorgchem.8b03148'],
                ['Oxford Journal', '10.1093/jigpal/jzy015'],
                ['Oxford Journal', '10.1111/j.1095-8339.2011.01155.x'],  # Open Access
                ['Oxford Journal', '10.1111/bij.12521'],  # Open Access
                ['Science Direct', '10.1016/j.ijrmhm.2018.07.009'],
                ['Science Direct', '10.1016/j.burnso.2018.03.001'],  # Open access
                ['Springer', '10.1007/s11127-018-0568-7'],
                ['Springer', '10.1007/s00048-018-0199-6'],
                ['Springer', '10.1007/s10763-017-9875-6'],
                ]

ss = ScreenScraper()

for article in article_list:
    if article[0] == 'Oxford Journal':
        result = ScreenScraper.oxford(article[1])
    elif article[0] == 'Springer':
        result = ScreenScraper.springer(article[1])
    elif article[0] == 'ACS':
        result = ScreenScraper.acs(article[1])
    elif article[0] == 'Science Direct':
        result = ss.science_direct(article[1])
    print(str(result) + ": " + article[1])



