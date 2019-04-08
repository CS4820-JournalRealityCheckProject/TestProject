import datetime
import re
import logging

import journal_utils.article as article
import debug_utils.debug as debug


# logging.basicConfig(level=logging.DEBUG, format='journal.py: %(message)s')


class Journal(object):
    """This class models a journal"""

    # indexes for year_dict
    BEGIN = 0
    END = 1
    ARTICLE = 2

    # problems that can occur
    YEAR_FORMAT_PROBLEM = 'Date-Format-Wrong'
    BOTH_BEGIN_END_EMPTY = 'Both-Dates-Empty'
    EMPTY_COLUMN_PROBLEM = 'Has-Empty-Column'

    def __init__(self,
                 title='None', package='None',
                 url='None', publisher='None',
                 print_issn='None', online_issn='None',
                 expected_subscript_begin='None',
                 expected_subscript_end='None'
                 ):

        # member variables 1 for problems
        self.has_problem = False
        self.problem_detail = ''

        # member variables 2
        self.result_as_expected = True
        self.access_to_all = True
        self.has_free_years = False
        self.wrong_years = ''
        self.free_years = ''

        # member variables 3
        self.title = title
        self.package = package
        self.url = url
        self.publisher = publisher
        self.print_issn = print_issn
        self.online_issn = online_issn

        # if self.print_issn == '':
        # self.print_issn = 'no-print-issn'
        # if self.online_issn == '':
        # self.online_issn = 'no-online-issn'

        # if both years are empty
        if expected_subscript_begin == '':
            self.has_problem = True
            self.problem_detail = self.BOTH_BEGIN_END_EMPTY
            self.expected_subscription_begin = expected_subscript_begin
            self.expected_subscription_end = expected_subscript_end
            debug.d_print(title, package, '=', self.expected_subscription_begin, ':', self.expected_subscription_end)
            return

        try:
            self.expected_subscription_begin = self.format_date(expected_subscript_begin, self.BEGIN)
            self.expected_subscription_end = self.format_date(expected_subscript_end, self.END)
        except ValueError as ex:
            self.has_problem = True
            self.problem_detail = self.YEAR_FORMAT_PROBLEM
            self.expected_subscription_begin = expected_subscript_begin
            self.expected_subscription_end = expected_subscript_end
            logging.debug(ex)
            logging.debug('format_date')
            logging.debug(self.title)
            logging.debug(__class__)
            debug.d_print(title, package, '=', self.expected_subscription_begin, ':', self.expected_subscription_end)
            return  # the value is incorrect, you will not create a journal

        debug.d_print(title, package, '=', self.expected_subscription_begin, ':', self.expected_subscription_end)

        try:
            self.begin_datetime = self.create_date(self.expected_subscription_begin)  # datetime object
            self.end_datetime = self.create_date(self.expected_subscription_end)  # datetime object
            self.year_dict = {}  # year: (start_date, end_date, Article)
            self.create_year_dict()
        except ValueError as ex:
            self.has_problem = True
            self.problem_detail = self.YEAR_FORMAT_PROBLEM
            logging.debug(ex)
            logging.debug(__class__)
            return

        # checks if begin_datetime is later than end_datetime
        if self.begin_datetime > self.end_datetime:
            self.has_problem = True
            self.problem_detail = 'Begin-Later-Than-End-Year'
            return

        # checks if begin_datetime and end_date are same
        if self.begin_datetime == self.end_datetime:
            self.has_problem = True
            self.problem_detail = 'Begin-End-Year-Same'
            return

    def __str__(self):
        s = ', '
        q = "'"
        cq = s + q
        line = (self.wrap_quote(self.title) + ' ' +
                self.wrap_quote(self.expected_subscription_begin) + ' ' +
                self.wrap_quote(self.expected_subscription_end) + ' ' +
                self.wrap_quote(self.print_issn) + ' ' +
                self.wrap_quote(self.online_issn) + ' ' +
                self.wrap_quote(self.package) + ' ' +
                self.wrap_quote(self.publisher)
                # self.wrap_quote(self.url) + s +
                # str(self.begin_datetime) + s +
                # str(self.end_datetime) + s
                )
        # line = (self.title + ', ' + self.expected_subscription_begin + ', ' + self.expected_subscription_end + ', ' +
        #         self.print_issn + ', ' + self.online_issn + ', ' + self.package)

        return line

    @staticmethod
    def wrap_quote(s):
        """
        Given string is wrapped with single quotes.
        :param s: string
        :return: a string wapped with single quotes.
        """
        return '[' + s + ']'

    @staticmethod
    def create_date(date):
        """
        Dates formats are created from a given dates.
        :param date:
        :return:
        """
        if date == 'Present':
            return datetime.datetime.today()
        try:
            year = int(date[0:4])  # exception should be handled here
            month = int(date[5:7])
            day = int(date[8:10])
        except ValueError:
            year = 0
            month = 0
            day = 0

        return datetime.datetime(year, month, day)

    def create_year_dict(self):
        """
        The dictionary for each article year is made.
            year_dict{year: (start_year, end_year, article)}
        :return:
        """
        self.year_dict[self.begin_datetime.year] = (self.expected_subscription_begin,
                                                    str(self.begin_datetime.year) + '-12-31',
                                                    article.Article(date=self.begin_datetime))
        # self.year_article_dict[self.begin_datetime.year] = article.Article(date=self.begin_datetime)

        year = self.begin_datetime.year + 1
        while year < self.end_datetime.year:
            self.year_dict[year] = (
                str(year) + '-01-01',
                str(year) + '-12-31',
                article.Article(date=datetime.datetime(year, 1, 1)))
            # self.year_article_dict = article.Article(date=datetime.datetime(year, 1, 1))
            year = year + 1

        self.year_dict[self.end_datetime.year] = (str(self.end_datetime.year) + '-01-01',
                                                  self.str_date(self.end_datetime),
                                                  article.Article(date=self.end_datetime))
        # self.year_article_dict[self.end_datetime.year] = article.Article(date=self.end_datetime)

    @staticmethod
    def str_date(date):
        """
        Date is converted into "xxxx-yy-zz" format
        :param date: datetime object
        :return: date string
        """
        if date.month <= 9:
            m = '0' + str(date.month)
        else:
            m = str(date.month)
        if date.day <= 9:
            d = '0' + str(date.day)
        else:
            d = str(date.day)
        return str(date.year) + '-' + m + '-' + d

    def record_article(self, year, name, doi, date):
        """
        The result of an article is recorded.
        :param year:
        :param name:
        :param doi:
        :param date:
        :return:
        """
        a = self.year_dict[year][2]
        a.name = name
        a.doi = doi
        a.date = date

    def record_wrong_years(self):
        self.wrong_years = ''
        for year in self.year_dict:
            a = self.year_dict[year][self.ARTICLE]

            if not a.accessible:  # article is accessible
                if not a.open and not a.free:
                    self.wrong_years = self.wrong_years + str(year) + '/'
                    self.result_as_expected = False
                    self.access_to_all = False
        if self.access_to_all:
            self.wrong_years = 'No-Problem-Years'

    def record_free_years(self):
        self.free_years = ''
        for year in self.year_dict:
            a = self.year_dict[year][self.ARTICLE]

            if a.accessible:
                if a.open or a.free:
                    self.free_years = self.free_years + str(year) + '/'
                    self.result_as_expected = False
                    self.has_free_years = True
        if not self.has_free_years:
            self.free_years = 'No-Free-Years'

    def set_problem(self, problem_detail='csv-wrong-row'):
        self.has_problem = True
        self.problem_detail = problem_detail

    @staticmethod
    def format_date(date, begin_or_end):
        BEGIN = 0
        END = 1

        if date == 'Present':
            return date

        if date == '' and begin_or_end == END:  # when ending date is empty, then consider it as 'Present'
            return 'Present'

        date0 = re.fullmatch('[0-9]{4}', date)  # yyyy
        if date0 is not None:
            if begin_or_end == BEGIN:
                return date + '-01-01'
            elif begin_or_end == END:
                return date + '-12-31'

        date0 = re.fullmatch('[0-9]{4}-[0-9]{2}', date)  # yyyy-mm
        if date0 is not None:
            if begin_or_end == BEGIN:
                return date + '-01'
            elif begin_or_end == END:
                return date + '-31'

        date1 = re.fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}', date)  # yyyy-mm-dd
        if date1 is not None:
            return date

        date1 = re.fullmatch('[0-9]{4}-[0-9]-[0-9]', date)  # yyyy-m-d
        if date1 is not None:
            return date[0:4] + '-0' + date[5:6] + '-0' + date[7:8]

        date1 = re.fullmatch('[0-9]{4}-[0-9][0-9]-[0-9]', date)  # yyyy-mm-d
        if date1 is not None:
            return date[0:4] + '-' + date[5:7] + '-0' + date[8:9]

        date1 = re.fullmatch('[0-9]{4}-[0-9]-[0-9][0-9]', date)  # yyyy-m-dd
        if date1 is not None:
            return date[0:4] + '-0' + date[5:6] + '-' + date[7:9]

        date2 = re.fullmatch('[0-9]{2}/[0-9]{2}/[0-9]{4}', date)  # mm/dd/yyyy
        if date2 is not None:
            return date[6:10] + '-' + date[0:2] + '-' + date[3:5]

        date2 = re.fullmatch('[0-9]/[0-9]{2}/[0-9]{4}', date)  # m/dd/yyyy
        if date2 is not None:
            return date[5:9] + '-0' + date[0:1] + '-' + date[2:4]

        date2 = re.fullmatch('[0-9]{2}/[0-9]/[0-9]{4}', date)  # mm/d/yyyy
        if date2 is not None:
            return date[5:9] + '-' + date[0:2] + '-0' + date[3:4]

        date2 = re.fullmatch('[0-9]/[0-9]/[0-9]{4}', date)  # m/d/yyyy
        if date2 is not None:
            return date[4:8] + '-0' + date[0:1] + '-0' + date[2:3]

        # date2 = re.fullmatch('[0-9]{2}/[0-9]{2}/[0-9]{4}', date)  # dd/mm/yyyy
        # if date2 is not None:
        #     return date[6:10] + '-' + date[3:5] + '-' + date[0:2]

        # date format is not expected
        raise ValueError


if __name__ == '__main__':
    # m = re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', '2000-3-21')
    # n = re.match('[0-9]{2}/[0-9]{2}/[0-9]{4}', '33/43/3333')
    # debug.d_print(m)
    # debug.d_print(n)
    b = 0
    e = 1
    debug.d_print(Journal.format_date('1991-12-12', b))
    debug.d_print(Journal.format_date('1991-1-12', e))
    debug.d_print(Journal.format_date('1991-12-2', b))
    debug.d_print(Journal.format_date('1991-1-3', e))
    debug.d_print(Journal.format_date('11/31/1993', b))
    debug.d_print(Journal.format_date('1/31/1993', b))
    debug.d_print(Journal.format_date('11/1/1993', b))
    debug.d_print(Journal.format_date('1/1/1993', b))

    debug.d_print(Journal.format_date('1991-12', b))
    debug.d_print(Journal.format_date('1933-03', e))
    debug.d_print(Journal.format_date('2091', b))
    debug.d_print(Journal.format_date('2001', e))
    debug.d_print(Journal.format_date('', e))
