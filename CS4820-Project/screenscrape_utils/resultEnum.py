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
    NetworkError = 5
    PublisherNotFound = 6
    OtherException = 7
