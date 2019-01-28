class Journal(object):
    year_dict = {}  # dictionary with "year" and "boolean" pair
    wrong_years = set()

    # more_year_dict = {}

    def __init__(self,
                 title=None, package=None,
                 url=None, publisher=None,
                 printISSN=None, onlineISSN=None,
                 expected_subscript_begin=1990, expected_subscript_end=2001,
                 ):
        self.title = title
        self.package = package
        self.url = url
        self.publisher = publisher
        self.printISSN = printISSN
        self.onlineISSN = onlineISSN
        self.expected_subscription_begin = expected_subscript_begin
        self.expected_subscription_end = expected_subscript_end

        # self.create_year_dict()

    def __str__(self):
        s = ' / '
        str = ("\"" + self.title + "\" / " + self.package + s +
               self.url + s +
               self.publisher + s +
               self.expected_subscription_begin + s +
               self.expected_subscription_end + s
               )
        return str


def create_year_dict(self):
    year = self.expected_subscription_begin
    while year <= self.expected_subscription_end:
        self.year_dict[year] = False
        year = year + 1


def set_dict_year_true(self, year):
    self.year_dict[year] = True

# journal = Journal()
# journal.speak()
