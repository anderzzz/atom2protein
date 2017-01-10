'''Bla bla

'''
from primitivedata import Structure, PubMedEntry
from calculators import StructureCalculator

import pandas as pd
from collections import namedtuple

Entry = namedtuple('Entry', 'brief, value, verbose')

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
        self['bb_torsions'] = Entry('backbone torsion angles', value, '')

    def populate_bfactor_chain_stat(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_bfactor_chain_stat(structure))
        self['bfactor_chain_stat'] = Entry('B-factor chain statistics', value, '')

    def populate_nresidues(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_nresidues(structure))
        self['nresidues'] = Entry('number of residues', value, '')

    def populate_nresidues_polarity(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_nresidues_polarity(structure))
        self['nresidues_polarity'] = Entry('number of polarity residues', value, '')

    def populate_rresidues_polarity(self, structure):
        '''Bla bla

        '''
        value = self._add_id_to(self.calculator.cmp_rresidues_polarity(structure))
        self['rresidues_polarity'] = Entry('percentage of polarity residues', value, '')

    def items(self):
        '''Bla bla

        '''
        for x in self:
            yield (x, self[x])

    def groupby(self, index_reduce, agg_func, entry_subset=None):
        '''Bla bla

        '''
        if entry_subset is None:
            entry_subset = list(self.__iter__())

        new_summary = StructureSummarizer(self.label)

        for entry_type in self:

            if entry_type in entry_subset:
                serie = self[entry_type].value
                levels = [x for x in serie.index.names if not x in index_reduce]
                group_by_pd = serie.groupby(level=levels, axis=0)
                serie_agg = group_by_pd.agg(agg_func)

                entry_brief = self[entry_type].brief + ' with grouping and aggregation'
                entry_verbose = self[entry_type].verbose + ' with grouping on ' + \
                '%s and aggregation by %s' %(str(levels), str(agg_func))
                new_entry = Entry('grouped on', serie_agg, entry_verbose)

            else:
                new_entry = self[entry_type]

            new_summary[entry_type] = new_entry

        return new_summary

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
        # Initialize the sum Summarizer
        new_summary = StructureSummarizer(self.label + '+' + other.label)

        # Loop over the union of Entry types and perform the Pandas algebra
        a_entries = set(self.__iter__())
        b_entries = set(other.__iter__())
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
        live_entries = []
        for member, value in self.entry_collector.items():
            if isinstance(value, Entry):
                live_entries.append(member)
        
        return iter(live_entries)

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

