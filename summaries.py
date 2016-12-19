'''Bla bla

How to make this nice and general for the statistics module? Lets go full blown
object oriented... in some way.
'''
from protein_structure import Structure
from pubmed_entity import PubMedEntry
from analyzers import StructureAnalyzer

import json
from collections import namedtuple

class UnknownDataType(Exception):
    pass

Entry = namedtuple('Entry', ['key','value','description'])

class StructureSummarizer:
    '''Bla bla

    '''
    def make_json(self):
        '''Bla bla

        '''
        pass

    def set_nresidues(self, structure):
        '''Bla bla

        '''
        value = self.analyzer.cmp_nresidues(structure)
        self.nresidues = Entry('number of residues', value, None)

    def set_nresidues_polarity(self, structure):
        '''Bla bla

        '''
        value = self.analyzer.cmp_nresidues_polarity(structure)
        self.nresidues_polarity = Entry('number of polarity residues', value, None)

    def __init__(self, **kwargs):
        '''Bla bla

        '''
        self.analyzer = StructureAnalyzer(**kwargs)

        self.nresidues = None
        self.nresidues_polarity = None

class PubMedSummarizer:
    '''Bla bla

    '''
    def __init__(self):
        '''Bla bla

        '''
        pass

class Summarizer:
    '''Bla bla

    '''
    def __init__(self, data_type, **kwargs):
        '''Bla bla

        '''
        if isinstance(data_type, Structure):
            self.summarizer = StructureSummarizer(**kwargs)
        elif isinstance(data_type, PubMedEntry):
            self.summarizer = PubMedSummarizer(**kwargs)
        else:
            raise UnknownDataType('No summarizer exist for data type %s' %(type(data_type)))
