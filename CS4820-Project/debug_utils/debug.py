import configparser
import config_utils.config

config = configparser.ConfigParser()
config.read(config_utils.config.PATH_TO_DEBUG_INI)
if config['debug']['debug-print-mode'] == 'True':
    debug_mode = True
else:
    debug_mode = False

if debug_mode:
    if config['debug']['debug-detail-mode'] == 'True':
        debug_detail_mode = True
    else:
        debug_detail_mode = False
else:
    debug_detail_mode = False


def d_print(s1='', s2='', s3='', s4='', s5='', s6='', s7='', s8='', s9='', s10=''):
    if debug_mode:
        print(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)


def d_print_detail(s1='', s2='', s3='', s4='', s5='', s6='', s7='', s8='', s9='', s10=''):
    if debug_detail_mode:
        print(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)
