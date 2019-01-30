import tkinter as tk
from tkinter import filedialog
import journal_utils.csv_reader as csv_reader


class MainUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widget()

    def create_widget(self):
        self.topFrame = tk.Frame(self, width=500, height=500)
        self.midFrame = tk.Frame(self, width=500, height=100)
        self.bottomFrame = tk.Frame(self)
        self.firstLabel = tk.Label(self, text="Journal Reality Checking")

        self.contentField = tk.Text(self.topFrame)
        self.readyLabel = tk.Entry(self.midFrame)

        self.uploadButton = tk.Button(self.bottomFrame, text="Browse File", command=self.uploadFile)
        self.searchButton = tk.Button(self.bottomFrame, text="Search Articles", command=self.searchArticle)
        self.downloadButton = tk.Button(self.bottomFrame, text="Download", command=self.printMessage)
        self.exitButton = tk.Button(self.bottomFrame, text="Exit", command=self.quit)

        self.readyLabel.pack()
        self.midFrame.pack()
        self.topFrame.pack()

        self.bottomFrame.pack()
        self.firstLabel.pack()

        self.contentField.pack()
        self.uploadButton.pack(side=tk.LEFT)
        self.searchButton.pack(side=tk.LEFT)
        self.downloadButton.pack(side=tk.LEFT)
        self.exitButton.pack(side=tk.RIGHT)

    def uploadFile(self):
        file_path = filedialog.askopenfilename(initialdir="currdir", title="Select File",
                                               filetypes=(("csv files", "*.csv"),
                                                          ("all files", "*.*")))
        print(file_path)
        csv_reader.read_csv_create_journal(file_path)
        return file_path

    def searchArticle(self):
        print('search')

    def printMessage(self):
        print('message')


root = tk.Tk()
app = MainUI(master=root)
app.mainloop()
