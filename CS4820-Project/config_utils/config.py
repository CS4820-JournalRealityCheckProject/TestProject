import configparser


def update_progress(input_file, output_file, wrong_file, status, index, title='not-specified'):
    config = configparser.ConfigParser()
    config['progress'] = {
        'complete': False,
        'status': status,
        'input-file-path': input_file,
        'output-file-path': output_file,
        'wrong-file-path': wrong_file,
        'current-index': index,
        'title': title

    }
    with open('./Data-Files/Configurations/progress.ini', 'w') as config_file:
        config.write(config_file)


def clear_progress():
    config = configparser.ConfigParser()

    config['progress'] = {
        'complete': True,
        'status': 0,
        'input-file-path': 'no-path',
        'output-file-path': 'no-path',
        'wrong-file-path': 'no-path',
        'current-index': -1

    }
    with open('./Data-Files/Configurations/progress.ini', 'w') as config_file:
        config.write(config_file)


if __name__ == '__main__':
    print('config')

    update_progress(99)
    # end_progress()
