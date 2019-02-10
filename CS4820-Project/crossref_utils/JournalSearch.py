#Program that gives sample DOI's from the correct
#journal for each year from start date to end date
#still a few indescrepencies
from crossref.restful import Works


class JournalSearch:

    def __init__(self, journal_title, journal_package_name, journal_url, journal_publisher, print_issn,
                                                        online_issn, start_date, end_date, start_month, end_month,
                                                        start_year, end_year):
        self.journal_title = journal_title
        self.journal_package_name = journal_package_name
        self.journal_url = journal_url
        self.journal_publisher = journal_publisher
        self.print_issn = print_issn
        self.online_issn = online_issn
        self.start_date = start_date
        self.end_date = end_date
        self.start_month = start_month
        self.end_month = end_month
        self.start_year = start_year
        self.end_year = end_year

    #function that searches 10 articles in journal for each year
    def search_journals(self):
        works = Works()
        doi_list = ['']

        #variable that creates string in correct format for year month and day
        start_ymd = str(self.start_year) + '-' + str(self.start_month) + '-' + str(self.start_date)
        end_ymd = str(self.end_year) + '-' + str(self.end_month) + '-' + str(self.end_date)

        #loop executes until all the DOI's are put into a list
        print("Journals for year: " + str(self.start_year))
        for i in works.query(self.journal_title).filter(has_funder='true', has_license='true',
                                                            issn=self.online_issn,
                                                            from_pub_date=start_ymd,
                                                            until_pub_date=end_ymd).sample(1).select('DOI'):
            print(str(i['DOI']))
            doi_list.append(i['DOI'])


def main():
    #paramaters have some filler values that aren't needed but there for prooject purposes
    #example used is Journal of Biosciences with correct ISSN
    searcher = JournalSearch('Journal of biosciences', 'Filler-Value', 'filler-value', 'filler-value',
                             'filler-value', '0973-7138', '01', 31, '01', 12, 2018, 2018)
    searcher.search_journals()


if __name__ == "__main__":
    main()

