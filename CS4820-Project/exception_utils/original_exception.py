#  The format of the date is not correct
class CsvDateFormatException(Exception):
    pass


#  Column(s) of a CSV file is emtpy
class CsvEmptyColumnException(Exception):
    pass


class CsvEmptyBeginDateException(CsvDateFormatException):
    pass


class CsvEmptyPrintIssnException(CsvEmptyColumnException):
    pass


class CsvEmptyOnlineIssnException(CsvEmptyColumnException):
    pass


class CsvEmptyTitleException(CsvEmptyColumnException):
    pass


class CsvEmptyPlatformException(CsvEmptyColumnException):
    pass


#  Exception which happens during reality check
class RealityCheckException(Exception):
    pass


#  Exception which happens during DOI search
class DoiSearchException(Exception):
    pass
