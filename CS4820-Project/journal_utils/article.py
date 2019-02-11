import datetime


class Article:

    def __init__(self, name='nothing', doi=None, date=None):
        self.name = name
        self.doi = doi
        self.date = date
        self.accessible = False

    def __str__(self):
        return self.name
