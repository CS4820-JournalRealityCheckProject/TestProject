import tkinter as tk
from time import sleep

import journal_ui.main_ui as main_ui
import journal_utils.csv_reader as csv_reader
import crossrefapi_utils.journal_search as searcher
import screenscrape_utils.screenscrape as screenscraper
import email_utils.email_handler as email_handler


class MainSystem:

    def __init__(self):
        print("system turned on")
        self.journal_list = None
        self.file_path = None
        # self.root = tk.Tk()
        # self.main_ui = main_ui.MainUI(master=self.root, main_system=self)
        # self.main_ui.mainloop()  # starts UI

    def create_journal_list(self):
        self.journal_list = csv_reader.read_csv_create_journal(self.file_path)

    @staticmethod
    def search_article(journal):
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
        print('Search article finished')

    @staticmethod
    def check_reality(journal):
        scraper = screenscraper.ScreenScraper
        print(journal.title, journal.publisher)
        for year in journal.year_dict:
            # print(journal.year_dict[year][2])
            doi = journal.year_dict[year][2].doi
            if doi is None:
                print('DOI is none')
            else:
                print(doi)
                result = scraper.check_journal(scraper, doi=doi)
                print(str(result))
        print('Reality check finished')

    @staticmethod
    def send_email():
        emailer = email_handler.EmailHandler()
        your_email = '@upei.ca'

        sender = your_email
        receiver = your_email
        password = input("Please enter a password: ")
        files = ["./email_utils/test.csv", "./email_utils/test2.csv"]

        emailer.set_sender(sender=sender, password=password)
        emailer.set_receiver(receiver=receiver)
        emailer.send(files)

    def update(self, code):
        print('CODE:', code)

        if code == 'FILE_UPLOADED':
            self.file_path = self.main_ui.input_file_path
            self.create_journal_list()
            print('SIZE:', len(self.journal_list))

        elif code == 'SEARCH_CLICKED':
            n = int(input('Enter an index:'))
            self.search_article(self.journal_list[n])

        elif code == 'DOWNLOAD_CLICKED':
            n = int(input('Enter an index:'))
            self.check_reality(self.journal_list[n])


def start_with_ui():
    main_system = MainSystem()
    main_system.main_ui.mainloop()  # starts UI


def start_without_ui():
    main_system = MainSystem()
    # main_system.send_email()
    main_system.file_path = "./journal_utils/journal-csv/use-this.csv"
    main_system.create_journal_list()
    n = int(input('Enter an index(-1 to exit):'))
    while n != -1:
        journal = main_system.journal_list[n]
        print('From', journal.expected_subscription_begin,
              'to', journal.expected_subscription_end)
        main_system.search_article(journal)
        main_system.check_reality(journal)
        n = int(input('Enter an index(-1 to exit):'))


def main():
    #  start_with_ui()  # the main system
    start_without_ui()  # the test system


def test_call(turn_on_ui):
    if turn_on_ui:
        start_with_ui()
    else:
        start_without_ui()


if __name__ == '__main__':
    main()
