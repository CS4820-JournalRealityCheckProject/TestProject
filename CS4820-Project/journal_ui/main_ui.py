import tkinter as tk
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

        # upload button
        self.upload_button = tk.Button(self, text="Browse", command=self.upload_file)
        self.upload_button.grid(row=1, column=1)

        # csv file label
        self.file_var = tk.StringVar()
        self.file_var.set("no file")
        self.file_label = tk.Label(self, textvariable=self.file_var, bg='cyan2', height=1, width=30)
        self.file_label.grid(row=1, column=2)

        # email label
        self.email_label = tk.Label(self, text='Email:')
        self.email_label.grid(row=2, column=1)

        # email textfield
        self.email_textfield = tk.Text(self, bd=1, bg='yellow', height=1, width=40)
        self.email_textfield.grid(row=2, column=2)

        # search button
        self.search_button = tk.Button(self, text="DOI Search", command=self.search_article)
        self.search_button.grid(row=3, column=1)

        # download button
        self.download_button = tk.Button(self, text="Download", command=self.download_file)
        self.download_button.grid(row=3, column=2)

        # exit button
        self.exit_button = tk.Button(self, text="Exit", command=self.quit)
        self.exit_button.grid(row=3, column=3)

        # email button
        self.email_button = tk.Button(self, text='Send', command=self.send_email)
        self.email_button.grid(row=4, column=2)

        # reality check button
        self.reality_check_button = tk.Button(self, text='Reality Check', command=self.check_reality)
        self.reality_check_button.grid(row=4, column=1)


        # radio buttons

        self.radio_var = tk.IntVar()
        self.radio_var.set(self.DOI_SEARCH_MODE)

        self.radio_search_doi = tk.Radiobutton(self, value=self.DOI_SEARCH_MODE, variable=self.radio_var,
                                               text='DOI Search')
        self.radio_reality_check = tk.Radiobutton(self, value=self.REALITY_CHECK_MODE, variable=self.radio_var,
                                                  text='Reality Check')

        self.radio_search_doi.grid(row=5, column=1)
        self.radio_reality_check.grid(row=5, column=2)

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
        self.mode = self.radio_var.get()
        print(self.mode)
        self.main_system.update(MainUI.FILE_UPLOADED)

    def download_file(self):
        self.main_system.update(MainUI.DOWNLOAD_CLICKED)

    def search_article(self):
        self.main_system.update(MainUI.SEARCH_CLICKED)

    def send_email(self):
        self.main_system.update(MainUI.EMAIL_CLICKED)

    def check_reality(self):
        self.main_system.update(MainUI.REALITY_CHECK_CLICKED)

    def print_message(self):
        print('message')


if __name__ == '__main__':
    root = tk.Tk()
    app = MainUI(master=root)
    app.mainloop()
