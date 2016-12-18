'''Bla bla

'''
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

    def __init__(self, pmid=None):
        '''Bla bla

        '''
        self.pmid = pmid
        self.article_title = None 
        self.article_abstract = None
        self.journal_title = None
        self.journal_title_abb = None
        self.journal_volume = None
        self.journal_year = None
        self.journal_pages = None

class PubMedCorpus:
    '''Bla bla

    '''
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

