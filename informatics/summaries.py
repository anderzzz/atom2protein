'''Bla bla

'''
from informatics.datacontainers import Structure
from informatics.calculators import StructureCalculator

import inspect
import pandas as pd
from collections import namedtuple

class ConsistencyError(Exception):
    pass

Entry = namedtuple('Entry', 'brief, value, verbose')

class StructureSummarizer:
    '''Bla bla

    '''
    SUMMARY_KEY = {'nresidues' : {'func' : 'cmp_nresidues', 
        'brief' : 'number of residues',
        'verbose' : 'Total number of residues per chain, including ' + \
                     'residues comprised of heteroatoms, such as water.'},

                   'bb_torsions' : {'func' : 'cmp_bb_torsions',
        'brief' : 'backbone torsion angles',
        'verbose' : ''},

                   'nresidues_polarity' : {'func' : 'cmp_nresidues_polarity',
        'brief' : 'number of residues in polarity classes',
        'verbose' : ''},

                   'bfactor_chain_stat' : {'func' : 'cmp_bfactor_chain_stat',
        'brief' : 'B-factor chain statistics',
        'verbose' : ''},

                   'rresidues_polarity' : {'func' : 'cmp_rresidues_polarity',
        'brief' : 'percentage of residues in polarity classes',
        'verbose' : ''}
        }
    '''dict: Dictionary that defines how to associate a property name with a
    property calculator function, and property semantics, both brief and
    verbose. This dictionary, and only this dictionary, encodes all relations
    between a summary property and the calculator machinery.

    '''
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

    def _make_populate_func(self, name, cmp_func, brief, verbose):
        '''Bla bla

        '''
        def _populate_x(structure):
            value = self._add_id_to(cmp_func(structure))
            self[name] = Entry(brief, value, verbose)

        return _populate_x

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
                 bb_torsions=None, kwargs_to_calc={}):
        '''Bla bla

        '''
        self.label = label 
        self.calculator = StructureCalculator(**kwargs_to_calc)

        # Obtain the property input arguments and their name. They define the
        # properties to store values for and associate calculator methods with.
        frame = inspect.currentframe()
        args_to_init = inspect.getargvalues(frame).args
        vals_to_init = inspect.getargvalues(frame).locals
        prop_args = [v for v in args_to_init if not v in ['self', 'label',
                                                          'kwargs_to_calc']]

        self.entry_collector = dict([(key, value) for key, value in
                                                      vals_to_init.items() 
                                                  if key in prop_args]) 

        # Verify that no properties are defined without calculator method, or
        # vice versa.
        test_set1 = set(self.entry_collector) - set(self.SUMMARY_KEY.keys())
        test_set2 = set(self.SUMMARY_KEY.keys()) - set(self.entry_collector)
        if not test_set1 == set([]):
            raise ConsistencyError('More summary properties defined than ' + \
                                   'associated with calculator method. ' + \
                                   'Excess properties are: ' + ','.join(test_set1))
        if not test_set2 == set([]):
            raise ConsistencyError('Fewer summary properties defined than ' + \
                                   'associations with calculator methods. ' + \
                                   'Missing properties are: ' + ','.join(test_set2))

        # Dynamically create population methods for each property.
        for prop, prop_cmp in self.SUMMARY_KEY.items():
            brief = prop_cmp['brief']
            verbose = prop_cmp['verbose']
            cmp_func = getattr(self.calculator, prop_cmp['func'])
            pop_func = self._make_populate_func(prop, cmp_func, brief, verbose)
            setattr(self, 'populate_' + prop, pop_func)


def create_summarizer_for(container, kwargs_to_sum={}):
    '''Bla bla

    '''
    if isinstance(container, Structure):
        ret = StructureSummarizer(container.label, **kwargs_to_sum)
    else:
        raise NotImplementedError("Only structures so far")

    return ret
