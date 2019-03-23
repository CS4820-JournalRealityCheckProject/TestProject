import tkinter as tk
import tkinter.ttk as ttk
import csv
from tkinter import filedialog
import journal_utils.csv_reader as csv_reader
import debug_utils.debug as debug


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

    # header column's format
    TEMP_CSV_HEADER = ['Title', 'Year', 'DOI', 'PackageName', 'URL', 'Publisher', 'PrintISSN',
                       'OnlineISSN', 'ManagedCoverageBegin', 'ManagedCoverageEnd']
    JOURNAL_CSV_HEADER = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN', 'OnlineISSN', 'ManagedCoverageBegin',
                          'ManagedCoverageEnd']
    JOURNAL_RESULT_CSV_HEADER = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN', 'OnlineISSN',
                                 'ManagedCoverageBegin',
                                 'ManagedCoverageEnd', 'AccessToAll', 'ProblemYears', 'FreeYears']
    STANDARD_HEADER = ['publication_title', 'print_identifier', 'online_identifier', 'date_first_issue_online',
                       'num_first_vol_online', 'num_first_issue_online', 'date_last_issue_online',
                       'num_last_vol_online',
                       'num_last_issue_online', 'title_url', 'first_author', 'title_id', 'embargo_info',
                       'coverage_depth',
                       'notes', 'publisher_name', 'publication_type', 'date_monograph_published_print',
                       'date_monograph_published_online', 'monograph_volume', 'monograph_edition', 'first_editor',
                       'parent_publication_title_id', 'preceding_publication_title_id', 'access_type', 'Subject(s)',
                       'Collection(s)', 'Year Started at OUP', 'MARC Control Number', 'Title History']
    OXFORD_HEADER = ['Title', 'ManagedCoverageBegin', 'ManagedCoverageEnd', 'PrintISSN', 'OnlineISSN', 'KBID',
                     'AlternateTitle', 'PackageName', 'URL', 'Publisher', 'Edition', 'Author', 'Editor', 'Illustrator',
                     'PrintISBN', 'OnlineISBN', 'DOI', 'PeerReviewed', 'CustomCoverageBegin', 'CustomCoverageEnd',
                     'CoverageStatement', 'Embargo', 'CustomEmbargo', 'Description', 'Subject', 'ResourceType',
                     'PackageContentType', 'CreateCustom', 'HideOnPublicationFinder', 'Delete', 'OrderedThroughEBSCO',
                     'IsCustom', 'UserDefinedField1', 'UserDefinedField2', 'UserDefinedField3', 'UserDefinedField4',
                     'UserDefinedField5', 'PackageType', 'AllowEbscoToAddNewTitles']

    # colors for email Entry
    COLOR_SAVED_EMAIL = 'lightcyan4'
    COLOR_NEW_EMAIL = 'black'

    def __init__(self, main_system, master=None):
        super().__init__(master)

        # master root
        self.master = master
        self.pack()

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
        self.rdo1 = tk.Radiobutton(tab1, value=self.PREVIOUS_EMAIL, variable=self.radio_var, text='Use Saved Email',
                                   command=self.radio_button_changed)
        self.rdo1.grid(row=7, column=2)

        self.rdo2 = tk.Radiobutton(tab1, value=self.NEW_EMAIL, variable=self.radio_var, text='Update Email',
                                   command=self.radio_button_changed)
        self.rdo2.grid(row=8, column=2)

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

        f_name = self.input_file_path.split('/')[-1]  # get only the name.csv
        debug.d_print(self.input_file_path)
        debug.d_print(f_name)
        self.file_var.set(f_name)
        self.file_name = f_name

        # checks if the uploaded file is valid
        with open(self.input_file_path, 'r', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # only for python 3
            debug.d_print('Columns:', header)

            if header == self.STANDARD_HEADER:
                self.mode = self.MODE_NOT_SET
                debug.d_print('*This is the standard format')

            elif header == self.OXFORD_HEADER:
                self.mode = self.MODE_NOT_SET
                debug.d_print('*This is the oxford format')

            elif header == self.JOURNAL_CSV_HEADER or header == self.JOURNAL_RESULT_CSV_HEADER:
                self.mode = self.DOI_SEARCH_MODE
                self.is_ready = True
                self.start_button.config(state="normal")
                self.top_message_var.set('DOI-SEARCH')
                self.warn_var.set('')
                debug.d_print('for journal')

            elif header == self.TEMP_CSV_HEADER:
                self.mode = self.REALITY_CHECK_MODE
                self.is_ready = True
                self.start_button.config(state="normal")
                self.top_message_var.set('REALITY CHECK')
                self.warn_var.set('')
                debug.d_print('for doi')

            else:
                self.mode = self.MODE_NOT_SET
                self.warn_var.set('Wrong file (wrong columns)')
                self.start_button.config(state="disabled")

        self.main_system.update(MainUI.FILE_UPLOADED)

    def search_article(self):
        self.main_system.update(MainUI.SEARCH_CLICKED)

    def check_reality(self):
        self.main_system.update(MainUI.REALITY_CHECK_CLICKED)

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

            self.search_article()  # the lines below are not executed if interrupted

            self.warn_var.set('DOI Search FINISHED')
            self.output_file_path = self.main_system.continue_output_file_path
            print(self.output_file_path)
            self.top_message_var.set('REALITY CHECK READY')
            self.warn_var.set(self.output_file_path)
            self.continue_button.config(state="normal")
            self.continue_button_var.set(self.continue_msg + self.output_file_path.split('/')[-1] + '.csv')

        elif self.mode == self.REALITY_CHECK_MODE:
            self.start_button.config(state="disabled")

            self.check_reality()  # the lines below are not executed if interrupted

            self.warn_var.set('Reality Check FINISHED')

    def email_entered(self, event=None):
        self.email_textfield.delete(0, tk.END)
        self.radio_var.set(self.NEW_EMAIL)

    def radio_button_changed(self, event=None):
        if self.radio_var.get() == self.PREVIOUS_EMAIL:
            self.temp_receiver = self.email_textfield.get()
            self.email_textfield.delete(0, tk.END)
            self.email_textfield.insert(tk.END, self.receiver)
            self.email_textfield.configure(fg=self.COLOR_SAVED_EMAIL)
        elif self.radio_var.get() == self.NEW_EMAIL:
            self.email_textfield.delete(0, tk.END)
            self.email_textfield.insert(tk.END, self.temp_receiver)
            self.email_textfield.configure(fg=self.COLOR_NEW_EMAIL)

    def is_new_receiver(self):
        if self.radio_var.get() == self.NEW_EMAIL:
            return True
        return False

    def continue_reality_check(self):
        self.mode = self.REALITY_CHECK_MODE
        self.input_file_path = self.output_file_path
        self.start()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainUI(master=root)
    app.mainloop()
