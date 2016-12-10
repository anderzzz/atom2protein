'''Bla bla

'''
class InvalidFormat(Exception):
    pass

class PDBData:
    '''Bla bla

    '''
    def by_pdbid(ids):
        '''Bla bla

        '''
        self.query = self.url_base + self.custom_report + '?' + \
                     'pdbids='

    def set_format_return(self, format_name):
        '''Bla bla

        '''
        if not format_name in self._available_formats: 
            raise InvalidFormat("Query return format %s not supported" %(format_name))

        self.format_return = 'format=' + format_name

    def __init__(self):
        '''Bla bla

        '''
        self.url_base = 'http://www.rcsb.org/pdb/rest/'
        self.custom_report = 'customReport.xml'
        self.format_return = 'format=csv'
        self._available_formats = ['csv', 'xml']

class NatureData:
    '''Bla bla

    '''
    url_base = 'empty'

