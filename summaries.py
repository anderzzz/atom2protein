'''Bla bla

'''
from primitivedata import Structure, PubMedEntry
from calculators import StructureCalculator

import json
import pandas as pd
from inspect import getmembers

class UnknownDataType(Exception):
    pass

class Entry:
    '''Bla bla

    '''
    def __init__(self, brief, value, verbose=None):
        '''Bla bla

        '''
        self.brief = brief
        self.value = value
        self.verbose = verbose

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

    def populate_bb_torsions(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_bb_torsions(structure))
        self['bb_torsions'] = Entry('backbone torsion angles', value, None)

    def populate_bfactor_chain_stat(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_bfactor_chain_stat(structure))
        self['bfactor_chain_stat'] = Entry('B-factor chain statistics', value, None)

    def populate_nresidues(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_nresidues(structure))
        self['nresidues'] = Entry('number of residues', value, None)

    def populate_nresidues_polarity(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_nresidues_polarity(structure))
        self['nresidues_polarity'] = Entry('number of polarity residues', value, None)

    def populate_rresidues_polarity(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_rresidues_polarity(structure))
        self['rresidues_polarity'] = Entry('percentage of polarity residues', value, None)

    def _get_live_entries(self):
        '''Bla bla

        '''
        live_entries = []
        for member, value in self.entry_collector.items():
            if isinstance(value, Entry):
                live_entries.append(member)
        
        return live_entries

    def _add_id_to(self, df):
        '''Bla bla

        '''
        names = ['id'] + df.index.names
        extended_index = [(self.label, ) + ind for ind in df.index]
        df.index = pd.MultiIndex.from_tuples(extended_index, names=names)

        return df

    def __add__(self, other):
        '''Bla bla

        '''
        new_summary = self.__init__(self.label + '+' + other.label)
        a_entries = set(self.__iter__())
        b_entries = set(self.__iter__())
        all_entry_types = a_entries | b_entries
        for entry_type in all_entry_types:
            if (entry_type in a_entries) and (entry_type in b_entries):
                a_entry = self[entry_type]
                b_entry = other[entry_type]
                value = a_entry.value.append(b_entry.value)
                entry_brief = a_entry.brief 
                entry_verbose = a_entry.verbose 
            elif entry_type in a_entries:
                a_entry = self[entry_type]
                value = a_entry.value
                entry_brief = a_entry.brief 
                entry_verbose = a_entry.verbose 
            elif entry_type in b_entries:
                b_entry = other[entry_type]
                value = b_entry.value
                entry_brief = b_entry.brief 
                entry_verbose = b_entry.verbose 

            new_entry = Entry(entry_brief, value, entry_verbose)
            new_summary[entry_type] = new_entry
            
        return new_summary

    def __getitem__(self, key):
        '''Bla bla

        '''
        try:
            ret = self.entry_collector[key] 
        except KeyError:
            raise KeyError('An entry for  %s not found in Summary' %(key))

        if ret is None:
            raise KeyError('A live entry of name %s not found in Summary' %(key))

        return ret

    def __setitem__(self, key, value):
        '''Bla bla

        '''
        self.entry_collector[key] = value 

    def __iter__(self):
        '''Bla bla

        '''
        return iter(self._get_live_entries())

    def __init__(self, label, nresidues=None, nresidues_polarity=None,
                 rresidues_polarity=None, bfactor_chain_stat=None,
                 bb_torsions=None, **kwargs):
        '''Bla bla

        '''
        self.calculator = StructureCalculator(**kwargs)

        self.label = label 
        self.entry_collector = {'nresidues' : nresidues,
                                'nresidues_polarity' : nresidues_polarity,
                                'rresidues_polarity' : rresidues_polarity,
                                'bfactor_chain_stat' : bfactor_chain_stat,
                                'bb_torsions' : bb_torsions}

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
