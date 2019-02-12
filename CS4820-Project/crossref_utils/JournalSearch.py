#Module method that gives sample DOI's from the correct
#journal from start date to end date
#still a few indescrepencies
from crossref.restful import Works


#function that searches an article in between given dates
def search_journal(journal_title, start_date, end_date, print_issn, online_issn):
        works = Works()
        received_doi = None

        #loop executes until all the DOI's are put into a list,
        #it is set up so if the online_issn doesn't return any DOI's then the method
        #will try again using the print_issn
        for i in works.query(journal_title).filter(has_funder='true', has_license='true',
                                                            issn=online_issn,
                                                            from_pub_date=start_date,
                                                            until_pub_date=end_date).sample(1).select('DOI'):
            received_doi = i['DOI']

        if received_doi is None:
            for j in works.query(journal_title).filter(has_funder='true', has_license='true',
                                                           issn=print_issn,
                                                           from_pub_date=start_date,
                                                           until_pub_date=end_date).sample(1).select('DOI'):
                received_doi = j['DOI']

        return received_doi


