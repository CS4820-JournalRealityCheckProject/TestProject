import tkinter as tk

import journal_ui.main_ui as main_ui


class MainSystem:

    journal_list = []

    def __init__(self):
        print("system turned on")
        self.start_ui()
        
    def start_ui(self):
        root = tk.Tk()
        app = main_ui.MainUI(master=root)
        app.mainloop()

    def read_csv_jourals(self):
        print('reading')




def main():
    main_system = MainSystem()


if __name__ == '__main__':
    main()



