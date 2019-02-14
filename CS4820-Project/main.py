import tkinter as tk

import journal_ui.main_ui as main_ui
import journal_utils.csv_reader as csv_reader


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
            if self.journal_list is not None:
                print(self.journal_list[n])
        print('finished')

    def search(self):
        for journal in self.journal_list:
            for year in journal.year_dict:
                doi = crossref_utils.fetch(journal.year_dict[year][0],  # start_date
                                           journal.year_dict[year][1],  # end_date
                                           journal.title, journal.print_issn, journal.online_issn)

                access = screenscrape_utils.determine_reality(doi)
                journal.year_dict[year][2].accessible = access

    def fetch_article(self, publisher, title, print_issn, online_issn, begin_date, end_date):
        # return crossref_utils.fetch(publisher, title, print_issn, online_issn, begin_date, end_date);
        print("crossref.fetch_article is called here")

    def check_reality(self, doi):
        # return screenscrape_utils.determine_reality(doi)
        print("journal reality check will be proceeded here")

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


def main():
    main_system = MainSystem()


def start():
    main_system = MainSystem()


if __name__ == '__main__':
    main()
