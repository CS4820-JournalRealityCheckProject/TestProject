import tkinter as tk

import journal_ui.main_ui as main_ui
import journal_utils.csv_reader as csv_reader


class MainSystem:

    def __init__(self):
        print("system turned on")
        self.start_ui()
        self.journal_list = None
        self.file_path = None

    def start_ui(self):
        self.root = tk.Tk()
        self.app = main_ui.MainUI(master=self.root,
                                  main_upload=self.read_csv,
                                  main_download=self.download_csv)
        self.app.mainloop()

    def read_csv(self):
        self.file_path = self.app.upload_file()
        self.create_journal_list()
        print('reading function of main')

    def create_journal_list(self):
        self.journal_list = csv_reader.read_csv_create_journal(self.file_path)

    def download_csv(self):
        n = 0
        while not (n == -1):
            n = int(input('Enter an index:'))
            if self.journal_list is not None:
                print(self.journal_list[n])
        print('finished')

    def fetch_article(self, publisher, begin_date, end_date):
        print("crossref.fetch_article is called here")

    def check_reality(self, doi):
        print("journal reality check will be proceeded here")


def main():
    main_system = MainSystem()


if __name__ == '__main__':
    main()
