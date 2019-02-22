import tkinter as tk

import journal_ui.main_ui as main_ui
import journal_utils.csv_reader as csv_reader
import crossrefapi_utils.journal_search as searcher
import screenscrape_utils.screenscrape as screenscraper


class MainSystem:

    def __init__(self):
        print("system turned on")
        self.journal_list = None
        self.file_path = None
        self.root = tk.Tk()
        self.main_ui = main_ui.MainUI(master=self.root, main_system=self)
        self.main_ui.mainloop()  # starts UI

    def create_journal_list(self):
        self.journal_list = csv_reader.read_csv_create_journal(self.file_path)

    def test_print(self):
        n = 0
        while not (n == -1):
            n = int(input('Enter an index:'))
            if n != -1:
                if self.journal_list is not None:
                    print(self.journal_list[n])
                    self.search(self.journal_list[n])
        print('finished')

    def search(self, journal):
        for year in journal.year_dict:
            print(journal.title,
                  journal.year_dict[year][0],  # start_date
                  journal.year_dict[year][1],  # end_date
                  journal.print_issn, journal.online_issn)
            doi = searcher.search_journal(journal.title,
                                          journal.year_dict[year][0],  # start_date
                                          journal.year_dict[year][1],  # end_date
                                          journal.print_issn, journal.online_issn)
            journal.year_dict[year][2].doi = doi
            # journal.year_article_dict[year].doi = doi
            print(doi)

    def fetch_article(self, publisher, title, print_issn, online_issn, begin_date, end_date):
        # return crossref_utils.fetch(publisher, title, print_issn, online_issn, begin_date, end_date);
        print("crossref.fetch_article is called here")

    def check_reality(self, journal):
        # return screenscrape_utils.determine_reality(doi)
        print("journal reality check will be proceeded here")
        scraper = screenscraper.ScreenScraper
        print(journal.title, journal.publisher)
        for year in journal.year_dict:
            # print(journal.year_dict[year][2])
            doi = journal.year_dict[year][2].doi
            print(doi)
            article = [journal.publisher, doi]
            result = scraper.check_journal(scraper, doi=doi)
            print(str(result))

        # access = screenscrape_utils.determine_reality(doi)
        # journal.year_dict[year][2].accessible = access

    def update(self, code):
        print('CODE:', code)
        if code == 'FILE_UPLOADED':
            self.file_path = self.main_ui.input_file_path
            self.create_journal_list()

        elif code == 'SEARCH_CLICKED':
            print('SIZE:', len(self.journal_list))
            self.test_print()

        elif code == 'DOWNLOAD_CLICKED':
            print('"Download is ready"')
            print('enter an index')
            n = int(input('Enter an index:'))
            self.check_reality(self.journal_list[n])


def main():
    main_system = MainSystem()


def start():
    main_system = MainSystem()


if __name__ == '__main__':
    main()
