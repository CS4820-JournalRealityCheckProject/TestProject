from tkinter import *
from tkinter import filedialog
import csv
import urllib2
import json
from crossref.restful import Works
from bs4 import BeautifulSoup as soup
from datetime import datetime

lines = 0


class JournalGui:

    def __init__(self, master):
        frame = Frame(master, width=1000, height=600)
        frame.pack()

        self.topFrame = Frame(master, width=500, height=500)
        self.midFrame = Frame(master, width=500, height=100)
        self.bottomFrame = Frame(master)
        self.firstLabel = Label(frame, text="Journal Reality Checking")

        self.contentField = Text(self.topFrame)
        self.readyLabel = Entry(self.midFrame)

        self.uploadButton = Button(self.bottomFrame, text="Browse File", command=self.uploadFile)
        self.searchButton = Button(self.bottomFrame, text="Search Articles", command=self.searchArticle)
        self.downloadButton = Button(self.bottomFrame, text="Download", command=self.printMessage)
        self.exitButton = Button(self.bottomFrame, text="Exit", command=frame.quit)

        self.readyLabel.pack()
        self.midFrame.pack()
        self.topFrame.pack()

        self.bottomFrame.pack()
        self.firstLabel.pack()

        self.contentField.pack()
        self.uploadButton.pack(side=LEFT)
        self.searchButton.pack(side=LEFT)
        self.downloadButton.pack(side=LEFT)
        self.exitButton.pack(side=RIGHT)


    def uploadFile(self):
        global lines
        global line
        global file_content
        file_name = filedialog.askopenfilename(initialdir="currdir", title="Select File",
                                               filetypes=(("csv files", "*.csv"),
                                                          ("all files", "*.*")))
        file_handle = open(file_name, 'r')
        print(file_name)
        self.searchReady()
        self.contentField.insert(END, file_name)
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, '\n')
        input_file = file_handle.readlines()
        file_content = csv.reader(input_file)
        # next(file_content) used to remove the header
        for index in range(3000):
            lines += 1
            line = next(file_content)
            print (line[0])
            print (lines)
        # for lines in file_content:
        #  print(lines[0], lines[1])
        self.contentField.insert(END, "File uploaded successfully", '\n')
        file_handle.close()
        print ("Close", file_handle.close())
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, '\n')

        data = []
        for row in file_content:
                #Title	PackageName	URL	Publisher	PrintISSN	OnlineISSN	ManagedCoverageBegin	ManagedCoverageEnd
            title = str(row[0])
            packageName = str(row[1])
            Url = str(row[2])
            publisher = str(row[3])
            printIssn = str(row[4])
            onlineIssn = str(row[5])
            coverageBegin = (row[6])
            coverageEnd = row[7]

            data.append([title, packageName, Url, publisher, printIssn, onlineIssn, coverageBegin, coverageEnd])

        for i in range(10):
            print data[i].__getitem__(0)


    # function for screen scrapping from Oxford
    '''
    bookTitle = "American Journal for Agricultural Economics"
    bookUrl = 'https://academic.oup.com/journals/search-results?' \
              'page=1&q=American%20Journal%20of%20Agricultural%20Economics&fl_SiteID=5567&' \
              'SearchSourceType=1&allJournals=1'
    myScrapUrl = bookUrl
    mySite = urllib2.urlopen(myScrapUrl)
    htmlPage = mySite.read()
    mySite.close()
    # Html parser
    pageSoup = soup(htmlPage, "html.parser")
    mySearch = pageSoup.findAll("div", {"class": "al-citation-list"})
    myLen = len(mySearch)
    for nums in range(myLen):
        firstDOI = mySearch[nums]
        myDOI = firstDOI.a["href"]
        myVolume = firstDOI.span.text
        # print "Result =", firstDOI
        print ("DOI: ", myDOI, "\n", "Volume: ", myVolume)
    '''


    def crossrefApi(self):
        work = Works()
        crossrefCount = work.count()
        journalAgency = work.agency('10.1111/j.1467-9353.2009.01461.x')
        publisherEl = work.doi('10.1111/j.1467-9353.2009.01461.x')
        pub = publisherEl['publisher']
        qcross = ("From crossref agency count", crossrefCount)
        xcross = ("Find agency ", journalAgency)
        ncross = ("Publisher of journal ", pub)
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, qcross)
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, xcross)
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, '\n')
        self.contentField.insert(END, ncross)


    @staticmethod
    def printMessage():
        print("Button works")


    def searchReady(self):
        self.readyLabel.insert(0, "File Ready")


    def searchModule(self):
        self.readyLabel.insert(0, "Connecting to  server.....")


    def searchArticle(self):
        self.crossrefApi()
        self.clear_entry()
        self.searchModule()

    def clear_entry(self):
        self.readyLabel.delete(0, 'end')


root = Tk()
root.title("Journal Reality Checking")
classObj = JournalGui(root)
root.mainloop()
