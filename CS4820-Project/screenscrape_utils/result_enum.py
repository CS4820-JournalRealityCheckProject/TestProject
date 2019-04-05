from enum import Enum


# <= 0 good
#  > 1 bad
class Result(Enum):
    Access = 0
    OpenAccess = -1
    FreeAccess = -2
    NoAccess = 1
    NoArticle = 2
    ArticleNotFound = 3
    UnsupportedWebsite = 4
    WrongWebsite = 5
    WebsiteNotAsExpected = 6
    NetworkError = 7
    PublisherNotFound = 8
    OtherException = 9
