from crossref.restful import Works
from crossref.restful import Journals

works = Works()

for i in works.query('Systematic Biology').filter(has_funder='true', has_license='true', issn='1076-836X').sample(10).select('DOI, prefix'):
    print(str(i))


journals = Journals()
journal_ = journals.journal('0975-7651')
print journal_