import csv

from journal_utils.journal import Journal


def write_file(file_name):
    with open(file_name + '.csv', 'w') as csv_file:
        fieldnames = ['title', 'package']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'title': 'Japan Academic', 'package': 'Japan Times'})
        writer.writerow({'title': 'Monthly Cooking', 'package': 'NHK Journal'})


# title='None', package='None',
#                  url='None', publisher='None',
#                  print_issn='None', online_issn='None',
#                  expected_subscript_begin='None',
#                  expected_subscript_end='None'


def write_result_csv(journal_list, file_name='journal_result'):
    print("result file")
    with open(file_name + '.csv', 'w') as csv_file:
        fieldnames = ['Title', 'PackageName', 'URL', 'Publisher', 'PrintISSN',
                      'OnlineISSN', 'ManagedCoverageBegin', 'ManagedCoverageEnd'
                      'AsExpected', 'ProblemYears', 'FreeYears' ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for j in journal_list:
            writer.writerow({'Title': j.title, 'PackageName': j.package, 'URL': j.url,
                             'Publisher': j.publisher, 'PrintISSN': j.print_isssn,'OnlineISSN': j.online_issn,
                             'ManagedCoverageBegin': j.expected_subscript_begin ,
                             'ManagedCoverageEnd': j.expected_subscript_end,
                             'AsExpected': 'Correct', 'ProblemYears': '1993, 1995',
                             'FreeYears': '2005'})




def write_problem_csv():
    print("result file")


def write_doi_csv():
    print("result file")


def read_file(file_name):
    with open(file_name + '.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row['title'], '=>', row['package'])


def read_csv_create_journal(file_name):
    journal_list = []

    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            journal_list.append(
                Journal(row['Title'], row['PackageName'], row['URL'],
                        row['Publisher'], row['PrintISSN'], row['OnlineISSN'],
                        row['ManagedCoverageBegin'], row['ManagedCoverageEnd']
                        ))
    return journal_list


if __name__ == '__main__':
    write_file('t1')
    read_file('t1')
    list = read_csv_create_journal('journals1')
    for i in list:
        print(i)
