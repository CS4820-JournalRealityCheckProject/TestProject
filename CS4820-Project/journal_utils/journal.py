import datetime
import journal_utils.article as article


class Journal(object):

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
        self.expected_subscription_begin = expected_subscript_begin
        self.expected_subscription_end = expected_subscript_end

        # self.begin_date = self.create_date(expected_subscript_begin)
        # self.end_date = self.create_date(expected_subscript_end)
        self.year_dict = {}  # year: (start_date, end_date, article)

        # self.create_year_dict()

    def __str__(self):
        s = ' / '
        line = ("\"" + self.title + "\" / " + self.package + s +
                self.url + s +
                self.publisher + s +
                self.expected_subscription_begin + s +
                self.expected_subscription_end + s
                # str(self.begin_date) + s +
                # str(self.end_date) + s
                )
        return line

    @staticmethod
    def create_date(date):
        if date == 'Present':
            return datetime.datetime.today()
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        return datetime.datetime(year, month, day)

    def create_year_dict(self):
        self.year_dict[self.begin_date.year] = (self.expected_subscription_begin,
                                                str(self.begin_date.year) + '-12-31',
                                                article.Article(date=self.begin_date))

        year = self.begin_date.year + 1
        while year < self.end_date.year:
            print('year:', year)
            self.year_dict[year] = (
                str(year) + '-01-01',
                str(year) + '-12-31',
                article.Article(date=datetime.datetime(year, 1, 1)))
            year = year + 1
        print('\n')

        self.year_dict[self.end_date.year] = (str(self.end_date.year) + '-01-01',
                                              self.str_date(self.end_date),
                                              article.Article(date=self.end_date))

    @staticmethod
    def str_date(date):
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
        a = self.year_dict[year][2]
        a.name = name
        a.doi = doi
        a.date = date


if __name__ == '__main__':
    j1 = Journal(expected_subscript_begin='2009-04-01',
                 expected_subscript_end='2013-10-31')

    j2 = Journal(expected_subscript_begin='2015-03-01',
                 expected_subscript_end='Present')

    for key in j1.year_dict:
        print(key, ':', j1.year_dict[key])

    print('\n')

    for key in j2.year_dict:
        print(key, ':', j2.year_dict[key])

    print('\n')
    print(j1)
    print(j2)
