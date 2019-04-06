import csv
import os

from journal_utils.journal import Journal

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
path = BASE_PATH + '/Data-Files/Output-Files/'
exception_path = BASE_PATH + '/Data-Files/Exceptions/'
ARTICLE = 2
FAILED = 'failed'


def construct_journal_list_from(journals_csv):
    journal_obj_list = []

    with open(journals_csv, 'r', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not empty_row(row):
                journal_obj_list.append(
                    Journal(row['Title'],
                            row['PackageName'],
                            row['URL'],
                            row['Publisher'],
                            row['PrintISSN'],
                            row['OnlineISSN'],
                            row['ManagedCoverageBegin'],
                            row['ManagedCoverageEnd']
                            ))
    return journal_obj_list


def empty_row(row):
    if row['Title'] == row['PackageName'] == row['URL'] == row['Publisher'] == row['PrintISSN'] == \
            row['OnlineISSN'] == row['ManagedCoverageBegin'] == row['ManagedCoverageEnd'] == '':
        return True
    return False


def reconstruct_journal_list_from(articles_csv):
    """
    Reconstruct journal objects from the temporary article csv file
    :param articles_csv:
    :return:
    """
    journal_obj_list = []
    current_title = ''
    current_platform = ''

    with open(articles_csv, 'r', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)
        journal = None
        for row in reader:
            if row['Year'] == FAILED:
                year = row['Year']
            else:
                year = int(row['Year'])

            if row['DOI'] == '':
                doi = None
            else:
                doi = row['DOI']

            #  When we hit a next journal
            if current_title != row['Title'] or current_platform != row['PackageName']:
                current_title = row['Title']
                current_platform = row['PackageName']

                journal = Journal(row['Title'],
                                  row['PackageName'],
                                  row['URL'],
                                  row['Publisher'],
                                  row['PrintISSN'],
                                  row['OnlineISSN'],
                                  row['ManagedCoverageBegin'],
                                  row['ManagedCoverageEnd']
                                  )

                # If a journal has an issue
                if year == FAILED:  # 'failed':
                    problem_detail = row['DOI']
                    journal.set_problem(problem_detail)
                    journal_obj_list.append(journal)
                else:
                    journal.year_dict[year][ARTICLE].doi = doi
                    journal_obj_list.append(journal)

            # We are still adding an article to the journal
            else:
                journal.year_dict[year][ARTICLE].doi = doi

    print('size' + str(len(journal_obj_list)))
    return journal_obj_list


def prepare_temp_csv(temp_file='doi-articles'):
    with open(path + temp_file + '.csv', 'w', encoding='utf8', newline='') as csv_file:
        fieldnames = ['Title',

                      'Year',
                      'DOI',

                      'PackageName',
                      'URL',
                      'Publisher',
                      'PrintISSN',
                      'OnlineISSN',
                      'ManagedCoverageBegin',
                      'ManagedCoverageEnd',
                      ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        print('write header is executed')


def prepare_result_csv(result_file='result-journals'):
    print("result file")
    with open(path + result_file + '.csv', 'w', encoding='utf8', newline='') as csv_file:
        fieldnames = ['Title',
                      'PackageName',
                      'URL',
                      'Publisher',
                      'PrintISSN',
                      'OnlineISSN',
                      'ManagedCoverageBegin',
                      'ManagedCoverageEnd',
                      'AccessToAll',
                      'ProblemYears',
                      'FreeYears'
                      ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def prepare_wrong_csv(wrong_file='wrong-list'):
    with open(path + wrong_file + '.csv', 'w', encoding='utf8', newline='') as csv_file:
        fieldnames = ['Title',
                      'Year',
                      'Result',
                      'DOI',
                      'DOI-URL',
                      'PackageName',
                      'URL',
                      'Publisher',
                      ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def prepare_exception_csv(exception_file='wrong-list'):
    with open(exception_path + exception_file + '.csv', 'w', encoding='utf8', newline='') as csv_file:
        fieldnames = ['Title',
                      'Year',
                      'DOI',
                      'DOI-URL',
                      'PackageName',
                      'URL',
                      'Publisher',
                      'exception',
                      'exceptionArguments',
                      'stackTrace'
                      ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def append_doi_row(journal, file_name='doi-articles'):
    with open(path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        for year in journal.year_dict:
            writer.writerow([journal.title,
                             year,
                             journal.year_dict[year][ARTICLE].doi,
                             journal.package,
                             journal.url,
                             journal.publisher,
                             journal.print_issn,
                             journal.online_issn,
                             journal.expected_subscription_begin,
                             journal.expected_subscription_end,
                             ])


def append_problem_doi_row(journal, file_name='doi-articles'):
    with open(path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([journal.title,
                         FAILED,  # 'failed'
                         journal.problem_detail,
                         journal.package,
                         journal.url,
                         journal.publisher,
                         journal.print_issn,
                         journal.online_issn,
                         journal.expected_subscription_begin,
                         journal.expected_subscription_end,
                         ])


def append_journal_row(journal, file_name='result-journals'):
    with open(path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([journal.title,
                         journal.package,
                         journal.url,
                         journal.publisher,
                         journal.print_issn,
                         journal.online_issn,
                         journal.expected_subscription_begin,
                         journal.expected_subscription_end,
                         journal.access_to_all,
                         journal.wrong_years,
                         journal.free_years
                         ])


def append_problem_journal_row(journal, file_name='result-journals'):
    with open(path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([journal.title,
                         journal.package,
                         journal.url,
                         journal.publisher,
                         journal.print_issn,
                         journal.online_issn,
                         journal.expected_subscription_begin,
                         journal.expected_subscription_end,
                         'Failed',
                         'Bad-Original',
                         '???'
                         ])


def append_wrong_row(mode, journal, file_name='wrong-list'):
    """

    :param mode: 'doi-search' or 'reality-check'
    :param journal:
    :param file_name:
    :return:
    """
    with open(path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)

        if journal.has_problem:
            if mode == 'doi-search' or mode == 'reality-check':
                writer.writerow([journal.title,
                                 'failed',
                                 journal.problem_detail,
                                 '',
                                 '',
                                 journal.package,
                                 journal.url,
                                 journal.publisher,
                                 ])
            return

        for year in journal.year_dict:
            article = journal.year_dict[year][ARTICLE]

            if mode == 'doi-search' and article.doi is None:
                writer.writerow([journal.title,
                                 year,
                                 article.result,
                                 'No-DOI',
                                 '',
                                 journal.package,
                                 journal.url,
                                 journal.publisher,
                                 ])

            if mode == 'reality-check' and not article.accessible:
                # doi_url = None
                if article.doi is None:
                    doi_url = ''
                else:
                    doi_url = 'http://doi.org/' + str(journal.year_dict[year][ARTICLE].doi)

                writer.writerow([journal.title,
                                 year,
                                 article.result,
                                 article.doi,
                                 doi_url,
                                 journal.package,
                                 journal.url,
                                 journal.publisher,
                                 ])


def append_exception_row(journal, file_name='exception-list'):
    """
    :param journal:
    :param file_name:
    :return:
    """
    with open(exception_path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        for year in journal.year_dict:
            if journal.year_dict[year][ARTICLE].exception:
                details = journal.year_dict[year][ARTICLE].exception_details
                writer.writerow([journal.title,
                                 year,
                                 journal.year_dict[year][ARTICLE].doi,
                                 'http://doi.org/' + str(journal.year_dict[year][ARTICLE].doi),
                                 journal.package,
                                 journal.url,
                                 journal.publisher,
                                 details[0],
                                 details[1],
                                 details[2],
                                 ])


def has_entry(path_name):
    new_path = path + path_name + '.csv'
    print('check lines:', len(open(new_path).readlines()))

    # has at least one entry without counting header
    if len(open(new_path).readlines()) > 1:
        return True
    return False


if __name__ == '__main__':
    print('csv reader')
