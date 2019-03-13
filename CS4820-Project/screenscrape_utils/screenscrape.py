import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup


class ScreenScraper:
    key_sd = ""

    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0'
    }

    def __init__(self):
        if __name__ == '__main__':
            self.key_sd = open("ScienceDirectAPI.txt").read()
        else:
            self.key_sd = open("screenscrape_utils/ScienceDirectAPI.txt").read()

    @staticmethod
    def doi_to_url(doi):
        url = "http://dx.doi.org/" + doi
        r = requests.get(url, allow_redirects=False)
        return r.headers['Location']

    @staticmethod
    def doi_to_journal(doi):
        url = "http://dx.doi.org/" + doi
        headers = {"accept": "application/x-bibtex"}
        r = requests.get(url, headers=headers)
        # Very messy way to get the publisher
        for line in r.text.split('\n'):
            if 'publisher' in line:
                return line[14:-2]

    def check_journal(self, doi):
        publisher = self.doi_to_journal(doi)
        print(publisher)
        try:
            if publisher == "Royal Society of Chemistry ({RSC})":
                return self.chem_gold(doi)
            elif publisher == "American Chemical Society ({ACS})":
                return self.acs(doi)
            elif publisher == "Oxford University Press ({OUP})":
                return self.oxford(doi)
            elif publisher == "Elsevier {BV}":
                return self.science_direct(doi)
            elif publisher == "Springer Nature" or publisher == "Pleiades Publishing Ltd":
                return self.springer(doi)
            elif publisher is None:
                return 'Could not find publisher'
            else:
                return '[' + publisher + '] Not found'
        except requests.exceptions.ConnectionError:
            return 'Could not connect to journal webpage'

    @staticmethod
    def science_direct(doi):
        url = ScreenScraper.doi_to_url(doi)
        r = requests.get(url)
        # There is a meta redirect to follow, use soup to follow
        soup1 = BeautifulSoup(r.text, 'html.parser')
        refresh = soup1.find("meta", {'http-equiv': "REFRESH"})
        # Take content and strip out everything before Redirect=
        link = refresh["content"].split('Redirect=')[1]
        # Remove everything after the questionmark(%3F)
        link = link.split('%3F')[0]
        # Fix some characters
        link = link.replace('%3A', ':')
        link = link.replace('%2F', '/')

        r = requests.get(link, headers=ScreenScraper.USER_AGENT)
        soup2 = BeautifulSoup(r.text, 'html.parser')
        if soup2.find("div", {'class': "OpenAccessLabel"}):
            return "Open access"
        # Look at the download button
        download_text = soup2.find("span", {'class': "pdf-download-label u-show-inline-from-lg"}).contents[0]
        if 'Get Access' in download_text:
            return False
        if 'Download' in download_text:
            return True

        return 'Some kind of error'

    def science_direct_api(self, doi):
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

        # Check for Wiley
        if soup.find('a', {'title':'Wiley Online Library'}):
            return ScreenScraper.wiley(soup)

        if not soup.find('div', {"class": "oup-header"}):
            return "Can not read journal"
        if soup.find('i', {"class": "icon-availability_open"}):
            return "Open access"
        if soup.find('i', {"class": "icon-availability_free"}):
            return "Free access"
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

    @staticmethod
    def chem_gold(doi):
        url = ScreenScraper.doi_to_url(doi)
        # Pass through another redirect
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        r = requests.get(url, headers=headers)
        # change the url to get to the article
        url = r.url.replace("ArticleLanding", "articlepdf")
        r = requests.get(url, headers=headers)
        # Check if we were kicked out of the article
        if "articlepdf" in r.url:
            return True
        return False


    @staticmethod
    def wiley(soup):
        """
        Currently just a filler,
        other methods can call this if they find themselves on a Wiley library page
        """
        return 'Article on Wiley Online Library'

if __name__ == '__main__':

    article_list = [ '10.1111/boj.2001.135.issue-1' ]

    ss = ScreenScraper()

    for article in article_list:
        result = ss.check_journal(article)
        print(str(result) + ": " + str(article))
