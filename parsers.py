'''Bla bla

'''
from webapis import PDBData, PubMedData
from pdbparser import PDBParser

class UnknownDataType(Exception):
    pass

class Parser:
    '''Bla bla

    '''
    def __call__(self, data):
        '''Bla bla

        '''
        self.parser(data)
        
    def __init__(self, data_type):
        '''Bla bla

        '''
        if isinstance(data_type, PDBData):
            self.parser = PDBParser()
        elif isinstance(data_type, PubMedData):
            self.parser = None 
        else:
            raise UnknownDataType('No parser exist for data type %s' %(type(data_type))
