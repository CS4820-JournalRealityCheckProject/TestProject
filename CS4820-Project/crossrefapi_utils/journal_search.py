# Module method that gives sample DOI's from the correct
# journal from start date to end date
# still a few indescrepencies

from crossref.restful import Works


# function that searches an article in between given dates
def search_doi(journal_title, start_date, end_date, print_issn, online_issn, count):
    """
    A defined number of doi are put into a list
    If no doi are found using the online issn, the print issn

    :param journal_title: The title of the journal
    :param start_date: The start date in the format yyyy-mm-dd
    :param end_date: The end date in the format yyyy-mm-dd
    :param print_issn: The International Standard Serial Number for the print journal
    :param online_issn: The International Standard Serial Number for the online journal
    :param count: How many doi the method should try to find
    :return: A list of doi, this can be empty, but should be no larger than count
    """
    works = Works()
    received_doi = []

    if print_issn == '' and online_issn == '':
        return 'Both ISSNs are empty'

    if online_issn != '':  # online ISSN exists
        for i in works.query(journal_title).filter(
                issn=online_issn,
                from_pub_date=start_date,
                until_pub_date=end_date).sample(count).select('DOI'):
            received_doi.append(i['DOI'])

    if print_issn != '':  # print ISSN exists
        if not received_doi:
            for j in works.query(journal_title).filter(
                    issn=print_issn,
                    from_pub_date=start_date,
                    until_pub_date=end_date).sample(count).select('DOI'):
                received_doi.append(j['DOI'])

    return received_doi
