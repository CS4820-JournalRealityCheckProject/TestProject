import csv

from journal_utils.journal import Journal


def write_file(file_name):
    with open(file_name + '.csv', 'w') as csv_file:
        fieldnames = ['title', 'package']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'title': 'Japan Academic', 'package': 'Japan Times'})
        writer.writerow({'title': 'Monthly Cooking', 'package': 'NHK Journal'})


def read_file(file_name):
    with open(file_name + '.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row['title'], '=>', row['package'])


def read_csv_create_journal(file_name):
    journal_list = []

    with open(file_name + '.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            journal_list.append(
                Journal(row['Title'], row['PackageName'], row['URL'],
                        row['Publisher'], row['PrintISSN'], row['OnlineISSN'],
                        row['ManagedCoverageBegin'], row['ManagedCoverageEnd']
                        ))

    print(journal_list[4])
    return journal_list


write_file('t1')
read_file('t1')
list = read_csv_create_journal('journals1')
for i in list:
    print(i)
