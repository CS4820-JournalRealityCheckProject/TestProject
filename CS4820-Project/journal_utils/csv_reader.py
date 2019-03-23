import csv

from journal_utils.journal import Journal

path = 'Data-Files/Output-Files/'


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
                j.year_dict[y][2].doi = row['DOI']
                journal_obj_list.append(j)
                # j.year_dict[y][2].accessible = access
            else:
                j.year_dict[y][2].doi = row['DOI']
                # j.year_dict[y][2].accessible = access

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
        j = journal
        for y in j.year_dict:
            writer.writerow([j.title,
                             y,
                             j.year_dict[y][2].doi,
                             j.package,
                             j.url,
                             j.publisher,
                             j.print_issn,
                             j.online_issn,
                             j.expected_subscription_begin,
                             j.expected_subscription_end,
                             ])


def append_journal_row(journal, file_name='result-journals'):
    with open(path + file_name + '.csv', 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        j = journal
        writer.writerow([j.title,
                         j.package,
                         j.url,
                         j.publisher,
                         j.print_issn,
                         j.online_issn,
                         j.expected_subscription_begin,
                         j.expected_subscription_end,
                         j.result_as_expected,
                         j.wrong_years,
                         j.free_years
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
        j = journal
        for y in j.year_dict:
            if mode == 'doi-search' and j.year_dict[y][2].doi is None:
                writer.writerow([j.title,
                                 y,
                                 j.year_dict[y][2].result,
                                 'no-doi',
                                 '',
                                 j.package,
                                 j.url,
                                 j.publisher,
                                 ])

            if mode == 'check-reality' and not j.year_dict[y][2].accessible:
                writer.writerow([j.title,
                                 y,
                                 j.year_dict[y][2].result,
                                 j.year_dict[y][2].doi,
                                 'http://doi.org/' + str(j.year_dict[y][2].doi),
                                 j.package,
                                 j.url,
                                 j.publisher,
                                 ])


if __name__ == '__main__':
    print('csv reader')
