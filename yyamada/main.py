# import journal_utils.Journal
from journal_utils.journal import Journal


class Main:

    journal_list = []

    def __init__(self):
        print("system turned on")
        self.journal = Journal(title='Japan Academic')
        print(self.journal.title)

    def read_csv_jourals(self):
        print('reading')


test = Main()
