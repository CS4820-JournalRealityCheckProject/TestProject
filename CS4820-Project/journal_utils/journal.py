import datetime
import re

import journal_utils.article as article


class Journal(object):
    """This class models a journal"""

    def __init__(self,
                 title='None', package='None',
                 url='None', publisher='None',
                 print_issn='None', online_issn='None',
                 expected_subscript_begin='None',
                 expected_subscript_end='None'
                 ):

        self.title = title
        self.package = package
        self.url = url
        self.publisher = publisher
        self.print_issn = print_issn
        self.online_issn = online_issn
        self.expected_subscription_begin = self.format_date(expected_subscript_begin)
        self.expected_subscription_end = self.format_date(expected_subscript_end)

        print(title, package, '=', self.expected_subscription_begin, ':', self.expected_subscription_end)  # Test print

        self.begin_date = self.create_date(self.expected_subscription_begin)  # datetime object
        self.end_date = self.create_date(self.expected_subscription_end)  # datetime object
        self.year_dict = {}  # year: (start_date, end_date, Article)
        self.year_article_dict = {}  # year: Article

        self.create_year_dict()

        self.result_as_expected = True
        self.wrong_years = ''
        self.free_years = ''
        # self.record_wrong_years()

    def __str__(self):
        s = ', '
        q = "'"
        cq = s + q
        line = ("\"" + self.title + "\" / " + self.package + s +
                # self.url + s +
                # self.publisher + s +
                self.wrap_quote(self.title) + s +
                self.wrap_quote(self.expected_subscription_begin) + s +
                self.wrap_quote(self.expected_subscription_end) + s +
                self.wrap_quote(self.print_issn) + s +
                self.wrap_quote(self.online_issn) + s
                # str(self.begin_date) + s +
                # str(self.end_date) + s
                )
        return line

    @staticmethod
    def wrap_quote(s):
        """
        Given string is wrapped with single quotes.
        :param s: string
        :return: a string wapped with single quotes.
        """
        return "'" + s + "'"

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
        self.year_dict[self.begin_date.year] = (self.expected_subscription_begin,
                                                str(self.begin_date.year) + '-12-31',
                                                article.Article(date=self.begin_date))
        # self.year_article_dict[self.begin_date.year] = article.Article(date=self.begin_date)

        year = self.begin_date.year + 1
        while year < self.end_date.year:
            self.year_dict[year] = (
                str(year) + '-01-01',
                str(year) + '-12-31',
                article.Article(date=datetime.datetime(year, 1, 1)))
            # self.year_article_dict = article.Article(date=datetime.datetime(year, 1, 1))
            year = year + 1

        self.year_dict[self.end_date.year] = (str(self.end_date.year) + '-01-01',
                                              self.str_date(self.end_date),
                                              article.Article(date=self.end_date))
        # self.year_article_dict[self.end_date.year] = article.Article(date=self.end_date)

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
        for year in self.year_dict:
            if not self.year_dict[year][2].accessible:  # article is accessible
                if self.year_dict[year][2].result != 'Open-Access' and \
                        self.year_dict[year][2].result != 'Free-Access':
                    self.wrong_years = self.wrong_years + str(year) + '/'
                    self.result_as_expected = False
        if self.result_as_expected:
            self.wrong_years = 'No-Wrong-Years'

    def record_free_years(self):
        for year in self.year_dict:
            if not self.year_dict[year][2].accessible:  # article is accessible
                if self.year_dict[year][2].result == 'Open-Access' or \
                        self.year_dict[year][2].result == 'Free-Access':
                    self.free_years = self.free_years + str(year) + '/'
                    self.result_as_expected = False
        if self.result_as_expected:
            self.free_years = 'No-Free-Years'

    @staticmethod
    def format_date(date):
        if date == 'Present':
            return date

        date1 = re.fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}', date)  # xxxx-xx-xx
        if date1 is not None:
            return date

        date1 = re.fullmatch('[0-9]{4}-[0-9]-[0-9]', date)  # xxxx-x-x
        if date1 is not None:
            return date[0:4] + '-0' + date[5:6] + '-0' + date[7:8]

        date1 = re.fullmatch('[0-9]{4}-[0-9][0-9]-[0-9]', date)  # xxxx-xx-x
        if date1 is not None:
            return date[0:4] + '-' + date[5:7] + '-0' + date[8:9]

        date1 = re.fullmatch('[0-9]{4}-[0-9]-[0-9][0-9]', date)  # xxxx-xx-x
        if date1 is not None:
            return date[0:4] + '-0' + date[5:6] + '-' + date[7:9]

        date2 = re.fullmatch('[0-9]{2}/[0-9]{2}/[0-9]{4}', date)  # xx/xx/xxxx
        if date2 is not None:
            return date[6:10] + '-' + date[3:5] + '-' + date[0:2]

        return '0000-00-00'


if __name__ == '__main__':
    print('matcher')
    m = re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', '2000-3-21')
    n = re.match('[0-9]{2}/[0-9]{2}/[0-9]{4}', '33/43/3333')
    print(m)
    print(n)
    print(Journal.format_date('1991-12-12'))
    print(Journal.format_date('1991-1-12'))
    print(Journal.format_date('1991-12-2'))
    print(Journal.format_date('1991-1-3'))
    print(Journal.format_date('01/05/1993'))
