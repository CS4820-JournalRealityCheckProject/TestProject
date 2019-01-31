import tkinter as tk
from tkinter import filedialog
import journal_utils.csv_reader as csv_reader


class MainUI(tk.Frame):

    def __init__(self, master=None, main_upload=None, main_download=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.file_path = None
        self.create_widget(main_upload=main_upload, main_download=main_download)

    def create_widget(self, main_upload, main_download):
        self.top_frame = tk.Frame(self, width=500, height=500)
        self.mid_frame = tk.Frame(self, width=500, height=100)
        self.buttom_frame = tk.Frame(self)
        self.first_label = tk.Label(self, text="Journal Reality Checking")

        self.content_field = tk.Text(self.top_frame)
        self.ready_label = tk.Entry(self.mid_frame)

        self.upload_button = tk.Button(self.buttom_frame, text="Browse File", command=main_upload)
        self.search_button = tk.Button(self.buttom_frame, text="Search Articles", command=self.search_article)
        self.download_button = tk.Button(self.buttom_frame, text="Download", command=main_download)
        self.exit_button = tk.Button(self.buttom_frame, text="Exit", command=self.quit)

        self.ready_label.pack()
        self.mid_frame.pack()
        self.top_frame.pack()

        self.buttom_frame.pack()
        self.first_label.pack()

        self.content_field.pack()
        self.upload_button.pack(side=tk.LEFT)
        self.search_button.pack(side=tk.LEFT)
        self.download_button.pack(side=tk.LEFT)
        self.exit_button.pack(side=tk.RIGHT)

    def upload_file(self):
        file_path = filedialog.askopenfilename(initialdir="currdir", title="Select File",
                                               filetypes=(("csv files", "*.csv"),
                                                          ("all files", "*.*")))
        print(file_path)
        return file_path

    def search_article(self):
        print('search')

    def print_message(self):
        print('message')


if __name__ == '__main__':
    root = tk.Tk()
    app = MainUI(master=root)
    app.mainloop()
