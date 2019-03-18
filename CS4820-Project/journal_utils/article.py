import datetime
import screenscrape_utils.result_enum as resultEnum

class Article(object):
    """This class models an article"""

    def __init__(self, name='nothing', doi=None, date=None):
        self.name = name
        self.doi = doi
        self.date = date
        self.accessible = resultEnum.Result.Access
        self.reason_of_false = 'no issues'

    def __str__(self):
        return self.name
