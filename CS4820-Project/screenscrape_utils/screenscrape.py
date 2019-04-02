import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, quote
import os
from bs4 import BeautifulSoup

if __name__ == '__main__':
    from result_enum import Result
    import platform_reader
else:
    from screenscrape_utils.result_enum import Result
    import screenscrape_utils.platform_reader as platform_reader

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0'
}

config = platform_reader.read_platforms()



def doi_to_url(doi):
    url = "http://dx.doi.org/" + quote(doi)
    r = requests.get(url, allow_redirects=False)
    return r.headers['Location']


def check_journal (doi, listed_platform):
    if doi is None or doi == "":
        return Result.NoArticle
    # get config array
    pub_data = None
    for publisher in config:
        if listed_platform == publisher[0]:
            pub_data = publisher
    if pub_data is None:
        return Result.PublisherNotFound

    url = doi_to_url(doi)
    base_url = "{0.netloc}".format(urlsplit(url))
    if pub_data[2] != base_url:
        return Result.UnsupportedWebsite

    method_result = globals()[pub_data[1]](url)
    return method_result


def science_direct(url):
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

    r = requests.get(link, headers=USER_AGENT)
    soup2 = BeautifulSoup(r.text, 'html.parser')
    if soup2.find("div", {'class': "OpenAccessLabel"}):
        return Result.OpenAccess
    # Look at the download button
    download_text = soup2.find("span", {'class': "pdf-download-label u-show-inline-from-lg"}).contents[0]
    if 'Get Access' in download_text:
        return Result.NoAccess
    if 'Download' in download_text:
        return Result.Access

    # Wrong site or Website changed
    return Result.UnsupportedWebsite


def springer(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    free = soup.find('div', {"id": "open-choice-icon"})
    no_access = soup.find('div', {"id": "article_no_access_banner"})
    school_access = soup.find('div', {"class": "note test-pdf-link"}, {"id": "cobranding-and-download-"
                                                                             "availability-text"})
    if school_access is None:
        school_access = soup.find('div', {"class": "download-article test-pdf-link"})

    if no_access:
        return Result.NoAccess
    if school_access:
        return Result.Access
    if free is not None and free.text == "Open Access":
        return Result.OpenAccess

    # Wrong site or Website changed
    return Result.UnsupportedWebsite


def oxford(url):
    r = requests.get(url, headers=USER_AGENT)

    soup = BeautifulSoup(r.text, 'html.parser')

    if not soup.find('div', {"class": "oup-header"}):
        return Result.UnsupportedWebsite
    if soup.find('i', {"class": "icon-availability_open"}):
        return Result.OpenAccess
    if soup.find('i', {"class": "icon-availability_free"}):
        return Result.FreeAccess
    for title in soup.find_all('title'):
        if 'OUP | Not Found' in title.text:
            return Result.ArticleNotFound
    if soup.find('div', {"class": "article-top-info-user-restricted-options"}):
        return Result.NoAccess
    return Result.Access


def acs(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    # Abstract appears in the third line if no access
    header = r.text.split('\n')[2]
    if 'Abstract' in header:
        return Result.NoAccess

    return Result.Access


def rsc(url):
    # Pass through another redirect
    r = requests.get(url, headers=USER_AGENT)
    # change the url to get to the article
    url = r.url.replace("ArticleLanding", "articlepdf")
    r = requests.get(url, headers=USER_AGENT)
    # Check if we were kicked out of the article
    if "articlepdf" in r.url:
        return Result.Access
    return Result.NoAccess


if __name__ == '__main__':

    article_list = [['10.1021/bc9700291', "ACS (CRKN)"],
                    ['10.1039/a806580b', 'Royal Society of Chemistry Gold (CRKN)'],
                    ['10.1080/10635150252899770', 'Oxford Journals (CRKN)'],
                    ['10.1016/s1578-2190(08)70378-0', 'ScienceDirect (CRKN)'],
                    ['10.1007/s00026-005-0237-z', 'SpringerLINK (CRKN)']
                    ]

    for article in article_list:
        print(article[0]+" : "+article[1])
        result = check_journal(article[0], article[1])
        print(result.name+"\n")
