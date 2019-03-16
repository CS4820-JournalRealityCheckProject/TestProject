import tkinter as tk
import traceback
from time import sleep
import csv
import configparser

import config_utils.config
import journal_ui.main_ui as main_ui
import journal_utils.csv_reader as csv_reader
import crossrefapi_utils.journal_search as searcher
import screenscrape_utils.screenscrape as screenscraper
import email_utils.email_handler as email_handler


class MainSystem(object):
    """
    This class is the main system.
    This class is instantiated at turning on the system.
    """

    def __init__(self):
        print("system turned on")
        self.journal_list = None
        self.file_path = None

        self.config = configparser.ConfigParser()
        self.config.read('progress.ini')
        self.complete = self.config['progress']['complete']
        self.status = self.config['progress']['status']
        self.current_index = int(self.config['progress']['current-index'])
        self.input_file_path = self.config['progress']['input-file-path']
        self.output_file_path = self.config['progress']['output-file-path']
        print(self.input_file_path)
        print(self.status)

        if self.complete == 'False':
            print()
            choice = input('Do you want to continue what interrupted last time?(y/n)')
            if choice == 'y':
                self.restore_progress()
            else:
                config_utils.config.clear_progress()
                self.complete = 'True'
                self.status = '0'
                self.input_file_path = 'no-path'
                self.output_file_path = 'no-path'
                self.current_index = -1

        self.ui = None
        self.root = tk.Tk()
        self.root.title("Journal Reality")
        self.ui = main_ui.MainUI(master=self.root, main_system=self)
        self.ui.mainloop()  # starts UI

    def restore_progress(self):
        print('|progress restored|')

        if self.status == 'doi-search':
            self.create_journal_list()
            self.search_articles_journal_list()
        elif self.status == 'reality-check':
            self.recreate_journal_list()
            self.check_reality_journal_list()
            # check articles

    def create_journal_list(self):
        """
        Creates a list of journals with a given file path
        :return: a list of journal objects
        """
        self.journal_list = csv_reader.construct_journal_list_from(self.input_file_path)

    def recreate_journal_list(self):
        self.journal_list = csv_reader.reconstruct_journal_list_from(self.input_file_path)

    def search_articles_journal_list(self):
        """iterates a list of journal and fetches an article and a doi for each year"""
        self.output_file_path = 'doi-articles'  # file name
        index = self.current_index
        if index == -1:
            print('initialized')
            csv_reader.prepare_temp_csv(self.output_file_path)  # creates a csv temp file
            index = 0

        while index < len(self.journal_list):
            title = self.journal_list[index].title
            config_utils.config.update_progress(self.input_file_path, self.output_file_path,
                                                status='doi-search', index=index, title=title)
            self.search_article(self.journal_list[index])
            csv_reader.append_doi_row(self.journal_list[index], self.output_file_path)

            index = index + 1

        self.send_email()
        config_utils.config.clear_progress()

    @staticmethod
    def search_article(journal):
        """
        Fetching articles using crossref api.
        :param journal: a journal object
        :return:
        """
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
            if doi is None:
                print(doi)
            else:
                print('https://doi.org/' + doi)
        print('Search article finished')

    def check_reality_journal_list(self):
        """
        Iterates a list of journal objects and checks a reality of each article
        :param journal_list:
        :return:
        """
        self.output_file_path = 'result-journals'  # file name
        index = self.current_index
        if index == -1:
            print('initialized')
            csv_reader.prepare_result_csv(self.output_file_path)  # creates a csv temp file
            index = 0

        while index < len(self.journal_list):
            title = self.journal_list[index].title
            config_utils.config.update_progress(self.input_file_path, self.output_file_path,
                                                status='reality-check', index=index, title=title)
            self.check_reality(self.journal_list[index])
            csv_reader.append_journal_row(self.journal_list[index], self.output_file_path)


            index = index + 1

        self.send_email()
        config_utils.config.clear_progress()
        self.ui.quit()

    @staticmethod
    def check_reality(journal):
        """
        Screen scrape and determine the journal reality.
        :param journal: a journal object
        :return:
        """
        print(journal.title, journal.publisher)
        for year in journal.year_dict:
            # print(journal.year_dict[year][2])
            doi = journal.year_dict[year][2].doi
            print('https://doi.org/' + doi)
            try:
                result = screenscraper.check_journal(doi)  # reality check
            except Exception:
                print('|exception happened|')
            journal.year_dict[year][2].accessible = result
            print(result.name)
        journal.record_wrong_years()  # wrong years are updated

        print('Reality check finished')

    def send_email(self, email='whimwhimxlife@gmail.com', password='xxxxx'):
        """
        Send the result file to a specified email address.
        :return:
        """
        emailer = email_handler.EmailHandler()
        your_email = email

        sender = your_email
        password = password

        sender = input('Please enter sender email:')
        password = input("Please enter a password for the sender: ")
        receiver = input('Please enter receiver email:')

        f = './' + self.output_file_path + '.csv'
        files = [f, "./email_utils/test2.csv"]

        emailer.set_sender(sender=sender, password=password)
        emailer.set_receiver(receiver=receiver)
        emailer.send(files)

    def update(self, code):
        """
        This method is called from main_ui.py for updating this system.
            FILE_UPLOADED
            SEARCH_CLICKED
            DOWNLOAD_CLICKED
        :param code: a message from main_ui.py
        :return:
        """
        print('CODE:', code)

        if code == main_ui.MainUI.FILE_UPLOADED:
            self.file_path = self.ui.input_file_path
            self.input_file_path = self.ui.input_file_path
            if self.ui.mode == self.ui.DOI_SEARCH_MODE:
                self.create_journal_list()
            elif self.ui.mode == self.ui.REALITY_CHECK_MODE:
                self.recreate_journal_list()

        elif code == main_ui.MainUI.SEARCH_CLICKED:
            self.search_articles_journal_list()
            # n = int(input('Enter an index:'))
            # self.search_article(self.journal_list[n])

        elif code == main_ui.MainUI.REALITY_CHECK_CLICKED:
            self.check_reality_journal_list()

        elif code == main_ui.MainUI.EMAIL_CLICKED:
            self.send_email()


def start_with_ui(file_path="./journal_utils/journal-csv/use-this.csv"):
    """
    System starts the UI.
    :param file_path: the file path to the csv file of journals
    :return:
    """
    main_system = MainSystem()
    main_system.main_ui.mainloop()  # starts UI


def start_without_ui(file_path="./journal_utils/journal-csv/use-this.csv"):
    """
    Test method for starting the system without UI.
    :param file_path:
    :return: file_path: the file path to the csv file of journals
    """
    main_system = MainSystem()
    print('here')
    # main_system.send_email()
    # main_system.input_file_path = file_path
    # main_system.create_journal_list()


def main():
    """
    Main method to be called when the system gets turned on.
    :return:
    """
    #  start_with_ui()  # the main system
    start_without_ui()  # the test system


def test_call(turn_on_ui, file_path):
    """
    Test method to be called from test.py
    :param turn_on_ui: boolean to activate UI or not.
    :param file_path: the file path to the csv file of journals
    :return: file_path:
    """
    if turn_on_ui:
        start_with_ui(file_path)
    else:
        start_without_ui(file_path)


if __name__ == '__main__':
    main()
