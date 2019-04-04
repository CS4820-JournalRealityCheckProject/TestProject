# Module method that gives sample DOI's from the correct
# journal from start date to end date
# still a few indescrepencies

from crossref.restful import Works


# function that searches an article in between given dates
def search_journal(journal_title, start_date, end_date, print_issn, online_issn, publisher):
    works = Works()
    received_doi = None

    # loop executes until all the DOI's are put into a list,
    # it is set up so if the online_issn doesn't return any DOI's then the method
    # will try again using the print_issn
    if print_issn == '' and online_issn == '':
        return 'Both ISSNs are empty'

    if online_issn != '':  # online ISSN exists
        for i in works.query(journal_title, publisher_name=publisher).filter(
                issn=online_issn,
                from_pub_date=start_date,
                until_pub_date=end_date).sample(1).select('DOI'):
            received_doi = i['DOI']

    if print_issn != '':  # print ISSN exists
        if received_doi is None:
            for j in works.query(journal_title, publisher_name=publisher).filter(
                    issn=print_issn,
                    from_pub_date=start_date,
                    until_pub_date=end_date).sample(1).select('DOI'):
                received_doi = j['DOI']

    return received_doi


if __name__ == '__main__':
    # doi = search_journal('Annals of Combinatorics', '1997-01-01', '2000-12-31', '0218-0006', '0219-3094')
    doi = search_journal('Social work in education', '1996-01-01', '2000-07-31', '0162-7961', '', )
    print(doi)
    title = 'Journal'
    w = Works()
    w.query(title).filter(1)
