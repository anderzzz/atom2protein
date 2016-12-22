'''Bla bla

'''
from primitivedata import Structure, PubMedEntry
from calculators import StructureCalculator

import json
from collections import namedtuple

class UnknownDataType(Exception):
    pass

class Entry:
    '''Bla bla

    '''
    def unpack_value(self):
        '''Bla bla

        '''
        return self.value

    def __init__(self, key, value, description=None):
        '''Bla bla

        '''
        self.key = key
        self.value = value
        self.description = description

class StructureSummarizer:
    '''Bla bla

    '''
    def make_json(self):
        '''Bla bla

        '''
        pass

    def make_pandas(self):
        '''Bla bla

        '''
        pass

    def get_entries(self):
        '''Bla bla

        '''
        public_attributes = [x for x in dir(self) if x[0] != '_']
        for attribute in public_attributes:
            whatweget = getattr(self, attribute)
            if isinstance(whatweget, Entry):
                yield whatweget

    def set_bb_torsions(self, structure):
        '''Bla bla

        '''
        value = self.calculator.cmp_bb_torsions(structure)
        self.bb_torsions = Entry('Backbone torsions', value, None)

    def get_bb_torsions(self):
        '''Bla bla

        '''
        return self.bb_torsions

    def set_bfactor_chain_stat(self, structure):
        '''Bla bla

        '''
        value = self.calculator.cmp_bfactor_chain_stat(structure)
        self.bfactor_chain_stat = Entry('B-factor chain statistics', value, None)

    def get_bfactor_chain_stat(self):
        '''Bla bla

        '''
        return self.bfactor_chain_stat

    def set_nresidues(self, structure):
        '''Bla bla

        '''
        value = self.calculator.cmp_nresidues(structure)
        self.nresidues = Entry('number of residues', value, None)

    def get_nresidues(self):
        '''Bla bla

        '''
        return self.nresidues

    def set_nresidues_polarity(self, structure):
        '''Bla bla

        '''
        value = self.calculator.cmp_nresidues_polarity(structure)
        self.nresidues_polarity = Entry('number of polarity residues', value, None)

    def get_nresidues_polarity(self):
        '''Bla bla

        '''
        return self.nresidues_polarity

    def set_label(self, label):
        '''Bla bla

        '''
        self.label = label

    def get_label(self):
        '''Bla bla

        '''
        return self.label

    def _unpack(self, get_function):
        '''Bla bla

        '''
        def wrapper():
            output = get_function()
            return output.unpack_value()

        return wrapper

    def __init__(self, **kwargs):
        '''Bla bla

        '''
        self.calculator = StructureCalculator(**kwargs)

        self.label = None
        self.nresidues = None
        self.nresidues_polarity = None
        self.bfactor_chain_stat = None

        self.unpack_nresidues_polarity = self._unpack(self.get_nresidues_polarity)
        self.unpack_nresidues = self._unpack(self.get_nresidues)
        self.unpack_bfactor_chain_stat = self._unpack(self.get_bfactor_chain_stat)
        self.unpack_bb_torsions = self._unpack(self.get_bb_torsions)
        
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
