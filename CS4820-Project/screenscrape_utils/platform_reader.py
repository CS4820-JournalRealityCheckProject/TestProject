import csv
import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
PLATFORM_FILE_NAME = '/Data-Files/Configurations/Platform_List.csv'
PLATFORM_COLUMNS = ['platform_name', 'func_name', 'base_url']


def read_platforms():
    """
    Read platforms from the list
    :return: None, if the file is not correct
             Otherwise, List of the list of platform, func and base url
    """
    file_name = BASE_PATH + PLATFORM_FILE_NAME

    if not correct_columns(file_name):
        return None

    platform_list = []
    with open(file_name, 'r', encoding='utf8') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            platform_list.append([row['platform_name'], row['func_name'], row['base_url']])

    return platform_list


def correct_columns(file_name):
    """
    :param file_name:
    :return: True, if columns are correct
             False, otherwise
    """
    with open(file_name, 'r', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # only for python 3

        if header == PLATFORM_COLUMNS:
            return True
        return False


if __name__ == '__main__':
    print('hi')
    platform_list1 = read_platforms()
    for p in platform_list1:
        print(p)
