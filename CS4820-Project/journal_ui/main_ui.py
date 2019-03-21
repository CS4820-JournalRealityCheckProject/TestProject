import tkinter as tk
import tkinter.ttk as ttk
import csv
from tkinter import filedialog
import journal_utils.csv_reader as csv_reader


class MainUI(tk.Frame):
    """This class models a UI"""

    # class constants
    FILE_UPLOADED = 'FILE_UPLOADED'
    DOWNLOAD_CLICKED = 'DOWNLOAD_CLICKED'
    SEARCH_CLICKED = 'SEARCH_CLICKED'
    EMAIL_CLICKED = 'EMAIL_CLICKED'
    REALITY_CHECK_CLICKED = 'REALITY_CHECK_CLICKED'

    DOI_SEARCH_MODE = 0
    REALITY_CHECK_MODE = 1

    DOI_CSV_HEADER = ['Title', 'Year', 'DOI', 'DOI-URL', 'Accessible', 'PackageName', 'URL', 'Publisher', 'PrintISSN',
                      'OnlineISSN', 'ManagedCoverageBegin', 'ManagedCoverageEnd', 'AsExpected', 'ProblemYears',
                      'FreeYears']
    JOURNAL_CSV_HEADER = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN', 'OnlineISSN', 'ManagedCoverageBegin',
                          'ManagedCoverageEnd']

    JOURNAL_RESULT_CSV_HEADER = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN', 'OnlineISSN',
                                 'ManagedCoverageBegin',
                                 'ManagedCoverageEnd', 'AsExpected', 'ProblemYears', 'FreeYears']

    def __init__(self, main_system, master=None):
        super().__init__(master)

        # master root
        self.master = master
        self.pack()

        # member variables
        self.main_system = main_system
        self.file_path = None
        self.input_file_path = None
        self.mode = 'doi-search'
        self.is_ready = False
        self.receiver = None

        # notebook (tab windows)
        nb = ttk.Notebook(width=200, height=200)

        # make tab windows (Frames)
        tab1 = tk.Frame(nb)
        tab2 = tk.Frame(nb)
        nb.add(tab1, text='System', padding=3)
        #nb.add(tab2, text='', padding=3)
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
        self.email_textfield = tk.Text(tab1, bd=1, bg='light grey', height=1, width=40)
        self.email_textfield.grid(row=4, column=2)

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

    def upload_file(self):
        """
        Allows a user to browse a csv file and upload it.
        :return:
        """
        self.input_file_path = filedialog.askopenfilename(initialdir="currdir", title="Select File",
                                                          filetypes=(("csv files", "*.csv"),
                                                                     ("all files", "*.*")))
        print(self.input_file_path)

        res2 = self.input_file_path.split('/')[-1]
        print(res2)
        self.file_var.set(res2)
        with open(self.input_file_path, 'r', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # only for python 3
            print(header)
            print(self.JOURNAL_CSV_HEADER)
            if header == self.JOURNAL_CSV_HEADER or header == self.JOURNAL_RESULT_CSV_HEADER:
                print('for journal')
                self.mode = self.DOI_SEARCH_MODE
                self.is_ready = True
                self.start_button.config(state="normal")
                self.top_message_var.set('"DOI-SEARCH"')
                self.warn_var.set('')

            elif header == self.DOI_CSV_HEADER:
                print('for doi')
                self.mode = self.REALITY_CHECK_MODE
                self.is_ready = True
                self.start_button.config(state="normal")
                self.top_message_var.set('"REALITY CHECK"')
                self.warn_var.set('')

            else:
                self.warn_var.set('Wrong file (wrong columns)')
                self.start_button.config(state="disabled")

        self.main_system.update(MainUI.FILE_UPLOADED)

    def search_article(self):
        self.main_system.update(MainUI.SEARCH_CLICKED)

    def check_reality(self):
        self.main_system.update(MainUI.REALITY_CHECK_CLICKED)

    def start(self):

        if self.email_textfield.get('1.0', 'end -1c') == '':
            print('email did not match')
            self.warn_var.set('Email is incorrect')
            return
        else:
            self.receiver = self.email_textfield.get('1.0', 'end -1c')
            print(self.receiver)

        if self.mode == self.DOI_SEARCH_MODE:
            self.start_button.config(state="disabled")
            self.search_article()
            self.warn_var.set('FINISHED')

        elif self.mode == self.REALITY_CHECK_MODE:
            self.start_button.config(state="disabled")
            self.check_reality()
            self.warn_var.set('FINISHED')


if __name__ == '__main__':
    root = tk.Tk()
    app = MainUI(master=root)
    app.mainloop()
