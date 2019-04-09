import configparser
import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

PATH_TO_PROGRESS_INI = BASE_PATH + '/Data-Files/Configurations/progress.ini'
PATH_TO_EMAIL_INI = BASE_PATH + '/Data-Files/Configurations/email.ini'
PATH_TO_SMTP_SERVER_INI = BASE_PATH + '/Data-Files/Configurations/smtp-server.ini'
PATH_TO_DEBUG_INI = BASE_PATH + '/Data-Files/Configurations/debug.ini'


def update_progress(input_file, output_file, wrong_file, exception_file, status, index, title='not-specified'):
    config = configparser.ConfigParser()
    config['progress'] = {
        'complete': False,
        'status': status,
        'input-file-path': input_file,
        'output-file-path': output_file,
        'wrong-file-path': wrong_file,
        'exception-file-path': exception_file,
        'current-index': index,
        'title': title

    }
    with open(BASE_PATH + '/Data-Files/Configurations/progress.ini', 'w') as config_file:
        config.write(config_file)


def clear_progress():
    config = configparser.ConfigParser()

    config['progress'] = {
        'complete': True,
        'status': 0,
        'input-file-path': 'no-path',
        'output-file-path': 'no-path',
        'wrong-file-path': 'no-path',
        'exception-file-path': 'no-path',
        'current-index': -1

    }
    with open(BASE_PATH + '/Data-Files/Configurations/progress.ini', 'w') as config_file:
        config.write(config_file)

    return PATH_TO_PROGRESS_INI


def update_email(receiver):
    email_config = configparser.ConfigParser()
    email_config.read(PATH_TO_EMAIL_INI)

    config = configparser.ConfigParser()
    config['email'] = {
        'sender': email_config['email']['sender'],
        'receiver': receiver,
        'password': email_config['email']['password']
    }
    with open(BASE_PATH + '/Data-Files/Configurations/email.ini', 'w') as config_file:
        config.write(config_file)

