import tkinter as tk
import tkinter.ttk as ttk
import csv
import logging
import threading
import os

from tkinter import filedialog

import debug_utils.debug as debug

# logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
BASE_PATH = os.path.dirname(os.path.dirname(__file__))


class MainUI(tk.Frame):
    """This class models a UI"""

    # class constants
    FILE_UPLOADED = 'FILE_UPLOADED'
    DOWNLOAD_CLICKED = 'DOWNLOAD_CLICKED'
    SEARCH_CLICKED = 'SEARCH_CLICKED'
    EMAIL_CLICKED = 'EMAIL_CLICKED'
    REALITY_CHECK_CLICKED = 'REALITY_CHECK_CLICKED'

    # system modes
    DOI_SEARCH_MODE = 0
    REALITY_CHECK_MODE = 1
    MODE_NOT_SET = -1

    # checks if update an email
    PREVIOUS_EMAIL = 0
    NEW_EMAIL = 1

    # strings
    NO_DOI_MSG = '!Caution! Check NO-DOI file.'
    no_doi_file_warning = False

    # header column's format
    TEMP_CSV_HEADER = ['Title', 'Year', 'DOI', 'PackageName', 'URL', 'Publisher', 'PrintISSN',
                       'OnlineISSN', 'ManagedCoverageBegin', 'ManagedCoverageEnd']
    JOURNAL_CSV_HEADER = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN', 'OnlineISSN', 'ManagedCoverageBegin',
                          'ManagedCoverageEnd']
    JOURNAL_RESULT_CSV_HEADER = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN', 'OnlineISSN',
                                 'ManagedCoverageBegin',
                                 'ManagedCoverageEnd', 'AccessToAll', 'ProblemYears', 'FreeYears']
    OXFORD_HEADER = ['Title', 'ManagedCoverageBegin', 'ManagedCoverageEnd', 'PrintISSN', 'OnlineISSN', 'KBID',
                     'AlternateTitle', 'PackageName', 'URL', 'Publisher', 'Edition', 'Author', 'Editor', 'Illustrator',
                     'PrintISBN', 'OnlineISBN', 'DOI', 'PeerReviewed', 'CustomCoverageBegin', 'CustomCoverageEnd',
                     'CoverageStatement', 'Embargo', 'CustomEmbargo', 'Description', 'Subject', 'ResourceType',
                     'PackageContentType', 'CreateCustom', 'HideOnPublicationFinder', 'Delete', 'OrderedThroughEBSCO',
                     'IsCustom', 'UserDefinedField1', 'UserDefinedField2', 'UserDefinedField3', 'UserDefinedField4',
                     'UserDefinedField5', 'PackageType', 'AllowEbscoToAddNewTitles']
    KBART_HEADER = ['publication_title', 'print_identifier', 'online_identifier', 'date_first_issue_online',
                    'num_first_vol_online', 'num_first_issue_online', 'date_last_issue_online',
                    'num_last_vol_online',
                    'num_last_issue_online', 'title_url', 'first_author', 'title_id', 'embargo_info',
                    'coverage_depth',
                    'notes', 'publisher_name', 'publication_type', 'date_monograph_published_print',
                    'date_monograph_published_online', 'monograph_volume', 'monograph_edition', 'first_editor',
                    'parent_publication_title_id', 'preceding_publication_title_id', 'access_type', 'Subject(s)',
                    'Collection(s)', 'Year Started at OUP', 'MARC Control Number', 'Title History']

    # colors for email Entry
    COLOR_SAVED_EMAIL = 'lightcyan4'
    COLOR_NEW_EMAIL = 'black'

    def __init__(self, main_system, master=None):
        super().__init__(master)

        # master root
        self.master = master
        self.pack()

        # threads
        self.doi_search_thread = None
        self.reality_check_thread = None

        # member variables
        self.main_system = main_system
        self.input_file_path = None
        self.output_file_path = None
        self.file_name = None
        self.mode = self.MODE_NOT_SET
        self.is_ready = False
        self.receiver = self.main_system.receiver
        self.temp_receiver = ''

        # notebook (tab windows)
        nb = ttk.Notebook(width=200, height=200)

        # make tab windows (Frames)
        tab1 = tk.Frame(nb)
        tab2 = tk.Frame(nb)
        nb.add(tab1, text='System', padding=3)
        # nb.add(tab2, text='', padding=3)

        nb.pack(expand=1, fill='both')

        # top label left
        self.top_label = tk.Label(tab1, text='Status: ')
        self.top_label.grid(row=0, column=1)

        # top message label
        self.top_message_var = tk.StringVar()
        self.top_message_var.set('Upload a file')
        self.top_message = tk.Label(tab1, textvariable=self.top_message_var, font='Helvetica 18 bold')
        self.top_message.grid(row=0, column=2)

        # empty field to allow space
        self.empty_field = tk.StringVar()
        self.empty_field.set("")
        self.empty_field = tk.Label(tab1)
        self.empty_field.grid(row=1, column=1)
        self.empty_field.grid(row=1, column=2)

        # upload button
        self.upload_button = tk.Button(tab1, text="Browse", command=self.upload_file)
        self.upload_button.grid(row=2, column=1)

        # csv file label
        self.file_var = tk.StringVar()
        self.file_var.set("no file")
        self.file_label = tk.Label(tab1, textvariable=self.file_var, bg='light grey', height=1, width=30)
        self.file_label.grid(row=2, column=2)

        # empty field to allow space
        self.empty_field = tk.StringVar()
        self.empty_field.set("")
        self.empty_field = tk.Label(tab1)
        self.empty_field.grid(row=3, column=1)
        self.empty_field.grid(row=3, column=2)

        # email label
        self.email_label = tk.Label(tab1, text='Email:')
        self.email_label.grid(row=4, column=1)

        # email textfield
        self.email_textfield = tk.Entry(tab1, bd=1, bg='light grey', fg=self.COLOR_SAVED_EMAIL)
        self.email_textfield.grid(row=4, column=2)
        self.email_textfield.insert(tk.END, self.receiver)
        self.email_textfield.bind("<FocusIn>", self.email_entered)
        self.email_textfield.config(state='disabled')

        # warning message label
        self.warn_var = tk.StringVar()
        self.warn_var.set("")
        self.warn_label = tk.Label(tab1, textvariable=self.warn_var, fg='red')
        self.warn_label.grid(row=5, column=2)

        # start button
        self.start_button = tk.Button(tab1, text="START", state='disabled', command=self.start)
        self.start_button.grid(row=6, column=1)

        # exit button
        self.exit_button = tk.Button(tab1, text="Exit", command=self.quit)
        self.exit_button.grid(row=6, column=3)

        # radio button for new or existing email
        self.radio_var = tk.IntVar()
        self.radio_var.set(self.PREVIOUS_EMAIL)

        # radio buttons
        self.previous_email_radio_btn = tk.Radiobutton(tab1, value=self.PREVIOUS_EMAIL, variable=self.radio_var,
                                                       text='Use Saved Email',
                                                       command=self.saved_email_clicked)
        self.previous_email_radio_btn.grid(row=7, column=2)

        self.new_email_radio_btn = tk.Radiobutton(tab1, value=self.NEW_EMAIL, variable=self.radio_var,
                                                  text='Update Email',
                                                  command=self.new_email_clicked)
        self.new_email_radio_btn.grid(row=8, column=2)
        self.disable_email_widgets()  # disable radio buttons

        # continue button
        self.continue_msg = 'Continue with '
        self.continue_button_var = tk.StringVar()
        self.continue_button_var.set(self.continue_msg + 'produced DOI file')
        self.continue_button = tk.Button(tab1, textvariable=self.continue_button_var,
                                         command=self.continue_reality_check, state='disabled')
        self.continue_button.grid(row=9, column=2)

    def upload_file(self):
        """
        Allows a user to browse a csv file and upload it.
        :return:
        """
        self.input_file_path = filedialog.askopenfilename(initialdir="currdir", title="Select File",
                                                          filetypes=(("csv files", "*.csv"),
                                                                     ("all files", "*.*")))
        if self.input_file_path == '':
            print('File select canceled.')
            self.disable_start_button()
            self.disable_email_widgets()
            self.file_var.set('no file')
            return

        f_name = self.input_file_path.split('/')[-1]  # get only the name.csv
        debug.d_print(self.input_file_path)
        debug.d_print(f_name)
        self.file_var.set(f_name)
        self.file_name = f_name

        self.continue_button.configure(state='disabled')  # continue button disabled

        # checks if the uploaded file is valid
        with open(self.input_file_path, 'r', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # only for python 3
            debug.d_print('Columns:', header)

            if header == self.KBART_HEADER:
                self.mode = self.MODE_NOT_SET
                debug.d_print('*This is the standard format')

            elif header == self.JOURNAL_CSV_HEADER or header == self.JOURNAL_RESULT_CSV_HEADER \
                    or header == self.OXFORD_HEADER:
                self.mode = self.DOI_SEARCH_MODE
                self.is_ready = True
                self.start_button.config(state="normal")
                self.top_message_var.set('DOI-SEARCH')
                self.warn_var.set('')
                debug.d_print('for journal')
                self.enable_email_widgets()

            elif header == self.TEMP_CSV_HEADER:
                self.mode = self.REALITY_CHECK_MODE
                self.is_ready = True
                self.start_button.config(state="normal")
                self.top_message_var.set('REALITY CHECK')
                self.warn_var.set('')
                debug.d_print('for doi')
                self.enable_email_widgets()

            else:
                self.mode = self.MODE_NOT_SET
                self.warn_var.set('Wrong file (wrong columns)')
                self.start_button.config(state="disabled")

        self.main_system.update(MainUI.FILE_UPLOADED)

    def start(self):

        if self.email_textfield.get() == '' and \
                self.radio_var.get() == self.NEW_EMAIL:
            self.warn_var.set('Enter an email')
            return
        else:
            self.receiver = self.email_textfield.get()
            debug.d_print(self.receiver)

        if self.mode == self.DOI_SEARCH_MODE:
            self.start_button.config(state="disabled")

            # starts a thread
            self.doi_search_thread = threading.Thread(name='doi-search-worker', target=self.doi_search_worker)
            # self.doi_search_thread.setDaemon(True)
            self.doi_search_thread.start()
            self.disable_all_buttons()
            self.warn_var.set('Started')

        elif self.mode == self.REALITY_CHECK_MODE:
            self.start_button.config(state="disabled")

            # starts a thread
            self.reality_check_thread = threading.Thread(name='reality-check-worker', target=self.reality_check_worker)
            # self.reality_check_thread.setDaemon(True)
            self.reality_check_thread.start()
            self.disable_all_buttons()
            self.warn_var.set('Started')

    def email_entered(self, event=None):
        self.email_textfield.delete(0, tk.END)
        self.radio_var.set(self.NEW_EMAIL)

    def saved_email_clicked(self):
        self.temp_receiver = self.email_textfield.get()
        self.email_textfield.delete(0, tk.END)
        self.email_textfield.insert(tk.END, self.receiver)
        self.email_textfield.configure(fg=self.COLOR_SAVED_EMAIL)
        self.email_textfield.config(state='disabled')

    def new_email_clicked(self):
        self.email_textfield.delete(0, tk.END)
        self.email_textfield.insert(tk.END, self.temp_receiver)
        self.email_textfield.configure(fg=self.COLOR_NEW_EMAIL)
        self.email_textfield.config(state='normal')

    def is_new_receiver(self):
        if self.radio_var.get() == self.NEW_EMAIL:
            return True
        return False

    def continue_reality_check(self):
        self.mode = self.REALITY_CHECK_MODE
        self.input_file_path = BASE_PATH + '/' + self.output_file_path + '.csv'
        self.main_system.input_file_path = self.input_file_path
        self.main_system.update(MainUI.FILE_UPLOADED)  # Reload the created file
        self.start()

    def doi_search_worker(self):
        logging.debug('doi-search thread started')
        self.search_article()

        # after doi search is done
        self.warn_var.set('DOI Search FINISHED')
        self.output_file_path = self.main_system.continue_output_file_path
        print(self.output_file_path)
        self.top_message_var.set('REALITY CHECK READY')
        if self.no_doi_file_warning:
            self.warn_var.set(self.NO_DOI_MSG + '\n' +
                              'RESULT:' + self.output_file_path)
        else:
            self.warn_var.set('RESULT:' + self.output_file_path)
        self.continue_button.config(state="normal")
        self.continue_button_var.set(self.continue_msg + self.output_file_path.split('/')[-1] + '.csv')
        self.enable_initial_buttons()

    def reality_check_worker(self):
        logging.debug('reality-check thread started')
        self.check_reality()

        # after reality check is done
        self.warn_var.set('Reality Check FINISHED')
        self.enable_initial_buttons()
        self.disable_email_widgets()

    def search_article(self):
        self.main_system.update(MainUI.SEARCH_CLICKED)

    def check_reality(self):
        self.main_system.update(MainUI.REALITY_CHECK_CLICKED)

    def notify_progress(self, numerator, denominator):
        self.warn_var.set('Progress: ' + str(numerator) + ' / ' + str(denominator))

    def disable_all_buttons(self):
        self.start_button.configure(state='disabled')
        self.upload_button.configure(state='disabled')
        self.exit_button.configure(state='disabled')
        self.continue_button.configure(state='disabled')
        self.previous_email_radio_btn.configure(state='disabled')
        self.new_email_radio_btn.configure(state='disabled')

    def enable_initial_buttons(self):
        self.upload_button.configure(state='normal')
        self.exit_button.configure(state='normal')
        self.previous_email_radio_btn.configure(state='normal')
        self.new_email_radio_btn.configure(state='normal')

    def disable_email_widgets(self):
        self.email_textfield.config(state='disabled')
        self.previous_email_radio_btn.configure(state='disabled')
        self.new_email_radio_btn.configure(state='disabled')

    def enable_email_widgets(self):
        self.email_textfield.config(state='normal')
        self.previous_email_radio_btn.configure(state='normal')
        self.new_email_radio_btn.configure(state='normal')

    def disable_start_button(self):
        self.start_button.config(state='disabled')

    def restore_ui(self, status):
        self.disable_all_buttons()

        # restore member variables
        self.input_file_path = self.main_system.input_file_path
        self.output_file_path = self.main_system.output_file_path
        self.file_name = self.output_file_path.split('/')[-1] + '.csv'
        if status == self.main_system.DOI_SEARCH_MODE:
            self.mode = self.DOI_SEARCH_MODE
        if status == self.main_system.REALITY_CHECK_MODE:
            self.mode = self.REALITY_CHECK_MODE
        self.is_ready = False
        self.receiver = self.main_system.receiver
        self.temp_receiver = ''

    def reset_member_variables(self):
        # threads
        self.doi_search_thread = None
        self.reality_check_thread = None

        # member variables
        self.input_file_path = None
        self.output_file_path = None
        self.file_name = None
        self.mode = self.MODE_NOT_SET
        self.is_ready = False
        # self.receiver = self.main_system.receiver
        self.temp_receiver = ''

    def set_no_doi_file_warning(self):
        self.no_doi_file_warning = True


if __name__ == '__main__':
    print('ui')
