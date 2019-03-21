import configparser
import tkinter as tk
import datetime
import smtplib

import config_utils.config
import ui_utils.main_ui as main_ui
import journal_utils.csv_reader as csv_reader
import crossrefapi_utils.journal_search as searcher
import screenscrape_utils.screenscrape as screenscraper
import screenscrape_utils.result_enum as result_enum
import email_utils.email_handler as email_handler
import debug_utils.debug as debug


class MainSystem(object):
    """
    This class is the main system.
    This class is instantiated at turning on the system.
    """

    def __init__(self):

        debug.d_print("system turned on")
        self.journal_list = None

        #  Config for the progress
        self.config = configparser.ConfigParser()
        self.config.read('./Data-Files/Configurations/progress.ini')
        self.complete = self.config['progress']['complete']
        self.status = self.config['progress']['status']
        self.current_index = int(self.config['progress']['current-index'])
        self.input_file_path = self.config['progress']['input-file-path']
        self.output_file_path = self.config['progress']['output-file-path']
        self.wrong_file_path = self.config['progress']['wrong-file-path']
        self.file_name = None

        # Config for email
        self.email_config = configparser.ConfigParser()
        self.email_config.read('./Data-Files/Configurations/email.ini')
        self.sender = self.email_config['email']['sender']
        self.receiver = self.email_config['email']['receiver']
        self.password = self.email_config['email']['password']

        debug.d_print(self.input_file_path)
        debug.d_print(self.status)

        if self.complete == 'False':
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
        self.root.title("Journal Reality Checking System")
        self.root.geometry("500x400")

        self.ui = main_ui.MainUI(master=self.root, main_system=self)
        self.ui.mainloop()  # starts UI

    def restore_progress(self):
        debug.d_print('|progress restored|')

        if self.status == 'doi-search':
            self.create_journal_list()
            self.search_articles_journal_list()
        elif self.status == 'reality-check':
            self.recreate_journal_list()
            self.check_reality_journal_list()

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
        d = str(datetime.datetime.today())
        date = d[0:4] + d[5:7] + d[8:10] + '-' + d[11:13] + d[14:16]
        self.output_file_path = 'TEMP-DOI-' + date  # file name
        self.wrong_file_path = 'NO-DOI-' + date

        config_utils.config.update_email(self.receiver)
        index = self.current_index
        if index == -1:
            debug.d_print('initialized')
            csv_reader.prepare_temp_csv(self.output_file_path)  # creates a csv temp file
            csv_reader.prepare_wrong_csv(self.wrong_file_path)
            index = 0

        while index < len(self.journal_list):
            title = self.journal_list[index].title
            config_utils.config.update_progress(self.input_file_path, self.output_file_path, self.wrong_file_path,
                                                status='doi-search', index=index, title=title)

            self.search_article(self.journal_list[index])  # DOI Search

            csv_reader.append_doi_row(self.journal_list[index], self.output_file_path)
            csv_reader.append_wrong_row(mode='doi-search', journal=self.journal_list[index],
                                        file_name=self.wrong_file_path)
            index = index + 1

        config_utils.config.clear_progress()
        self.send_email()

    @staticmethod
    def search_article(journal):
        """
        Fetching articles using crossref api.
        :param journal: a journal object
        :return:
        """
        for year in journal.year_dict:
            debug.d_print(journal.title,
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
                debug.d_print(doi)
            else:
                debug.d_print('https://doi.org/' + doi)
        debug.d_print('Search article finished')

    def check_reality_journal_list(self):
        """
        Iterates a list of journal objects and checks a reality of each article
        :param journal_list:
        :return:
        """
        d = str(datetime.datetime.today())
        date = d[0:4] + d[5:7] + d[8:10] + '-' + d[11:13] + d[14:16]
        self.output_file_path = 'RESULT-JOURNALS-' + date  # file name
        self.wrong_file_path = 'PROBLEM-JOURNALS-' + date

        config_utils.config.update_email(self.receiver)
        index = self.current_index
        if index == -1:
            debug.d_print('initialized')
            csv_reader.prepare_result_csv(self.output_file_path)  # creates a csv temp file
            csv_reader.prepare_wrong_csv(self.wrong_file_path)
            index = 0

        while index < len(self.journal_list):
            title = self.journal_list[index].title
            config_utils.config.update_progress(self.input_file_path, self.output_file_path, self.wrong_file_path,
                                                status='reality-check', index=index, title=title)

            self.check_reality(self.journal_list[index])  # Reality Check

            csv_reader.append_journal_row(self.journal_list[index], self.output_file_path)
            csv_reader.append_wrong_row(mode='check-reality', journal=self.journal_list[index],
                                        file_name=self.wrong_file_path)

            index = index + 1

        config_utils.config.clear_progress()
        self.send_email()

    def check_reality(self, journal):
        """
        Screen scrape and determine the journal reality.
        :param journal: a journal object
        :return:
        """
        debug.d_print(journal.title, journal.publisher)
        for year in journal.year_dict:
            # debug.d_print(journal.year_dict[year][2])
            doi = journal.year_dict[year][2].doi
            debug.d_print('https://doi.org/' + str(doi))
            try:
                result = screenscraper.check_journal(doi)  # reality check
            except Exception:
                debug.d_print(year)
                debug.d_print('|exception happened|')
                result = result_enum.Result.OtherException

            journal.year_dict[year][2].result = result  # result is stored in article
            if result is result_enum.Result.Access or result is result_enum.Result.OpenAccess:
                journal.year_dict[year][2].accessible = True

            journal.year_dict[year][2].result = self.convert_result(result)  # result is checked
            debug.d_print(str(year), ':', str(result))

        debug.d_print(journal.wrong_years)
        journal.record_wrong_years()  # wrong years are updated

        debug.d_print('Reality check finished')

    @staticmethod
    def convert_result(result):
        if result == result_enum.Result.Access:
            return 'Accessible'
        elif result == result_enum.Result.OpenAccess:
            return 'Open-Access'
        elif result == result_enum.Result.FreeAccess:
            return 'Free-Access'
        elif result == result_enum.Result.NoAccess:
            return 'No-Access'
        elif result == result_enum.Result.NoArticle:
            return 'No-Article'
        elif result == result_enum.Result.ArticleNotFound:
            return 'Article-Not-Found'
        elif result == result_enum.Result.UnsupportedWebsite:
            return 'Unsupported-Website'
        elif result == result_enum.Result.NetworkError:
            return 'Network-Error'
        elif result == result_enum.Result.PublisherNotFound:
            return 'Publisher-Not-Found'
        elif result == result_enum.Result.OtherException:
            return 'Other-Exception'
        else:
            return 'No-Result-Obtained'

    def send_email(self, email='whimwhimxlife@gmail.com', password='xxxxx'):
        """
        Send the result file to a specified email address.
        :return:
        """
        emailer = email_handler.EmailHandler()

        f1 = csv_reader.path + self.output_file_path + '.csv'
        f2 = csv_reader.path + self.wrong_file_path + '.csv'
        files = [f1, f2]

        emailer.set_sender(sender=self.sender, password=self.password)
        emailer.set_receiver(receiver=self.receiver)
        try:
            emailer.send(files)
        except smtplib.SMTPRecipientsRefused:
            print('Email was incorrect')

    def update(self, code):
        """
        This method is called from main_ui.py for updating this system.
            FILE_UPLOADED
            SEARCH_CLICKED
            DOWNLOAD_CLICKED
        :param code: a message from main_ui.py
        :return:
        """
        debug.d_print('CODE:', code)

        if code == main_ui.MainUI.FILE_UPLOADED:
            self.input_file_path = self.ui.input_file_path
            self.file_name = self.ui.file_name

            if self.ui.mode == self.ui.DOI_SEARCH_MODE:
                self.create_journal_list()
            elif self.ui.mode == self.ui.REALITY_CHECK_MODE:
                self.recreate_journal_list()

        elif code == main_ui.MainUI.SEARCH_CLICKED:
            self.receiver = self.ui.receiver
            self.search_articles_journal_list()

        elif code == main_ui.MainUI.REALITY_CHECK_CLICKED:
            self.receiver = self.ui.receiver
            self.check_reality_journal_list()


def main():
    main_system = MainSystem()
    debug.d_print('"PROGRAM TERMINATED"')


if __name__ == '__main__':
    main()
