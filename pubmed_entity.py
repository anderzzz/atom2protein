'''Bla bla

'''
import xml.etree.ElementTree as etree

class XMLPathError(Exception):
    pass

class PMIDResetError(Exception):
    pass

class PubMedEntry:
    '''Bla bla

    '''
    def set_journal_title(self, title):
        '''Bla bla

        '''
        self.journal_title = title

    def set_journal_title_abbreviation(self, title_abb):
        '''Bla bla

        '''
        self.journal_title_abb = title_abb

    def set_journal_year(self, year):
        '''Bla bla

        '''
        self.journal_year = int(year)

    def set_journal_volume(self, volume):
        '''Bla bla

        '''
        self.journal_volume = volume

    def set_journal_pages(self, pagination):
        '''Bla bla

        '''
        self.journal_pagination = pagination

    def set_article_title(self, title):
        '''Bla bla

        '''
        self.article_title = title

    def set_article_abstract(self, abstract_text):
        '''Bla bla

        '''
        self.article_abstract = abstract_text

    def set_pmid(self, pmid):
        '''Bla bla

        '''
        if self.pmid == None:
            self.pmid = int(pmid)
        else:
            raise PMIDResetError('PubMed ID already set. Changing it not an allowed operation')

    def get_pmid(self):
        '''Bla bla

        '''
        return self.pmid

    def _get_and_check(self, root, path, default=''):
        '''Bla bla

        '''
        element = root.find(path)
        if element is None:
            ret = default
        else:
            ret = element.text
            if len(ret.strip()) == 0:
                raise XMLPathError('The path %s returned empty text')

        return ret

    def _populate_from_xml(self, xml_string):
        '''Bla bla

        '''
        root = etree.fromstring(xml_string)

        medline_root = './PubmedArticle/MedlineCitation/'
        article_root = medline_root + 'Article/'

        self.set_pmid(self._get_and_check(root, 
                      medline_root + 'PMID'))
        self.set_journal_title(self._get_and_check(root, 
                               article_root + 'Journal/Title')) 
        self.set_journal_title_abbreviation(self._get_and_check(root,
                                            article_root + 'Journal/ISOAbbreviation')) 
        self.set_journal_volume(self._get_and_check(root,
                                article_root + 'Journal/JournalIssue/Volume'))
        self.set_journal_year(self._get_and_check(root,
                              article_root + 'Journal/JournalIssue/PubDate/Year'))
        self.set_article_title(self._get_and_check(root,
                               article_root + 'ArticleTitle'))
        self.set_article_abstract(self._get_and_check(root,
                                  article_root + 'Abstract/AbstractText'))
        self.set_journal_pages(self._get_and_check(root,
                               article_root + 'Pagination/MedlinePgn'))

    def __str__(self):
        '''Bla bla

        '''
        title_line = 'Article with title: "%s"' %(self.article_title)
        pubmed_id_line = 'Pubmed ID: %s' %(str(self.pmid))

        return title_line + '\n' + pubmed_id_line

    def __eq__(self, other):
        '''Bla bla

        '''
        pmid_1 = self.get_pmid()
        pmid_2 = other.get_pmid()

        return pmid_1 == pmid_2

    def __hash__(self):
        '''Bla bla

        '''
        return self.get_pmid()

    def __init__(self, xml_rawdata):
        '''Bla bla

        '''
        self.pmid = None
        self.article_title = None 
        self.article_abstract = None
        self.journal_title = None
        self.journal_title_abb = None
        self.journal_volume = None
        self.journal_year = None
        self.journal_pages = None

        self._populate_from_xml(xml_rawdata) 

class PubMedCorpus:
    '''Bla bla

    '''
    def append(self, element):
        '''Bla bla

        '''
        element_parsed = PubMedEntry(element)
        self.container.add(element_parsed)

    def __iter__(self):
        '''Bla bla

        '''
        for entry in self.container:
            yield entry

    def __len__(self):
        '''Bla bla

        '''
        return len(self.container)

    def __init__(self):
        '''Bla bla

        '''
        self.container = set([]) 

