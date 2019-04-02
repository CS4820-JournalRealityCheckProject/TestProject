
class Article(object):
    """This class models an article"""

    def __init__(self, name='nothing', doi=None, date=None):
        self.name = name
        self.doi = doi
        self.date = date
        self.accessible = False
        self.free = False
        self.open = False
        self.result = None
        self.reason_of_false = 'no issues'
        self.exception = False
        self.exceptionDetails = None

    def __str__(self):
        return self.name
