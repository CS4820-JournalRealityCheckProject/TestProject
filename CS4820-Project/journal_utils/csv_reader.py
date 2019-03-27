import csv

from journal_utils.journal import Journal

path = 'Data-Files/Output-Files/'
ARTICLE = 2


def construct_journal_list_from(journals_csv):
    journal_obj_list = []

    with open(journals_csv, 'r', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
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
        j = None
        for row in reader:
            y = int(row['Year'])
            # if row['Accessible'] == 'TRUE':
            #     access = True
            # else:
            #     access = False

            if current_title != row['Title'] or current_platform != row['PackageName']:
                current_title = row['Title']
                current_platform = row['PackageName']

                j = Journal(row['Title'],
                            row['PackageName'],
                            row['URL'],
                            row['Publisher'],
                            row['PrintISSN'],
                            row['OnlineISSN'],
                            row['ManagedCoverageBegin'],
                            row['ManagedCoverageEnd']
                            )
                j.year_dict[y][ARTICLE].doi = row['DOI']
                journal_obj_list.append(j)
                # j.year_dict[y][ARTICLE].accessible = access
            else:
                j.year_dict[y][ARTICLE].doi = row['DOI']
                # j.year_dict[y][ARTICLE].accessible = access

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
            if mode == 'doi-search':
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

            if mode == 'doi-search' and journal.year_dict[year][ARTICLE].doi is None:
                writer.writerow([journal.title,
                                 year,
                                 journal.year_dict[year][ARTICLE].result,
                                 'no-doi',
                                 '',
                                 journal.package,
                                 journal.url,
                                 journal.publisher,
                                 ])

            if mode == 'reality-check' and not journal.year_dict[year][ARTICLE].accessible:
                writer.writerow([journal.title,
                                 year,
                                 journal.year_dict[year][ARTICLE].result,
                                 journal.year_dict[year][ARTICLE].doi,
                                 'http://doi.org/' + str(journal.year_dict[year][ARTICLE].doi),
                                 journal.package,
                                 journal.url,
                                 journal.publisher,
                                 ])


if __name__ == '__main__':
    print('csv reader')
