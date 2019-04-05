import configparser
import tkinter as tk
import datetime
import smtplib
import threading
import json

import config_utils.config
import ui_utils.main_ui as main_ui
import ui_utils.popup as popup
import journal_utils.csv_reader as csv_reader
import crossrefapi_utils.journal_search as searcher
import screenscrape_utils.screenscrape as screenscraper
import screenscrape_utils.result_enum as result_enum
import email_utils.email_handler as email_handler
import email_utils.email_server_handler as email_server
import debug_utils.debug as debug


class MainSystem(object):
    """
    This class is the main system.
    This class is instantiated at turning on the system.
    """

    # two modes
    DOI_SEARCH_MODE = 'doi-search'
    REALITY_CHECK_MODE = 'reality-check'

    # indexes used for year_dict[year][index] for Journal
    # year_dict = {year: (begin_date, end_date, Article)}
    BEGIN = 0
    END = 1
    ARTICLE = 2

    # variables
    LAST_FINISHED = -1

    def __init__(self):

        debug.d_print("system turned on")
        self.journal_list = None

        #  Config for the progress
        self.config = configparser.ConfigParser()
        self.config.read(config_utils.config.PATH_TO_PROGRESS_INI)
        self.complete = None

        # handles no progress.ini exists or file path is incorrect
        try:
            self.complete = self.config['progress']['complete']  # PROBLEM
        except KeyError as e:  # if
            progress_ini_path = config_utils.config.clear_progress()
            self.config.read(progress_ini_path)
            self.complete = self.config['progress']['complete']
            debug.d_print('new progress.ini created')

        # Config for progress
        self.status = self.config['progress']['status']
        self.current_index = int(self.config['progress']['current-index'])
        self.input_file_path = self.config['progress']['input-file-path']
        self.output_file_path = self.config['progress']['output-file-path']
        self.wrong_file_path = self.config['progress']['wrong-file-path']
        self.file_name = None
        self.continue_output_file_path = None

        # Config for email
        self.email_config = configparser.ConfigParser()
        self.email_config.read(config_utils.config.PATH_TO_EMAIL_INI)
        self.sender = self.email_config['email']['sender']
        self.receiver = self.email_config['email']['receiver']
        self.password = self.email_config['email']['password']

        debug.d_print(self.input_file_path)
        debug.d_print(self.status)

        # Prepare UI
        self.ui = None
        self.root = tk.Tk()
        self.root.title("Journal Reality Checking System")
        self.root.geometry("600x400")

        if self.complete == 'False':
            title = self.status
            msg = 'Do you want to recover the progress last time?'
            yes = popup.resume_yesno(title, msg)
            if yes:
                self.ui = main_ui.MainUI(master=self.root, main_system=self)
                self.restore_progress()
                self.ui.mainloop()  # starts UI

            else:
                config_utils.config.clear_progress()
                self.reset_member_variables()
                # Instantiate MainUI class object
                self.ui = main_ui.MainUI(master=self.root, main_system=self)
                self.ui.mainloop()  # starts UI
        else:
            # Instantiate MainUI class object
            self.ui = main_ui.MainUI(master=self.root, main_system=self)
            self.ui.mainloop()  # starts UI

    def restore_progress(self):
        debug.d_print('|progress restored|')
        self.ui.restore_ui(self.status)  # ui is recovered.
        print(self.status)

        if self.status == 'doi-search':
            self.create_journal_list()
            # self.iterate_journal_list(self.DOI_SEARCH_MODE)
            doi_search_thread = threading.Thread(name='doi-search-worker', target=self.ui.doi_search_worker)
            # doi_search_thread.setDaemon(True)  #
            doi_search_thread.start()

        elif self.status == 'reality-check':
            self.recreate_journal_list()
            # self.iterate_journal_list(self.REALITY_CHECK_MODE)
            reality_check_thread = threading.Thread(name='doi-search-worker', target=self.ui.reality_check_worker)
            # reality_check_thread.setDaemon(True)  #
            reality_check_thread.start()

    def reset_member_variables(self):
        self.complete = 'True'
        self.status = '0'
        self.input_file_path = 'no-path'
        self.output_file_path = 'no-path'
        self.wrong_file_path = 'no-path'
        self.current_index = -1

    def create_journal_list(self):
        self.journal_list = csv_reader.construct_journal_list_from(self.input_file_path)

    def recreate_journal_list(self):
        self.journal_list = csv_reader.reconstruct_journal_list_from(self.input_file_path)

    def iterate_journal_list(self, mode):
        """
        Iterates a journal list
        :param mode: 'doi-search' or 'reality-check'
        :return:
        """
        #  prints start messages
        if mode == self.DOI_SEARCH_MODE:
            debug.d_print('===============DOI-SEARCH=================')
        if mode == self.REALITY_CHECK_MODE:
            debug.d_print('==============REALITY-CHECK===============')

        # updates email address
        config_utils.config.update_email(self.receiver)

        # retrieve index
        index = self.current_index

        # if there is no progress remaining
        if index == self.LAST_FINISHED:  # -1
            d = str(datetime.datetime.today())
            date = d[5:7] + d[8:10]
            # date = d[0:4] + d[5:7] + d[8:10] + '-' + d[11:13] + d[14:16]

            input_file_name = self.input_file_path.split('/')[-1][0:-4]
            print('filename: ', input_file_name)

            # decides names of the result files
            if mode == self.DOI_SEARCH_MODE:
                self.output_file_path = 'TEMP-DOI-' + date + '_from_' + input_file_name  # file name
                self.wrong_file_path = 'NO-DOI-' + date + '_from_' + input_file_name
                # self.output_file_path = date + '-TEMP-DOI'  # file name
                # self.wrong_file_path = date + '-NO-DOI'
            elif mode == self.REALITY_CHECK_MODE:
                self.output_file_path = 'RESULT-JOURNALS-' + date + '_from_' + input_file_name  # file name
                self.wrong_file_path = 'PROBLEM-JOURNALS-' + date + '_from_' + input_file_name
                # self.output_file_path = date + '-RESULT-JOURNALS'  # file name
                # self.wrong_file_path = date + '-PROBLEM-JOURNALS'

                # creates csv files for appending
            if mode == self.DOI_SEARCH_MODE:
                csv_reader.prepare_temp_csv(self.output_file_path)  # creates a csv temp file
            elif mode == self.REALITY_CHECK_MODE:
                csv_reader.prepare_result_csv(self.output_file_path)  # creates a csv temp file
            csv_reader.prepare_wrong_csv(self.wrong_file_path)

            index = 0
            config_utils.config.update_progress(self.input_file_path, self.output_file_path, self.wrong_file_path,
                                                status=mode, index=index, title=self.journal_list[index].title)

        #  Iterates a list of journals using index
        list_size = len(self.journal_list)
        while index < list_size:
            if self.ui is not None:
                self.ui.notify_progress(index + 1, list_size)

            debug.d_print(index + 1, ":", self.journal_list[index])
            title = self.journal_list[index].title

            #  doi-search or reality-check will be called
            if not self.journal_list[index].has_problem:
                if mode == self.DOI_SEARCH_MODE:
                    try:
                        self.search_article(self.journal_list[index])  # DOI Search
                    except KeyError:
                        self.journal_list[index].has_problem = True
                        self.journal_list[index].problem_detail = 'Unknown-DOI-Search-Error'
                    except json.decoder.JSONDecodeError:
                        self.journal_list[index].has_problem = True
                        self.journal_list[index].problem_detail = 'JSON-Decode-Error-DOI-Search'
                elif mode == self.REALITY_CHECK_MODE:
                    self.check_reality(self.journal_list[index])  # Reality Check

            # recording results into csv
            if not self.journal_list[index].has_problem:
                if mode == self.DOI_SEARCH_MODE:
                    csv_reader.append_doi_row(self.journal_list[index], self.output_file_path)
                elif mode == self.REALITY_CHECK_MODE:
                    csv_reader.append_journal_row(self.journal_list[index], self.output_file_path)
            else:
                if mode == self.DOI_SEARCH_MODE:
                    csv_reader.append_problem_doi_row(self.journal_list[index], self.output_file_path)
                elif mode == self.REALITY_CHECK_MODE:
                    csv_reader.append_problem_journal_row(self.journal_list[index], self.output_file_path)

            # recording problems into csv
            csv_reader.append_wrong_row(mode=mode, journal=self.journal_list[index],
                                        file_name=self.wrong_file_path)

            index = index + 1
            config_utils.config.update_progress(self.input_file_path, self.output_file_path, self.wrong_file_path,
                                                status=mode, index=index, title=title)

            #  prints progresses
            if not self.journal_list[index - 1].has_problem:
                debug.d_print(index, '/', list_size, 'finished\n')  # prints progress
            else:
                debug.d_print(index, '/', list_size, 'skipped\n')  # prints progress

        # the temp doi file is ready to be continued
        if mode == self.DOI_SEARCH_MODE:
            self.continue_output_file_path = 'Data-Files/Output-Files/' + self.output_file_path
            if csv_reader.has_entry(self.wrong_file_path):
                self.ui.wrong_file_path = self.wrong_file_path
                self.ui.set_no_doi_file_warning()

        # work is done. clear data
        config_utils.config.clear_progress()
        self.send_email(mode)
        self.reset_member_variables()

    def search_article(self, journal):
        """
        Fetching articles using crossref api.
        :param journal: a journal object
        :return:
        """
        for year in journal.year_dict:
            debug.d_print(journal.year_dict[year][self.BEGIN],  # start_date
                          journal.year_dict[year][self.END],  # end_date
                          )
            doi = searcher.search_journal(journal.title,
                                          journal.year_dict[year][self.BEGIN],  # start_date
                                          journal.year_dict[year][self.END],  # end_date
                                          journal.print_issn, journal.online_issn,
                                          journal.publisher)
            journal.year_dict[year][self.ARTICLE].doi = doi
            if doi is None:
                debug.d_print(doi)
            else:
                debug.d_print('https://doi.org/' + doi)

    def check_reality(self, journal):
        """
        Screen scrape and determine the journal reality.
        :param journal: a journal object
        :return:
        """
        debug.d_print(journal.title, journal.package)

        for year in journal.year_dict:
            article = journal.year_dict[year][self.ARTICLE]
            doi = article.doi
            print(doi)
            if doi is None:
                print('nodoi is executed')
                article.accessible = False
                article.result = 'No-DOI'
                journal.record_wrong_years()  # wrong years are updated
                journal.record_free_years()  # free years are updated
                return
            try:
                result = screenscraper.check_journal(doi, journal.package)  # reality check
            except Exception:
                debug.d_print(year)
                debug.d_print('|exception happened|')
                result = result_enum.Result.OtherException

            article.result = result  # result is stored in article
            if result is result_enum.Result.Access:
                article.accessible = True
            if result is result_enum.Result.OpenAccess:
                article.accessible = True
                article.open = True
            if result is result_enum.Result.FreeAccess:
                article.accessible = True
                article.free = True

            article.result = self.convert_result(result)  # result is checked
            debug.d_print(str(year), ':', str(result), '=', 'https://doi.org/' + str(doi))

        journal.record_wrong_years()  # wrong years are updated
        journal.record_free_years()  # free years are updated

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
        elif result == result_enum.Result.WrongWebsite:
            return 'Incorrect-Website'
        elif result == result_enum.Result.WebsiteNotAsExpected:
            return 'Website-Not-As-Expected'
        elif result == result_enum.Result.NetworkError:
            return 'Network-Error'
        elif result == result_enum.Result.PublisherNotFound:
            return 'Publisher-Not-Found'
        elif result == result_enum.Result.OtherException:
            return 'Other-Exception'
        else:
            return 'No-Result-Obtained'

    def send_email(self, mode):
        """
        Send the result file to a specified email address.
        :return:
        """

        use_server = True

        self.config = configparser.ConfigParser()
        self.config.read(config_utils.config.PATH_TO_SMTP_SERVER_INI)

        if use_server:
            #  Sender is a server
            emailer = email_server.EmailHandler(smtp_server=self.config['email-info']['smtp-server'],
                                                port=int(self.config['email-info']['port']),
                                                from_name=self.config['email-info']['from'],
                                                sender=self.config['email-info']['sender'],
                                                domain=self.config['email-info']['domain'],
                                                subject=self.config['email-info']['subject'],
                                                body=self.config['email-info']['body']
                                                )  # using a server name to send
        else:
            #  Sender is personal address
            emailer = email_handler.EmailHandler()
            emailer.set_sender(sender=self.sender, password=self.password)

        emailer.set_receiver(receiver=self.receiver)
        emailer.set_subject(subject=mode + ' finished')
        emailer.set_body(body='The ' + mode + ' has been finished. Two are files attached.\n\n')

        f1 = csv_reader.path + self.output_file_path + '.csv'
        f2 = csv_reader.path + self.wrong_file_path + '.csv'
        files = [f1, f2]

        try:
            emailer.send(files)
        except smtplib.SMTPRecipientsRefused:
            print('Email was incorrect')
        debug.d_print('email finished')

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
            if self.ui.is_new_receiver():
                self.receiver = self.ui.receiver
            self.iterate_journal_list(self.DOI_SEARCH_MODE)

        elif code == main_ui.MainUI.REALITY_CHECK_CLICKED:
            if self.ui.is_new_receiver():
                self.receiver = self.ui.receiver
            self.iterate_journal_list(self.REALITY_CHECK_MODE)


def main():
    main_system = MainSystem()
    debug.d_print('"PROGRAM TERMINATED"')


if __name__ == '__main__':
    main()
