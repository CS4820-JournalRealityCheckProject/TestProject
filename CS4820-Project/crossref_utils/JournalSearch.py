#Program that gives sample DOI's from the correct
#journal for each year from start year to end year
#still a few indescrepencies

from crossref.restful import Works


class JournalSearch:

    def __init__(self, journal_title, journal_package_name, journal_url, journal_publisher, print_issn, online_issn, start_year, end_year):
        self.journal_title = journal_title
        self.journal_package_name = journal_package_name
        self.journal_url = journal_url
        self.journal_publisher = journal_publisher
        self.print_issn = print_issn
        self.online_issn = online_issn
        self.start_year = start_year
        self.end_year = end_year

    #function that searches 10 articles in journal for each year
    def search_journals(self):
        works = Works()
        doi_list = ['']

        #loop executes until start year reaches the end year also puts results into a list
        while self.start_year <= self.end_year:
            print("Journals for year: " + str(self.start_year))
            for i in works.query(self.journal_title).filter(has_funder='true', has_license='true',
                                                            issn=self.online_issn,
                                                            from_pub_date=str(self.start_year) + '-01-01',
                                                            until_pub_date=str(self.start_year) + '-12-31').sample(10).select('DOI, prefix'):
                print(str(i))
                doi_list.append(i)

            self.start_year += 1


def main():
    #paramaters have some filler values that aren't needed but there for prooject purposes
    #example used is Journal of Biosciences with correct ISSN
    searcher = JournalSearch('Journal of biosciences', 'Filler-Value', 'filler-value', 'filler-value',
                             'filler-value', '0973-7138', 2016, 2018)
    searcher.search_journals()


if __name__ == "__main__":
    main()


